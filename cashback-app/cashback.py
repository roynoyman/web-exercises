import datetime
from dataclasses import dataclass, asdict
from enum import Enum


@dataclass
class Cashback:
    _id: str
    amount: int
    merchant_name: str
    customer_name: str
    customer_email: str
    created_at: str

    @staticmethod
    def from_request(config):
        return Cashback(config['cashback_id'],
                        config['amount'],
                        config['merchant_name'],
                        config['customer_name'],
                        config['customer_email'],
                        str(datetime.time.hour)
                        )

    def asdict(self):
        return asdict(self)
