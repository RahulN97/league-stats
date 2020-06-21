import json
import requests

from constants import (
    API_KEY,
    ROOT_SUMMONER,
    URLS
)
from copy import deepcopy
from enum import Enum
from request_engine import RequestEngine
from threading import Lock


# Read-Only Shared Resources
RESOURCES = {
    'champion_cache': None,
    'match_history': None
}

# Thread-Safe Shared Resource
results_lock = Lock()
RESULTS = {}


class FetchStatus(Enum):
    SUCCESS = 1
    FAIL = 2
    NONE = 3


class ResourceManager:
    def __init__(self, args=None):
        self.statuses = {}
        self.root_summoner = args.user if args else ROOT_SUMMONER
        self.size = args.size if args else 100
        self.request_engine = RequestEngine()


    def _init_champion_cache(self) -> FetchStatus:
        if RESOURCES['champion_cache']:
            return FetchStatus.NONE

        resp_data, status = self.request_engine.get(URLS['champions'])

        RESOURCES['champion_cache'] = {}
        for champion,data in resp_data['data'].items():
            RESOURCES['champion_cache'][data['key']] = data

        return FetchStatus.SUCCESS if status == 200 else FetchStatus.FAIL


    def _init_match_history(self) -> FetchStatus:
        if RESOURCES['match_history']:
            return FetchStatus.NONE

        summ_resp, _ = self.request_engine.get(
            URLS['summoner_dto'], summoner=self.root_summoner
        )

        RESOURCES['match_history'] = []
        resp_statuses = []
        for i in range(0, self.size, 100):
            begin_index = i
            end_index = min(i+100, self.size)

            match_resp, status = self.request_engine.get(
                URLS['match_history'],
                acct_id=summ_resp['accountId'],
                begin_index=begin_index,
                end_index=end_index
            )
            RESOURCES['match_history'].extend(match_resp['matches'])
            resp_statuses.append(status)

        return FetchStatus.SUCCESS if all(s == 200 for s in resp_statuses) else FetchStatus.FAIL


    def init_all_resources(self):
        self.statuses = {
            resource_name: getattr(self, f'_init_{resource_name}')()
            for resource_name in list(RESOURCES.keys())
        }


    def read_results(self, key=None):
        with results_lock:
            if key:
                return RESULTS.get(key)
            return deepcopy(RESULTS)


    def write_results(self, key, result):
        with results_lock:
            RESULTS[key] = result
