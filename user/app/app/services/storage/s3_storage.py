from functools import lru_cache
from typing import Any
from app.services.storage.base_storage import BaseStorage
from boto3.session import Session
from botocore.client import BaseClient


class S3Storage(BaseStorage):
    def __init__(
            self,
            bucket_name: str,
            service_name: str,
            endpoints_url: str,
            access_key_id: str,
            secret_access_key: str,
    ) -> None:
        self.ready_to_initialize = False
        self.bucket_name: str = bucket_name
        self.service_name: str = service_name
        self.endpoints_url: str = endpoints_url
        self.access_key_id: str = access_key_id
        self.secret_access_key: str = secret_access_key
        self._session: Session = Session()
        self.ready_to_initialize = True
        self._init_client()

    def _init_client(self):
        self._client: BaseClient = self._session.client(
            service_name=self.service_name,
            endpoint_url=self.endpoints_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
        )

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)
        if self.ready_to_initialize and __name in ("service_name", "endpoints_url", "access_key_id", "secret_access_key"):
            self._init_client()

    @property
    def prefix(self) -> str:
        return self._client._endpoint.host + '/' + self.bucket_name + '/'

    def get_key_from_link(self, link: str) -> str:
        return link[len(self.prefix):]

    def load(
        self,
        key: str,
        file: bytes,
        content_type: str,
    ) -> str | None:
        result = self._client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=file,
            ContentType=content_type
        )
        if not (200 <= result.get('ResponseMetadata', {}).get('HTTPStatusCode', 500) < 300):
            return None
        return self.prefix + key

    def remove(self, link: str) -> None:
        key = self.get_key_from_link(link)
        self._client.delete_object(Bucket=self.bucket_name, Key=key)
