import os
from typing import Optional
from requests import Session, RequestException

from .exceptions import ApiException

class Api:
    def __init__(
        self,
        api_user_id: Optional[str] = None,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
    ):
        self.test_name = None
        self.api_user_id = api_user_id or os.environ.get("CARBONATE_USER_ID")
        self.api_key = api_key or os.environ.get("CARBONATE_API_KEY")
        self.api_url = api_url or "https://api.carbonate.dev/"
        self.client = Session()

        if not self.api_user_id:
            raise ValueError(
                "No user ID provided, please either pass in api_user_id to the constructor or set the CARBONATE_USER_ID environment variable"
            )

        if not self.api_key:
            raise ValueError(
                "No API key provided, please either pass in api_key to the constructor or set the CARBONATE_API_KEY environment variable"
            )

    def set_test(self, test):
        self.test_name = test

    def call_api(self, url: str, data: dict):
        if not data['test_name']:
            raise ValueError(
                "No test name provided, please use the @carbonate.test() annotation or call start_test() with your test name"
            )

        try:
            response = self.client.post(
                self.api_url + url,
                headers={"X-Api-User-Id": self.api_user_id, "X-Api-Key": self.api_key},
                json=data,
                timeout=60,
            )
        except RequestException as e:
            raise ApiException(f"Call to {url} failed with exception {e}")

        if response.status_code == 200:
            json = response.json()

            return json
        else:
            raise ApiException(
                f"Call to {url} failed with status code {response.status_code}, body: {response.content.decode('utf-8')}"
            )

    def extract_actions(self, test_name: str, instruction: str, html: str) -> list:
        actions = self.call_api("actions/extract", {
            "test_name": test_name,
            "story": instruction,
            "html": html,
        })

        if actions is None:
            return []

        return actions["actions"]

    def extract_assertions(self, test_name: str, instruction: str, html: str) -> list:
        assertion = self.call_api("assertions/extract", {
            "test_name": test_name,
            "story": instruction,
            "html": html,
        })

        if assertion is None:
            return []

        return assertion["assertions"]

    def extract_lookup(self, test_name: str, instruction: str, html: str) -> Optional[dict]:
        lookup = self.call_api("lookup/extract", {
            "test_name": test_name,
            "story": instruction,
            "html": html,
        })

        return lookup
