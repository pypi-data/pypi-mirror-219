import random
from typing import Callable, List, Optional, Union

from scrapy.exceptions import NotConfigured
from scrapy.settings import Settings
from scrapy.utils.misc import create_instance, load_object

from crawler_utils.credentials.credential import Credential
from crawler_utils.credentials.store import CredentialVersionConflictError, CredentialsStore
from crawler_utils.credentials.store.local import FileCredentialsStore, InMemoryCredentialsStore
from crawler_utils.credentials.store.talisman import TalismanCredentialsStore

SelectionStrategy = Callable[[List[Credential]], Credential]
ConflictResolutionStrategy = Callable[[Credential, Credential], bool]


class CredentialsManager:

    def __init__(self,
                 store: CredentialsStore,
                 domain: str,
                 selection_strategy: Union[str, SelectionStrategy] = 'least used',
                 conflict_resolution_strategy: Union[str, ConflictResolutionStrategy] = 'pull',
                 credential_id: int = None):
        """
        Credential manager for Crawlers API.

        :param store: Credentials store
        :param domain: Credentials domain
        :param selection_strategy:
        A strategy to select single credential from credentials list.
        - 'random' - selects random valid credential
        - 'least used' (default) - selects credential which was used the least
        - callable with signature (credentials: List[Credential]) -> Credential
        :param conflict_resolution_strategy:
        A strategy to resolve version conflict on credential update.
        - 'raise' - just raises CredentialVersionConflictError
        - 'pull' - updates local credential with remote state
        - 'push' - updates remote credential with local state
        - callable with signature (local: Credential, remote: Credential) -> bool, which
            - puts merged state into local credential
            - returns true if new local state must be pushed to remote
        :param credential_id: Pre-selected credential id
        """
        if domain is None:
            raise ValueError('Undefined credentials domain')
        self._store = store
        self._domain = domain
        self._selection_strategy = selection_strategy
        self._conflict_resolution_strategy = conflict_resolution_strategy
        if credential_id:
            credential = self._store.get_by_id(credential_id)
            if credential.domain != domain:
                raise ValueError(f'Expected domain {domain}, but selected {credential} has {credential.domain}')
            self._credentials = [credential]
        else:
            self._credentials = self._store.get(self._domain)

    @classmethod
    def from_settings(cls, settings: Settings, store: CredentialsStore = None, **kwargs):
        if not store:
            store = cls.load_credentials_store(settings)
        if isinstance(store, TalismanCredentialsStore):
            credential_id = store.job_env.credential_id
        else:
            credential_id = settings.get('CREDENTIAL_ID')
        return cls(**{
            'store': store,
            'credential_id': credential_id,
            'domain': settings.get('CREDENTIALS_DOMAIN'),
            'selection_strategy': settings.get('CREDENTIALS_SELECTION_STRATEGY', 'least used'),
            'conflict_resolution_strategy': settings.get('CREDENTIALS_CONFLICT_RESOLUTION_STRATEGY', 'pull'),
            **kwargs
        })

    _STORE_TYPES = {
        'talisman': TalismanCredentialsStore,
        'memory': InMemoryCredentialsStore,
        'file': FileCredentialsStore
    }

    @classmethod
    def load_credentials_store(cls, settings: Settings):
        if store_type_name := settings.get('CREDENTIALS_STORE'):
            if not (store_type := cls._STORE_TYPES.get(store_type_name)):
                store_type = load_object(store_type_name)
            return create_instance(store_type, settings, None)
        for store_type in cls._STORE_TYPES.values():
            try:
                return create_instance(store_type, settings=settings, crawler=None)
            except NotConfigured:
                pass
        raise NotConfigured('Failed to load credentials store')

    def get_credential(self, **kwargs) -> Optional[Credential]:
        """
        Selects single credential.
        """
        valid_credentials = [c for c in self._credentials if c.status == 'Valid']
        if not valid_credentials:
            return None
        if self._selection_strategy == 'random':
            return random.choice(valid_credentials)
        elif self._selection_strategy == 'least used':
            return self._select_least_used(valid_credentials)
        elif callable(self._selection_strategy):
            return self._selection_strategy(valid_credentials, kwargs)  # TODO kwargs -> **kwargs
        else:
            raise ValueError('Unknown selection strategy')

    def update_credential(self, credential: Credential, **kwargs) -> None:
        """
        Synchronizes credential state with API.
        """
        try:
            credential.version = self._store.update(credential)
        except CredentialVersionConflictError:
            if self._conflict_resolution_strategy == 'raise':
                raise
            remote_credential = self._store.get_by_id(credential.id)
            if self._conflict_resolution_strategy == 'pull':
                self._pull_update(credential, remote_credential)
            elif self._conflict_resolution_strategy == 'push':
                credential.version = remote_credential.version
                self.update_credential(credential)
            elif callable(self._conflict_resolution_strategy):
                if self._conflict_resolution_strategy(credential, remote_credential, kwargs):
                    self.update_credential(credential)
            else:
                raise ValueError('Unknown conflict resolution strategy')

    @staticmethod
    def _select_least_used(credentials):
        def get_times_used(credential):
            try:
                result = int(credential.state.get('TIMES_USED'))
            except:
                result = 0

            return result

        def inc_times_used(credential):
            credential.state['TIMES_USED'] = get_times_used(credential) + 1

        min_times_used = min(map(get_times_used, credentials))
        least_used = [c for c in credentials if get_times_used(c) == min_times_used]
        selected_credential = random.choice(least_used)
        inc_times_used(selected_credential)
        return selected_credential

    @staticmethod
    def _pull_update(local_credential, remote_credential):
        for attr in ('domain', 'type', 'login', 'password', 'token', 'description',
                     'status', 'state', 'cookies', 'version'):
            setattr(local_credential, attr, getattr(remote_credential, attr))
