import functools
import json
import requests
import time

from constants import (
    API_KEY,
    URLS
)
from request_engine import RequestEngine
from resource_manager import ResourceManager
from typing import (
    Dict,
    Tuple
)


class Strategy:
    def __init__(self, summoner):
        self.summoner = summoner
        self.api_key = API_KEY
        self.request_engine = RequestEngine()
        self.resource_manager = ResourceManager()
        self.acct_id = self.get_acct_id(summoner)


    def execute(self):
        pass


    def write(self, strat_name, result):
        self.resource_manager.write_results(strat_name, result)


    def get(self, url, **kwargs) -> Tuple[Dict, int]:
        return self.request_engine.get(url, **kwargs)


    def post(self, url, data, **kwargs) -> Tuple[Dict, int]:
        return self.request_engine.post(url, data, **kwargs)


    def get_acct_id(self, summoner):
        resp_data, _ = self.get(URLS['summoner_dto'], summoner=self.summoner)
        return resp_data['accountId']
