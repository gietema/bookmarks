"""Class to connect to pocket and get items from pocket"""
import base64
import os
import logging
import json
import requests
from typing import Tuple, List, Dict
from dotenv import load_dotenv
import click

load_dotenv()

@click.command()
def main():
    """Run to get the Pocket access token"""
    access_token = PocketHandler().authenticate()
    print(access_token)


class PocketHandler:
    def get_urls_titles(self) -> Tuple[List[str], List[str]]:
        """
        Get the urls and titles of the most recent links in Pocket

        Returns
        -------
        urls, titles: Tuple[List[str], List[str]]
            Lists of urls and titles
        """
        request_token = self.get_request_token()
        urls, titles = [], []
        content = self.fetch_content(os.getenv("POCKET_ACCESS_TOKEN"))
        if not isinstance(content, dict):
            return urls, titles
        for key, item in content.items():
            urls.append(item["resolved_url"])
            title = item["given_title"]
            if len(title) < 3:
                title = item["resolved_title"]
            titles.append(title)
        return urls, titles

    def get_request_token(self) -> str:
        """
        Gets request token from pocket
        """
        response = requests.post(
            "https://getpocket.com/v3/oauth/request",
            data={
                "consumer_key": os.getenv("POCKET_CONSUMER_KEY"),
                "redirect_uri": "/",
            },
        )
        response = response.content.decode()
        assert response[:5] == "code="
        return response[5:]

    def fetch_content(self, access_token: str) -> Dict[str, str]:
        """
        Fetches content from pocket

        Parameters
        ----------
        access_token: str
            The access token to get access to pocket

        Returns
        -------
        items: Dict[str, str]
            Dict with items added to pocket
        """
        response = requests.post(
            "https://getpocket.com/v3/get",
            data={
                "consumer_key": os.getenv("POCKET_CONSUMER_KEY"),
                "access_token": access_token,
                "count": 5,
                "tag": "public",
            },
        )
        return response.json()["list"]

    def authenticate(self) -> str:
        """
        Used to authenticate the user.

        Returns
        -------
        access_token: str
            The access token
        
        Notes
        -----
        Access tokens do not expire in pocket, so this only needs to be done once. 
        If you're just using this app for your own purposes, just call this locally and store the access token
        """
        request_token = self.get_request_token()
        print(
            f"""
            Go to: https://getpocket.com/auth/authorize?request_token={request_token}&redirect_uri=http://www.google.com"
        """
        )
        wait_for_response = input("Enter if visited")
        access_token = self.get_access_token(request_token)
        return access_token

    def get_access_token(self, request_token: str) -> str:
        """
        Gets access token from pocket

        Parameters
        ----------
        request_token: str
            The request token
        """
        response = requests.post(
            "https://getpocket.com/v3/oauth/authorize",
            data={
                "consumer_key": os.getenv("POCKET_CONSUMER_KEY"),
                "code": request_token,
            },
        )
        response = response.content.decode()
        assert response[:13] == "access_token="
        return response[13:].split("&")[0]


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    main()  # pylint: disable=no-value-for-parameter
