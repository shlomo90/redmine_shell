import requests

from redminelib.engines.base import BaseEngine


class MySyncEngine(BaseEngine):
    @staticmethod
    def create_session(**params):
        session = requests.Session()
        session.verify = False
        requests.packages.urllib3.disable_warnings()

        for param in params:
            setattr(session, param, params[param])

        return session

    def process_bulk_request(self, method, url, container, bulk_params):
        return [resource
            for params in bulk_params
                for resource in self.request(
                    method, url, params=params)[container]]
