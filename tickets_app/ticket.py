from dataclasses import dataclass


@dataclass
class Ticket:
    id: str
    title: str
    content: str
    userEmail: str
    creationTime: float  # unix timestamp
    labels: list
