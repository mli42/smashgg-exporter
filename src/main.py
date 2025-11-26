import requests
from dotenv import load_dotenv
import os
from queries.tournamentsQuery import TOURNAMENTS_QUERY, VARIABLES
import asyncio
from json import loads


async def get_tournaments(url, json, headers) -> requests.Response:
    # print(json)
    try:
        response = requests.post(url, json=json, headers=headers)
    except BaseException:
        print("Error with request. Retrying")
        return await get_tournaments(url, json, headers)
    return response


async def main():
    STARTGG_TOKEN = os.getenv('STARTGG_TOKEN')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {STARTGG_TOKEN}",
    }

    url = "https://api.start.gg/gql/alpha"

    response = get_tournaments(
        url,
        json={
            "query": TOURNAMENTS_QUERY,
            "variables": VARIABLES
        },
        headers=headers)

    awaited = await response

    print(loads(awaited.text))


if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())
