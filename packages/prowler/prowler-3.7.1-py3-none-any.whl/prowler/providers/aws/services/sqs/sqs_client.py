from prowler.providers.aws.lib.audit_info.audit_info import current_audit_info
from prowler.providers.aws.services.sqs.sqs_service import SQS

sqs_client = SQS(current_audit_info)
