import base64
import os
import logging
import json
import requests
from dotenv import load_dotenv
import click

load_dotenv()


class PocketHandler:
    def get_urls_titles(self):
        request_token = self.get_request_token()
        urls, titles = [], []
        content = self.fetch_content(os.getenv("POCKET_ACCESS_TOKEN"))
        if not isinstance(content, dict):
            return urls, titles
        for key, item in content.items():
            urls.append(item["resolved_url"])
            titles.append(item["given_title"])
        return urls, titles

    def get_request_token(self):
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

    def get_access_token(self, request_token: str):
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

    def fetch_content(self, access_token: str) -> dict:
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
    
    def authenticate(self, request_token) -> str:
        print(f"""
            Go to: https://getpocket.com/auth/authorize?request_token={request_token}&redirect_uri=http://www.google.com"
        """)
        wait_for_response = input("Enter if visited")
        access_token = self.get_access_token(request_token)
        print(access_token)
        return access_token
