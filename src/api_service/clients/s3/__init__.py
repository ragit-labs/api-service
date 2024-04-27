from __future__ import annotations
import logging
import boto3
import botocore

class S3Client:

    def __init__(self: S3Client, bucket_name: str, endpoint_url: str, region_name: str, aws_access_key_id: str, aws_secret_access_key: str):
        self.bucket_name = bucket_name
        session = boto3.Session()
        self.client = session.client(
            's3', 
            endpoint_url=endpoint_url, 
            region_name=region_name, 
            aws_access_key_id=aws_access_key_id, 
            aws_secret_access_key=aws_secret_access_key
        )
        print("Creating client...", bucket_name, region_name, endpoint_url, aws_access_key_id, aws_secret_access_key)
    
    def upload_file(self: S3Client, data: bytes, key: str):
        # TODO: add ACL, Metadata later
        try:
            self.client.put_object(
                Body=data, 
                Bucket=self.bucket_name,
                Key=key
            )
        except botocore.exceptions.ClientError as e:
            logging.error(f"Error uploading file to S3: {e}")
            return False
        return True

    def download_file(self: S3Client, source_path: str, dest_path: str):
        self.client.download_file(self.bucket_name, source_path, dest_path)
    
    def download_file_as_obj(self: S3Client, source_path: str):
        return self.client.get_object(Bucket=self.bucket_name, Key=source_path)

    def create_presigned_post(self: S3Client, key: str, expiration: int = 300):
        return self.client.generate_presigned_post(self.bucket_name, key, ExpiresIn=expiration)

    def create_presigned_url(self: S3Client, key: str, expiration: int = 300):
        return self.client.generate_presigned_url(ClientMethod='put_object', Params={'Bucket': self.bucket_name, 'Key': key}, ExpiresIn=expiration, HttpMethod='PUT')

    def delete_file(self: S3Client, key: str):
        self.client.delete_object(Bucket=self.bucket_name, Key=key)
