import os
import pathlib
import sys

from boto3 import client, session
from botocore.credentials import RefreshableCredentials
from botocore.session import get_session

from prowler.config.config import aws_services_json_file
from prowler.lib.check.check import list_modules, recover_checks_from_service
from prowler.lib.logger import logger
from prowler.lib.utils.utils import open_file, parse_json_file
from prowler.providers.aws.lib.audit_info.models import AWS_Assume_Role, AWS_Audit_Info


################## AWS PROVIDER
class AWS_Provider:
    def __init__(self, audit_info):
        logger.info("Instantiating aws provider ...")
        self.aws_session = self.set_session(audit_info)
        self.role_info = audit_info.assumed_role_info

    def get_session(self):
        return self.aws_session

    def set_session(self, audit_info):
        try:
            # If we receive a credentials object filled is coming form an assumed role, so renewal is needed
            if audit_info.credentials:
                logger.info("Creating session for assumed role ...")
                # From botocore we can use RefreshableCredentials class, which has an attribute (refresh_using)
                # that needs to be a method without arguments that retrieves a new set of fresh credentials
                # asuming the role again. -> https://github.com/boto/botocore/blob/098cc255f81a25b852e1ecdeb7adebd94c7b1b73/botocore/credentials.py#L395
                assumed_refreshable_credentials = RefreshableCredentials(
                    access_key=audit_info.credentials.aws_access_key_id,
                    secret_key=audit_info.credentials.aws_secret_access_key,
                    token=audit_info.credentials.aws_session_token,
                    expiry_time=audit_info.credentials.expiration,
                    refresh_using=self.refresh_credentials,
                    method="sts-assume-role",
                )
                # Here we need the botocore session since it needs to use refreshable credentials
                assumed_botocore_session = get_session()
                assumed_botocore_session._credentials = assumed_refreshable_credentials
                assumed_botocore_session.set_config_variable(
                    "region", audit_info.profile_region
                )
                return session.Session(
                    profile_name=audit_info.profile,
                    botocore_session=assumed_botocore_session,
                )
            # If we do not receive credentials start the session using the profile
            else:
                logger.info("Creating session for not assumed identity ...")
                # Input MFA only if a role is not going to be assumed
                if audit_info.mfa_enabled and not audit_info.assumed_role_info.role_arn:
                    mfa_ARN, mfa_TOTP = input_role_mfa_token_and_code()
                    get_session_token_arguments = {
                        "SerialNumber": mfa_ARN,
                        "TokenCode": mfa_TOTP,
                    }
                    sts_client = client("sts")
                    session_credentials = sts_client.get_session_token(
                        **get_session_token_arguments
                    )
                    return session.Session(
                        aws_access_key_id=session_credentials["Credentials"][
                            "AccessKeyId"
                        ],
                        aws_secret_access_key=session_credentials["Credentials"][
                            "SecretAccessKey"
                        ],
                        aws_session_token=session_credentials["Credentials"][
                            "SessionToken"
                        ],
                        profile_name=audit_info.profile,
                    )
                else:
                    return session.Session(
                        profile_name=audit_info.profile,
                    )
        except Exception as error:
            logger.critical(
                f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}"
            )
            sys.exit(1)

    # Refresh credentials method using assume role
    # This method is called "adding ()" to the name, so it cannot accept arguments
    # https://github.com/boto/botocore/blob/098cc255f81a25b852e1ecdeb7adebd94c7b1b73/botocore/credentials.py#L570
    def refresh_credentials(self):
        logger.info("Refreshing assumed credentials...")

        response = assume_role(self.aws_session, self.role_info)
        refreshed_credentials = dict(
            # Keys of the dict has to be the same as those that are being searched in the parent class
            # https://github.com/boto/botocore/blob/098cc255f81a25b852e1ecdeb7adebd94c7b1b73/botocore/credentials.py#L609
            access_key=response["Credentials"]["AccessKeyId"],
            secret_key=response["Credentials"]["SecretAccessKey"],
            token=response["Credentials"]["SessionToken"],
            expiry_time=response["Credentials"]["Expiration"].isoformat(),
        )
        logger.info("Refreshed Credentials:")
        logger.info(refreshed_credentials)
        return refreshed_credentials


def assume_role(session: session.Session, assumed_role_info: AWS_Assume_Role) -> dict:
    try:
        assume_role_arguments = {
            "RoleArn": assumed_role_info.role_arn,
            "RoleSessionName": "ProwlerAsessmentSession",
            "DurationSeconds": assumed_role_info.session_duration,
        }

        if assumed_role_info.external_id:
            assume_role_arguments["ExternalId"] = assumed_role_info.external_id

        if assumed_role_info.mfa_enabled:
            mfa_ARN, mfa_TOTP = input_role_mfa_token_and_code()
            assume_role_arguments["SerialNumber"] = mfa_ARN
            assume_role_arguments["TokenCode"] = mfa_TOTP

        # set the info to assume the role from the partition, account and role name
        sts_client = session.client("sts")
        assumed_credentials = sts_client.assume_role(**assume_role_arguments)
    except Exception as error:
        logger.critical(
            f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}"
        )
        sys.exit(1)

    else:
        return assumed_credentials


def input_role_mfa_token_and_code() -> tuple[str]:
    """input_role_mfa_token_and_code ask for the AWS MFA ARN and TOTP and returns it."""
    mfa_ARN = input("Enter ARN of MFA: ")
    mfa_TOTP = input("Enter MFA code: ")
    return (mfa_ARN.strip(), mfa_TOTP.strip())


def generate_regional_clients(
    service: str, audit_info: AWS_Audit_Info, global_service: bool = False
) -> dict:
    try:
        regional_clients = {}
        service_regions = get_available_aws_service_regions(service, audit_info)
        # Check if it is global service to gather only one region
        if global_service:
            if service_regions:
                if audit_info.profile_region in service_regions:
                    service_regions = [audit_info.profile_region]
                service_regions = service_regions[:1]
        for region in service_regions:
            regional_client = audit_info.audit_session.client(
                service, region_name=region, config=audit_info.session_config
            )
            regional_client.region = region
            regional_clients[region] = regional_client
        return regional_clients
    except Exception as error:
        logger.error(
            f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}]: {error}"
        )


def get_aws_available_regions():
    try:
        actual_directory = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
        with open_file(f"{actual_directory}/{aws_services_json_file}") as f:
            data = parse_json_file(f)

        regions = set()
        for service in data["services"].values():
            for partition in service["regions"]:
                for item in service["regions"][partition]:
                    regions.add(item)
        return list(regions)
    except Exception as error:
        logger.error(f"{error.__class__.__name__}: {error}")
        return []


def get_checks_from_input_arn(audit_resources: list, provider: str) -> set:
    """get_checks_from_input_arn gets the list of checks from the input arns"""
    checks_from_arn = set()
    # Handle if there are audit resources so only their services are executed
    if audit_resources:
        services_without_subservices = ["guardduty", "kms", "s3", "elb", "efs"]
        service_list = set()
        sub_service_list = set()
        for resource in audit_resources:
            service = resource.split(":")[2]
            sub_service = resource.split(":")[5].split("/")[0].replace("-", "_")
            # WAF Services does not have checks
            if service != "wafv2" and service != "waf":
                # Parse services when they are different in the ARNs
                if service == "lambda":
                    service = "awslambda"
                elif service == "elasticloadbalancing":
                    service = "elb"
                elif service == "elasticfilesystem":
                    service = "efs"
                elif service == "logs":
                    service = "cloudwatch"
                # Check if Prowler has checks in service
                try:
                    list_modules(provider, service)
                except ModuleNotFoundError:
                    # Service is not supported
                    pass
                else:
                    service_list.add(service)

                # Get subservices to execute only applicable checks
                if service not in services_without_subservices:
                    # Parse some specific subservices
                    if service == "ec2":
                        if sub_service == "security_group":
                            sub_service = "securitygroup"
                        if sub_service == "network_acl":
                            sub_service = "networkacl"
                        if sub_service == "image":
                            sub_service = "ami"
                    if service == "rds":
                        if sub_service == "cluster_snapshot":
                            sub_service = "snapshot"
                    sub_service_list.add(sub_service)
                else:
                    sub_service_list.add(service)
        checks = recover_checks_from_service(service_list, provider)

        # Filter only checks with audited subservices
        for check in checks:
            if any(sub_service in check for sub_service in sub_service_list):
                if not (sub_service == "policy" and "password_policy" in check):
                    checks_from_arn.add(check)

    # Return final checks list
    return sorted(checks_from_arn)


def get_regions_from_audit_resources(audit_resources: list) -> list:
    """get_regions_from_audit_resources gets the regions from the audit resources arns"""
    audited_regions = []
    for resource in audit_resources:
        region = resource.split(":")[3]
        if region and region not in audited_regions:  # Check if arn has a region
            audited_regions.append(region)
    if audited_regions:
        return audited_regions
    return None


def get_available_aws_service_regions(service: str, audit_info: AWS_Audit_Info) -> list:
    # Get json locally
    actual_directory = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
    with open_file(f"{actual_directory}/{aws_services_json_file}") as f:
        data = parse_json_file(f)
    # Check if it is a subservice
    json_regions = data["services"][service]["regions"][audit_info.audited_partition]
    if audit_info.audited_regions:  # Check for input aws audit_info.audited_regions
        regions = list(
            set(json_regions).intersection(audit_info.audited_regions)
        )  # Get common regions between input and json
    else:  # Get all regions from json of the service and partition
        regions = json_regions
    return regions


def get_default_region(service: str, audit_info: AWS_Audit_Info) -> str:
    """get_default_region gets the default region based on the profile and audited service regions"""
    service_regions = get_available_aws_service_regions(service, audit_info)
    default_region = get_global_region(
        audit_info
    )  # global region of the partition when all regions are audited and there is no profile region
    if audit_info.profile_region in service_regions:
        # return profile region only if it is audited
        default_region = audit_info.profile_region
    # return first audited region if specific regions are audited
    elif audit_info.audited_regions:
        default_region = audit_info.audited_regions[0]
    return default_region


def get_global_region(audit_info: AWS_Audit_Info) -> str:
    """get_global_region gets the global region based on the audited partition"""
    global_region = "us-east-1"
    if audit_info.audited_partition == "aws-cn":
        global_region = "cn-north-1"
    elif audit_info.audited_partition == "aws-us-gov":
        global_region = "us-gov-east-1"
    elif "aws-iso" in audit_info.audited_partition:
        global_region = "aws-iso-global"
    return global_region
