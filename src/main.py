import asyncio

from dotenv import load_dotenv

from queries.getTournaments import get_tournaments


async def main():
    response = get_tournaments()

    queryComplexity = response['extensions']['queryComplexity']
    pageInfo = response['data']['tournaments']['pageInfo']
    tournaments = response['data']['tournaments']['nodes']

    print(f"{queryComplexity = }")
    print(f"{pageInfo = }")
    print(tournaments)


if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())
