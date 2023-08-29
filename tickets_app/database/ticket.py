from dataclasses import dataclass

TICKET_TEXT_ATTRIBUTES = ['title', 'content', 'userEmail']


@dataclass
class Ticket:
    id: str
    title: str
    content: str
    userEmail: str
    creationTime: float  # unix timestamp
    labels: list
