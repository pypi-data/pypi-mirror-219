import logging

from taichu_storage import StorageInterface
from obs import ObsClient, PutObjectHeader


class StorageObs(StorageInterface):

    def __init__(self, cfgs=None):
        if cfgs is None:
            cfgs = {}

        self._bucket = cfgs.get('obs_bucket')
        obs_ak = cfgs.get('obs_ak')
        obs_sk = cfgs.get('obs_sk')
        obs_server = cfgs.get('obs_server')

        self._client = ObsClient(
            access_key_id=obs_ak,
            secret_access_key=obs_sk,
            server=obs_server
        )

    def download_file(self, file_path, key):
        pass

    def download_directory(self, key, local_target_directory):
        pass

    def generate_signed_url(self, key, expiration=600, host_url=None):
        try:
            rps = self._client.createSignedUrl("GET", self._bucket, key, "", 6000, {}, {})
            return rps.signedUrl
        except Exception as e:
            logging.error(e)
            return ''

    def generate_upload_credentials(self, key, expiration=3600):
        pass

    def write_bytes(self, content_bytes, key):
        self.write_string(content_bytes, key)

    def write_string(self, content_string, key):
        try:
            self._client.putContent(self._bucket, key, content=content_string)
        except Exception as e:
            logging.info("key: " + key)
            logging.error("TaichuStorageError", e)

    def upload_file(self, file_path, key):
        headers = PutObjectHeader()
        headers.contentType = 'text/plain'
        self._client.putFile(self._bucket, key, file_path, metadata={}, headers=headers)
