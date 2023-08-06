import abc
from typing import List

from crawler_utils.credentials import Credential


class CredentialsStore(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get(self, domain: str) -> List[Credential]:
        pass

    @abc.abstractmethod
    def get_by_id(self, credential_id: int) -> Credential:
        pass

    @abc.abstractmethod
    def update(self, credential: Credential) -> int:
        pass


class CredentialsStoreError(Exception):
    pass


class NoSuchCredentialError(CredentialsStoreError):
    pass


class CredentialVersionConflictError(CredentialsStoreError):
    pass
