import re

from models import ActivityState, EventDB

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


def should_skip_event(event: EventDB) -> bool:
    event_slug = event.slug.split('/')[-1]

    return (
        event.state != ActivityState.COMPLETED or
        any(re.search(pattern, event_slug) for pattern in BLACKLISTED_PATTERNS)
    )
