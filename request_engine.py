import json
import requests

from constants import API_KEY
from typing import (
    Dict,
    Tuple
)


class RequestEngine:
    def __init__(self):
        self.api_key = API_KEY


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
            raise SystemExit(f'Fetching from {url} failed with error:\n{e}')
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
            raise SystemExit(f'Posting to {url} failed with error:\n{e}')
        except json.decoder.JSONDecodeError as e:
            raise SystemExit(f'Failed to decode resp data: {resp.text} with error:\n{e}')

        return resp_data, resp.status_code


    def format_url(self, url, **kwargs):
        return url.format(API_KEY=self.api_key, **kwargs)
