import time

from resource_manager import RESOURCES


def check_resource(resource=None, retry=3, wait=5):
    def resource_decorator(func):
        def wrapper(self, *args, **kwargs):
            for _ in range(retry):
                if RESOURCES.get(resource):
                    return func(self, *args, **kwargs)
                time.sleep(wait)
            raise SystemExit(f'Resource {resource} is empty')
        return wrapper
    return resource_decorator
