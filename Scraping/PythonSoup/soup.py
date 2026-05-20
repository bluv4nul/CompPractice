import csv
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://atlas.herzen.spb.ru"
START_PAGE = 1
END_PAGE = 54
NOT_SPECIFIED = "Не указано"


def get_text_or_default(block):
    if not block:
        return NOT_SPECIFIED

    text = block.find("h1", class_="text-m")
    if not text:
        return NOT_SPECIFIED

    return text.get_text(strip=True) or NOT_SPECIFIED


def main():
    all_teachers = []
    session = requests.Session()

    for page in range(START_PAGE, END_PAGE + 1):
        url = f"{BASE_URL}/teachers?page={page}"
        response = session.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        teachers = soup.find_all("a", class_="text-blue-600")

        for teacher in teachers:
            name = teacher.get_text(strip=True)
            link = urljoin(BASE_URL, teacher.get("href"))

            response = session.get(link)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            teacher_info = soup.find("div", class_="flex flex-col p-4 px-2 lg:px-2")

            if teacher_info:
                phone_block = teacher_info.find(
                    "div",
                    class_="flex lg:space-x-2 items-center text-blue-400 py-1 lg:pl-2 rounded-lg cursor-pointer mb-1",
                )
                email_block = teacher_info.find(
                    "div",
                    class_="flex items-center text-blue-400 py-1 rounded-lg cursor-pointer mb-1",
                )
            else:
                phone_block = None
                email_block = None

            all_teachers.append(
                {
                    "name": name,
                    "email": get_text_or_default(email_block),
                    "phone": get_text_or_default(phone_block),
                    "link": link,
                }
            )

    with open("pythonsoup.csv", "w", encoding="utf-8-sig", newline="") as file:
        fieldnames = ["name", "email", "phone", "link"]
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")

        writer.writeheader()
        writer.writerows(all_teachers)


if __name__ == "__main__":
    main()
