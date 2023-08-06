from typing import Dict, Optional

import requests


class Productive:
    """
    @author: Paweł Karbowniczek <pawel.karbowniczek@cloudflight.io>
    Productive API client
    """

    URL: str = "https://api.productive.io/api/v2/"

    def __init__(
        self, url: Optional[str] = None, headers: Optional[Dict] = None
    ) -> None:
        self.url = self.URL
        if url is not None:
            self.url = url
        self.headers = headers

    def get(self, resource: str) -> Dict:
        """

        @param resource:
        @return:
        """
        response = requests.get(
            url=f"{self.url}{resource}", headers=self.headers
        )
        response.raise_for_status()
        data = response.json()["data"]
        if "meta" in response.json():
            if "current_page" and "total_pages" in response.json()["meta"]:
                current_page = response.json()["meta"]["current_page"]
                total_pages = response.json()["meta"]["total_pages"]
                i = current_page
                data = []
                while i <= total_pages:
                    response = requests.get(
                        url=f"{self.url}{resource}",
                        headers=self.headers,
                        params={"page[number]": str(i)},
                    )
                    response.raise_for_status()
                    data.extend(response.json()["data"])
                    i = i + 1
        return data

    def post(self, resource: str, json: Dict) -> Dict:
        """

        @param resource:
        @param json:
        @return:
        """
        url = f"{self.url}{resource}"
        response = requests.post(url=url, headers=self.headers, json=json)
        response.raise_for_status()
        return response.json()["data"]

    def patch(self, resource: str, json: Dict) -> Dict:
        """

        @param resource:
        @param json:
        @return:
        """
        url = f"{self.url}{resource}"
        response = requests.patch(url=url, headers=self.headers, json=json)
        response.raise_for_status()
        return response.json()["data"]

    def delete(self, resource: str) -> int:
        """

        @param resource:
        @return:
        """
        url = f"{self.url}{resource}"
        response = requests.delete(url=url, headers=self.headers)
        response.raise_for_status()
        return response.status_code
