import logging

import boto3
import botocore.exceptions
from botocore.config import Config

from taichu_storage import StorageInterface
import os


class StorageBoto3(StorageInterface):
    def __init__(self, cfgs=None):
        if cfgs is None:
            cfgs = {}

        bucket = cfgs.get('boto3_bucket')
        ak = cfgs.get('boto3_ak')
        sk = cfgs.get('boto3_sk')
        region_name = cfgs.get('boto3_region_name')
        endpoint_url = cfgs.get('boto3_endpoint_url')

        self._bucket = bucket
        self._client = boto3.client(
            's3',
            aws_access_key_id=ak,
            aws_secret_access_key=sk,
            use_ssl=True,
            region_name=region_name,
            endpoint_url=endpoint_url,
            config=Config(s3={"addressing_style": "virtual", "signature_version": 's3v4'}))

    def write_bytes(self, content_bytes, key):
        self._client.put_object(Body=content_bytes, Bucket=self._bucket, Key=key)

    def write_string(self, content_string, key):
        try:
            data = content_string.encode('utf-8')
            self._client.put_object(Body=data, Bucket=self._bucket, Key=key)
        except Exception as e:
            logging.info("key: " + key)
            logging.error("TaichuStorageError", e)

    def upload_file(self, file_path, key):
        self._client.upload_file(file_path, self._bucket, key)

    def download_file(self, file_path, key):
        self._client.download_file(self._bucket, key, file_path)

    def download_directory(self, key, local_target_directory):
        response = self._client.list_objects_v2(Bucket=self._bucket, Prefix=key)
        m = {}
        for obj in response.get('Contents', []):
            s3_key = obj['Key']
            # local_file_path = os.path.join(local_target_directory, os.path.relpath(s3_key, key))
            local_file_path = f'{local_target_directory}{s3_key.replace(key, "")}'
            dirname = os.path.dirname(local_file_path)
            try:
                if not m.get(dirname, False):
                    os.makedirs(dirname, exist_ok=True)
                    m[dirname] = True
                    print('make dir: '+dirname)
                if os.path.isdir(local_file_path):
                    print(local_file_path + " is a directory continue")
                    continue
                self._client.download_file(self._bucket, s3_key, local_file_path)
                print(f'Downloaded s3://{self._bucket}/{s3_key} to {local_file_path}')
            except Exception as e:
                logging.error(e)
                logging.info(s3_key)
                logging.info(local_file_path)
                logging.info('dirname: %s' % dirname)

    def generate_signed_url(self, key, expiration=600, host_url=None):
        try:
            url = self._client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self._bucket, 'Key': key},
                ExpiresIn=expiration
            )
            if not host_url:
                return url
            h = self._boto_host
            if self._boto_port != 80:
                h = self._boto_host + ':' + str(self._boto_port)
            url = url.replace(h, host_url)
            print("URL_RETURN: ", url)
            return url
        except botocore.exceptions.ClientError as e:
            logging.error("Error generating presigned URL:", e)
            return None

    def generate_upload_credentials(self, key, expiration=3600):
        return self._client.generate_presigned_post(self._bucket, key, ExpiresIn=expiration)
        # {'url': 'http://xxxx', 'fields': {'key': 'sys/test/abc.txt',
        # 'x-amz-algorithm': 'AWS4-HMAC-SHA256', 'x-amz-credential': 'root/20230704/cn/s3/aws4_request',
        # 'x-amz-date': '20230704T073038Z',
        # 'policy':
        # 'eyJleHBpcmF0aW9uIjogIjIwMjMtMDctMDRUMDg6MzA6MzhaIiwgImNvbmRpdGlvbnMiOiBbeyJidWNrZXQiOiAicHVibGlzaC1kYXRhIn0sIHsia2V5IjogInN5cy90ZXN0L2FiYy50eHQifSwgeyJ4LWFtei1hbGdvcml0aG0iOiAiQVdTNC1ITUFDLVNIQTI1NiJ9LCB7IngtYW16LWNyZWRlbnRpYWwiOiAicm9vdC8yMDIzMDcwNC9jbi9zMy9hd3M0X3JlcXVlc3QifSwgeyJ4LWFtei1kYXRlIjogIjIwMjMwNzA0VDA3MzAzOFoifV19',
        # 'x-amz-signature': 'accdd539815bb170132a109c1802630ab3bf1e582f7792e19d51100158cb5057'}}


if __name__ == '__main__':
    c = StorageBoto3({

    })
    # c.write_string('abc', 'sys/test/abc.txt')
    # print(c.generate_signed_url('sys/test/abc.txt'))
    print(c.generate_upload_credentials('sys/test/abc.txt'))
    # c.write_json({'abc': "123"}, 'sys/test/json.json')
    # c.upload_file('test/b.txt', 'sys/test/b.txt')
    # c.upload_directory('test', 'sys/test/directory')
    # c.download_directory('sys/test/directory', 'test/download')

