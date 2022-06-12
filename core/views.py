import json
import os

from django.views    import View
from django.http     import JsonResponse

import boto3
import logging
from my_settings         import AWS_STORAGE_BUCKET_NAME, AWS_SECRET_ACCESS_KEY
from botocore.exceptions import ClientError

bucket = AWS_STORAGE_BUCKET_NAME
client = boto3.client('s3')

def upload_fileobj(Fileobj, Bucket, Key, ExtraArgs, Callback=None, Config=None):
    try:
        client.upload_fileobj(Fileobj, Bucket, Key, ExtraArgs)

    except ClientError as e:
        logging.error(e)
        return False

    return True