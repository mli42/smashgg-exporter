import os
from time import sleep
from typing import Generator, cast

import requests

from customTypes.startgg import StartggResponse, SuccessResponse, Tournament

from .tournamentsQuery import TOURNAMENTS_QUERY

STARTGG_URL = "https://api.start.gg/gql/alpha"


def get_tournaments(
    afterDate: int,
    beforeDate: int,
    page: int,
) -> SuccessResponse:
    STARTGG_TOKEN = os.getenv('STARTGG_TOKEN')

    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {STARTGG_TOKEN}",
    }

    BODY = {
        "query": TOURNAMENTS_QUERY,
        "variables": {
            "afterDate": afterDate,
            "beforeDate": beforeDate,
            "countryCode": "FR",
            "addrState": "IDF",
            "perPage": 5,
            "page": page,
        }
    }

    retries = 3

    for attempt in range(retries):
        if attempt != 0:
            sleep(2)

        try:
            response: StartggResponse = requests \
                .post(STARTGG_URL, json=BODY, headers=HEADERS) \
                .json()

            if (response.get('success') is False):
                raise Exception(response.get('message'))

            if (response.get('errors') is not None):
                raise Exception(response.get('errors', [])[0]['message'])

            return cast(SuccessResponse, response)
        except Exception as e:
            print(f"Error with request. Retrying ({attempt+1}/{retries})...")
            print(f"> {e}")

    raise RuntimeError("Request failed after retries")


def get_tournaments_iter(
    afterDate: int,
    beforeDate: int,
) -> Generator[Tournament, None, None]:
    response = get_tournaments(afterDate, beforeDate, 1)
    totalPages = response['data']['tournaments']['pageInfo']['totalPages']

    for page in range(2, totalPages + 2):
        pageInfo = response['data']['tournaments']['pageInfo']
        tournaments = response['data']['tournaments']['nodes']

        print(f"{pageInfo = }")

        for tournament in tournaments:
            yield tournament

        if (page != totalPages + 1):
            response = get_tournaments(afterDate, beforeDate, page)
