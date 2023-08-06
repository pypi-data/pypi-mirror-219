import httpx
from httpx import Timeout

from stigg.generated.async_client import AsyncClient
from stigg.generated.client import Client

PRODUCTION_API_URL = "https://api.stigg.io/graphql"

DEFAULT_REQUEST_TIMEOUT = Timeout(timeout=30.0)

HTTP_TRANSPORT_RETRY_COUNT = 5


class StiggClient(Client):
    pass


class AsyncStiggClient(AsyncClient):
    pass


def get_headers(api_key: str):
    return {"X-API-KEY": api_key, "Content-Type": "application/json"}


class Stigg:
    @staticmethod
    def create_client(api_key: str, api_url: str = PRODUCTION_API_URL) -> StiggClient:
        headers = get_headers(api_key)
        transport = httpx.HTTPTransport(retries=HTTP_TRANSPORT_RETRY_COUNT)
        http_client = httpx.Client(
            headers=headers,
            timeout=DEFAULT_REQUEST_TIMEOUT,
            transport=transport
        )
        return StiggClient(
            url=api_url,
            headers=headers,
            http_client=http_client,
        )

    @staticmethod
    def create_async_client(
            api_key: str, api_url: str = PRODUCTION_API_URL
    ) -> AsyncStiggClient:
        headers = get_headers(api_key)
        transport = httpx.AsyncHTTPTransport(retries=HTTP_TRANSPORT_RETRY_COUNT)
        http_client = httpx.AsyncClient(
            headers=headers,
            timeout=DEFAULT_REQUEST_TIMEOUT,
            transport=transport
        )
        return AsyncStiggClient(
            url=api_url,
            headers=headers,
            http_client=http_client,
        )
