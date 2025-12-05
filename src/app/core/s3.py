import os
import boto3
from pathlib import Path
from .config import settings
def upload_folder_to_s3(local_folder, bucket="", s3_prefix=""):
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
    local_folder = Path(local_folder)
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            local_path = Path(root) / file
            relative_path = local_path.relative_to(local_folder)
            print(relative_path)
            s3_key = str(Path(s3_prefix) / relative_path).replace("\\", "/")

            s3.upload_file(
                Filename=str(local_path),
                Bucket=bucket,
                Key=s3_key
            )
            print("Uploaded:", s3_key)
