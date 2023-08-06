import boto3
from os import getenv as _getenv


def save_to_s3(s3_key: str, content_body: str, aws_access_key_id=None,
               aws_secret_access_key=None, aws_region=None, s3_bucket=None):
    if aws_access_key_id is None: aws_access_key_id = _getenv('aws_access_key_id')
    if aws_secret_access_key is None: aws_secret_access_key = _getenv('aws_secret_access_key')
    if aws_region is None: aws_region = _getenv('aws_region')
    if s3_bucket is None: s3_bucket = _getenv('s3_bucket_risk')

    s3_client = boto3.client('s3'
                             , aws_access_key_id=aws_access_key_id
                             , aws_secret_access_key=aws_secret_access_key
                             , region_name=aws_region)
    s3_client.put_object(Bucket=s3_bucket
                         , Body=content_body
                         , Key=s3_key
                         )


def get_from_s3(s3_key, filename, aws_access_key_id=None, aws_secret_access_key=None, aws_region=None, s3_bucket=None):
    if aws_access_key_id is None: aws_access_key_id = _getenv('aws_access_key_id')
    if aws_secret_access_key is None: aws_secret_access_key = _getenv('aws_secret_access_key')
    if aws_region is None: aws_region = _getenv('aws_region_name')
    if s3_bucket is None: s3_bucket = _getenv('s3_bucket_lms')

    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    s3_result = s3_client.download_file(
        Bucket=s3_bucket,
        Key=s3_key,
        Filename=filename
    )

    return s3_result
