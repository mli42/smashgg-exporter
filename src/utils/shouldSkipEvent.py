import re

from customTypes.startgg import Event

BLACKLISTED_PATTERNS = [
    r'side-event',
    r'attente',
    r'melt-chill',
    r'double',
    r'ladder',
    r'cpu',
    r'random',
    r'squadstrike',
    r'squad-strike',
    r'squads',
    r'amiibo',
]


def should_skip_event(event: Event) -> bool:
    event_slug = event['slug'].split('/')[-1]

    return (
        event['state'] != 'COMPLETED' or
        any(re.search(pattern, event_slug) for pattern in BLACKLISTED_PATTERNS)
    )
