import asyncio

from dotenv import load_dotenv

from customTypes.startgg import Tournament
from getDateTimestamp import get_date_timestamp
from queries.getTournaments import get_tournaments_iter
from utils.skipEvent import skipEvent


def handle_tournament(tournament: Tournament):
    for event in tournament['events']:
        event_slug = event['slug'].split('/')[-1]

        if skipEvent(event):
            # print(f"SKIPPING EVENT : {event_slug} ({event['id']})")
            continue

        print(event_slug)


async def main():
    afterDate = get_date_timestamp("01/01/2025")
    beforeDate = get_date_timestamp("01/04/2025")

    for tournament in get_tournaments_iter(afterDate, beforeDate):
        handle_tournament(tournament)


if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())
