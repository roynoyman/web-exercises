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

    # def is_filtered_ticket(self, filters):
    #     text_filters = extract_text_filters_from_filters(filters)
    #     timestamp_filters = extract_timestamp_filters_from_filters(filters)
    #     is_text_filter = is_text_filtered(text_filters, ticket) if text_filters else True
    #     is_timestamp_filter = is_timestamp_filtered(timestamp_filters, ticket) if timestamp_filters else True
    #     return is_text_filter and is_timestamp_filter

