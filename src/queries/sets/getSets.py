import os
from time import sleep
from typing import Generator, cast

import requests

from customTypes.startgg import (EventSet, StartggEventSetsResponse,
                                 SuccessEventSetsResponse)
from utils.constants import STARTGG_API_URL

from .setsQuery import SETS_QUERY


def get_event_sets(
    eventId: int,
    page: int,
) -> SuccessEventSetsResponse:
    STARTGG_TOKEN = os.getenv('STARTGG_TOKEN')

    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {STARTGG_TOKEN}",
    }

    BODY = {
        "query": SETS_QUERY,
        "variables": {
            "eventId": eventId,
            "perPage": 40,
            "page": page,
        }
    }

    retries = 3

    for attempt in range(retries):
        if attempt != 0:
            sleep(60)

        try:
            response: StartggEventSetsResponse = requests \
                .post(STARTGG_API_URL, json=BODY, headers=HEADERS) \
                .json()

            if (response.get('success') is False):
                raise Exception(response.get('message'))

            if (response.get('errors') is not None):
                raise Exception(response.get('errors', [])[0]['message'])

            return cast(SuccessEventSetsResponse, response)
        except Exception as e:
            print(f"Error with request. Retrying ({attempt+1}/{retries})...")
            print(f"> {e}")

    raise RuntimeError("Request failed")


def get_event_sets_iter(
    eventId: int,
) -> Generator[EventSet, None, None]:
    response = get_event_sets(eventId, 1)
    totalPages = response['data']['event']['sets']['pageInfo']['totalPages']

    for page in range(2, totalPages + 2):
        queryComplexity = response['extensions']['queryComplexity']
        pageInfo = response['data']['event']['sets']['pageInfo']
        sets = response['data']['event']['sets']['nodes']

        print(f"> Sets {pageInfo = } | {queryComplexity = }")

        for event_set in sets:
            yield event_set

        if (page != totalPages + 1):
            response = get_event_sets(eventId, page)
