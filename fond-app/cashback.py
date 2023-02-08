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


class CashbackState(str, Enum):
    CREATED = 'created'
    EMAIL_SENT = 'email_sent'
    ISSUED = 'issued'


@dataclass
class Cashback:
    _id: str
    amount: int
    state: CashbackState
    valid: CashbackValidation

    @staticmethod
    def from_request(config):
        return Cashback(config['_id'],
                        config['amount'],
                        config['state'],
                        CashbackValidation.VALID)

    # def set_actual_state(self, state: ApplicationActualState):
    #     self.actual_state = state

    def asdict(self):
        return asdict(self)
