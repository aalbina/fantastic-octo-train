import os
import uuid

import requests
from bs4 import BeautifulSoup


def _get_title(content: bytes) -> str:
    soup = BeautifulSoup(content, "html.parser")
    title = soup.find_all("title")

    if title:
        return title[0].text.replace("/", "").replace("\\", "")
    return uuid.uuid4().hex


def save_pages(links: list[str]):
    with requests.Session() as session:
        for link in links:
            response = session.get(link)

            file_name = os.path.join(os.getcwd(), "saved", f"{_get_title(response.content)}.html")
            with open(file_name, "wb") as file:
                file.write(response.content)


if __name__ == "__main__":
    links = [
        "https://habr.com/ru/articles/729844/",
        "https://habr.com/ru/articles/598107/",
        "https://habr.com/ru/articles/596317/",
    ]

    save_pages(links)
