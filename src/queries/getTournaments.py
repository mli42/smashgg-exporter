import os
from time import sleep
from typing import cast

import requests

from customTypes.startgg import StartggResponse, SuccessResponse

from .tournamentsQuery import TOURNAMENTS_QUERY

STARTGG_URL = "https://api.start.gg/gql/alpha"


def get_tournaments(afterDate: int, beforeDate: int) -> SuccessResponse:
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
        }
    }

    retries = 3

    for attempt in range(retries):
        if attempt != 0:
            sleep(3)

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
