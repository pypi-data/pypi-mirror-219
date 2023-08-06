from typing import Any, Dict, Union, cast
import click
import requests
from typing import TypeVar
from urllib.parse import urljoin

T = TypeVar("T")


class GableClient:
    def __init__(self, endpoint: str, api_key: str) -> None:
        self.endpoint = endpoint
        self.api_key = api_key

        self.validate_api_key()
        self.validate_endpoint()

    def validate_api_key(self):
        if not self.api_key:
            raise click.ClickException(
                "API Key is not set. Use the --api-key argument or set GABLE_API_KEY "
                "environment variable."
            )

    def validate_endpoint(self):
        if not self.endpoint:
            raise click.ClickException(
                "API Endpoint is not set. Use the --endpoint or set GABLE_API_ENDPOINT "
                "environment variable."
            )

    def get(self, path: str, **kwargs: Any) -> tuple[dict[str, Any], bool, int]:
        return self._request(path, method="GET", **kwargs)

    def post(self, path: str, **kwargs: Any) -> tuple[dict[str, Any], bool, int]:
        return self._request(path, method="POST", **kwargs)

    def _request(
        self, path: str, method: str = "GET", **kwargs: Any
    ) -> tuple[dict[str, Any], bool, int]:
        url = urljoin(self.endpoint, path)
        headers = {"X-API-KEY": self.api_key}
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, **kwargs)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, **kwargs)
        else:
            raise click.ClickException("Invalid HTTP method: {method} not supported.")
        # Check for missing api key
        if response.status_code == 403:
            raise click.ClickException("Invalid API Key")
        return (
            cast(dict[str, Any], response.json()),
            response.status_code == 200,
            response.status_code,
        )
