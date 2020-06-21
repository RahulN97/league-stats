import functools
import json
import requests
import time

from constants import (
    API_KEY,
    URLS
)
from resource_manager import ResourceManager
from typing import Dict, Tuple


class Strategy:
    def __init__(self, summoner):
        self.summoner = summoner
        self.api_key = API_KEY
        self.acct_id = self.get_acct_id(summoner)
        self.resource_manager = ResourceManager()


    def execute(self):
        pass


    def write(self, strat_name, result):
        self.resource_manager.write_results(strat_name, result)


    def retry_requests(func, max_retries=3):
        def retry_decorator(self, *args, **kwargs):
            for _ in range(max_retries):
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    exception = e
            raise exception
        return retry_decorator


    @retry_requests
    def get(self, url, **kwargs) -> Tuple[Dict, int]:
        url = self.format_url(url, **kwargs)
        try:
            resp = requests.get(url=url)
            resp_data = json.loads(resp.text)
        except requests.exceptions.RequestException as e:
            raise SystemExit(f'Get request to {url} failed with error:\n{e}')
        except json.decoder.JSONDecodeError as e:
            raise SystemExit(f'Failed to decode resp data: {resp.text} with error:\n{e}')

        return resp_data, resp.status_code


    @retry_requests
    def post(self, url, post_data, **kwargs) -> Tuple[Dict, int]:
        url = self.format_url(url, **kwargs)
        try:
            resp = requests.post(url=url, data=json.dumps(post_data))
            resp_data = json.loads(resp.text)
        except requests.exceptions.RequestException as e:
            raise SystemExit(f'Post request to {url} failed with error:\n{e}')
        except json.decoder.JSONDecodeError as e:
            raise SystemExit(f'Failed to decode resp data: {resp.text} with error:\n{e}')

        return resp_data, resp.status_code


    def format_url(self, url, **kwargs):
        return url.format(API_KEY=API_KEY, **kwargs)


    def get_acct_id(self, summoner):
        resp_data, _ = self.get(URLS['summoner_dto'], summoner=self.summoner)
        return resp_data['accountId']
