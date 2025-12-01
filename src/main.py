import asyncio
import os
from time import sleep
from typing import cast

import requests
from dotenv import load_dotenv

from customTypes.startgg import StartggResponse, SuccessResponse
from queries.tournamentsQuery import TOURNAMENTS_QUERY, VARIABLES


def get_tournaments(url, json, headers) -> SuccessResponse:
    retries = 3

    for attempt in range(retries):
        if attempt != 0:
            sleep(3)

        try:
            response: StartggResponse = requests \
                .post(url, json=json, headers=headers) \
                .json()

            if (response.get('success') is False):
                raise Exception(response.get('message'))

            return cast(SuccessResponse, response)
        except Exception as e:
            print(f"Error with request. Retrying ({attempt+1}/{retries})...")
            print(f"> {e}")

    raise RuntimeError("Request failed after retries")


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

    queryComplexity = response['extensions']['queryComplexity']
    pageInfo = response['data']['tournaments']['pageInfo']
    tournaments = response['data']['tournaments']['nodes']

    print(f"{queryComplexity = }")
    print(f"{pageInfo = }")
    print(tournaments)


if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())
