import boto3, uuid, logging

from django.conf         import settings
from botocore.exceptions import ClientError

class AWSFileUploader:
    def __init__(self, client):
        self.client = client

    def upload(self, file, config, content_type):
        try:
            file_id    = str(uuid.uuid4())
            extra_args = {'ContentType' : file.content_type}
            key        = content_type + "/" + file_id

            self.client.upload_fileobj(
                file,
                config,
                key,
                extra_args
            )

            return f'https://{config}.s3.{settings.AWS_REGION}.amazonaws.com/{content_type}/{file_id}'

        except:
            return None

    def delete(self, file_name, config):
            self.client.delete_object(
                Bucket = config,
                Key=f'{file_name}'
            )

class FileHandler:
    def __init__(self, file_uploader):
        self.file_uploader = file_uploader
    
    def upload(self, file, config, content_type):
        return self.file_uploader.upload(file, config, content_type)

    def delete(self, file_name, config):
        return self.file_uploader.delete(file_name, config)