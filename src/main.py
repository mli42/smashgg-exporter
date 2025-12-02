import asyncio

from dotenv import load_dotenv

from customTypes.startgg import Event, Tournament
from queries.getTournaments import get_tournaments_iter
from utils.constants import STARTGG_BASE_URL
from utils.getDateTimestamp import get_date_timestamp
from utils.shouldSkipEvent import should_skip_event


def handle_event(event: Event):
    print(f"EVENT [{event['id']}] : {STARTGG_BASE_URL}/{event['slug']}")
    pass


def handle_tournament(tournament: Tournament):
    for event in tournament['events']:

        if should_skip_event(event):
            # event_slug = event['slug'].split('/')[-1]
            # print(f"SKIPPING EVENT : {event_slug} ({event['id']})")
            continue

        handle_event(event)


async def main():
    afterDate = get_date_timestamp("01/01/2025")
    beforeDate = get_date_timestamp("01/04/2025")

    for tournament in get_tournaments_iter(afterDate, beforeDate):
        handle_tournament(tournament)


if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())
