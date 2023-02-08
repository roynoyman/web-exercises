from dataclasses import dataclass, asdict
from enum import Enum


class ApplicationActualState(str, Enum):
    # livy states
    DEAD = "dead"
    RUNNING = "running"
    STARTING = "starting"

    # livy states unused for batches
    NOT_STARTED = "not_started"
    RECOVERING = "recovering"
    IDLE = "idle"
    BUSY = "busy"
    SHUTTING_DOWN = "shutting_down"
    ERROR = "error"
    KILLED = "killed"
    SUCCESS = "success"

    # default state when livy cant give the state of the application
    NOT_RUNNING = 'not_running'


class CashbackValidation(str, Enum):
    VALID = 'valid'
    NOT_VALID = 'not_valid'


class EventType(str, Enum):
    CREATED = 'created'
    EMAIL_SENT = 'email_sent'
    ISSUED = 'issued'


@dataclass
class Event:
    _id: int
    type: str

    @staticmethod
    def from_request(config):
        return Event(config['cashback_id'], config['type'])

    # def set_actual_state(self, state: ApplicationActualState):
    #     self.actual_state = state

    def asdict(self):
        return asdict(self)
