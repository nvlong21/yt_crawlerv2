import os
import boto3
from .config import settings
def get_s3_client():
    if settings.AWS_S3:
        s3 = boto3.client("s3")
    elif settings.S3_CLOUDPROVIDER == "aws":
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.S3_ACCESSKEY,
            aws_secret_access_key=settings.S3_SECRETKEY,
            region_name=settings.S3_REGION
        )
    else:
        s3 = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOOINT,
            aws_access_key_id=settings.S3_ACCESSKEY,
            aws_secret_access_key=settings.S3_SECRETKEY,
            region_name=settings.S3_REGION
        )        
    try:
        yield s3
    finally:
        pass   