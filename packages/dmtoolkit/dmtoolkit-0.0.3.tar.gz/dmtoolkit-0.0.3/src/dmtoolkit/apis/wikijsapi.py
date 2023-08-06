import os

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from autonomous import log


class WikiJS:
    def __init__(self, endpoint=None, api_key=None):
        self.endpoint = os.environ.get("WIKIJS_URL", endpoint)
        self.api_key = os.environ.get("WIKIJS_TOKEN", api_key)
        headers = {"Authorization": f"Bearer {self.api_key}"}
        transport = RequestsHTTPTransport(url=self.endpoint, headers=headers)
        self.client = Client(transport=transport, fetch_schema_from_transport=True)

    def execute(self, query):
        log(query)
        try:
            return self.client.execute(gql(query))
        except Exception as e:
            raise Exception(e.message)
