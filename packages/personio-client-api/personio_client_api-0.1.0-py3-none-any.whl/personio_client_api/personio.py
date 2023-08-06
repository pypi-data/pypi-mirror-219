import logging
from typing import Dict, Optional

import requests

from personio_client_api.exceptions import PersonioClient


class Personio:
    URL: str = "https://api.personio.de/v1/"

    def __init__(
        self, client_id: str, client_secret: str, url: Optional[str] = None
    ) -> None:
        self.url = self.URL
        if url is not None:
            self.url = url
        self.client_id = client_id
        self.client_secret = client_secret
        try:
            self.token = self.get_token()
        except requests.exceptions.HTTPError as exc:
            logging.exception(exc)
            self.token = None

    def get_token(self) -> str:
        querystring = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        headers = {"Accept": "application/json"}

        response = requests.request(
            "POST", url=f"{self.URL}auth", headers=headers, params=querystring
        )
        response.raise_for_status()
        return response.json()["data"]["token"]

    def get(self, resource: str) -> Dict:
        if self.token is None:
            self.token = self.get_token()
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }
        try:
            response = requests.get(
                url=f"{self.URL}{resource}", headers=headers
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise PersonioClient from exc
        self.token = response.headers["authorization"].split(" ")[1]
        return response.json()["data"]
