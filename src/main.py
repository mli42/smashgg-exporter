import asyncio

from dotenv import load_dotenv

from getDateTimestamp import get_date_timestamp
from queries.getTournaments import get_tournaments


async def main():
    afterDate = get_date_timestamp("01/01/2025")
    beforeDate = get_date_timestamp("01/04/2025")
    response = get_tournaments(afterDate, beforeDate)

    queryComplexity = response['extensions']['queryComplexity']
    pageInfo = response['data']['tournaments']['pageInfo']
    tournaments = response['data']['tournaments']['nodes']

    print(f"{queryComplexity = }")
    print(f"{pageInfo = }")
    print(tournaments)


if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())
