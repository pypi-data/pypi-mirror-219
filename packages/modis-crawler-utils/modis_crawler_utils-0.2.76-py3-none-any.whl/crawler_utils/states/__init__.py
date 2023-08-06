import abc
import dataclasses
import typing

ID = typing.Union[str, int]


@dataclasses.dataclass(frozen=True)
class StateKey:
    crawler_id: ID = None
    periodic_job_id: ID = None
    information_source_id: ID = None
    credential_id: ID = None
    custom_key: str = None


@dataclasses.dataclass
class State:
    id: ID = None
    key: StateKey = None
    state: dict = dataclasses.field(default_factory=lambda: {})
    version: int = 0


@dataclasses.dataclass
class CredentialState(State):
    cookies: typing.Dict[str, str] = dataclasses.field(default_factory=lambda: {})


class StatesStore(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def pull_state(self, id_or_key: typing.Union[ID, StateKey]) -> State:
        pass

    @abc.abstractmethod
    def push_state(self, state: State) -> State:
        pass


class CredentialStatesStore(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def pull_credential_state(self, id_or_key: typing.Union[ID, StateKey]) -> CredentialState:
        pass

    @abc.abstractmethod
    def push_credential_state(self, state: CredentialState, status: str = 'Valid') -> CredentialState:
        pass


class VersionConflict(Exception):
    def __init__(self):
        super().__init__('The specified version of the state does not match current')
