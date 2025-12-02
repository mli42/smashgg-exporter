import asyncio

from dotenv import load_dotenv

from getDateTimestamp import get_date_timestamp
from queries.getTournaments import get_tournaments_iter


async def main():
    afterDate = get_date_timestamp("01/01/2025")
    beforeDate = get_date_timestamp("01/04/2025")

    tournaments = []
    for tournament in get_tournaments_iter(afterDate, beforeDate):
        tournaments.append(tournament)


if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())
