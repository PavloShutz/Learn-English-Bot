import aiohttp
from bs4 import BeautifulSoup
import re


async def collect_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            return html


async def main():
    main_link = 'https://www.englishclub.com'
    html = await collect_data(f"{main_link}/grammar/")
    soup = BeautifulSoup(html, 'lxml')
    all_links = soup.find('main').findAll('li')
    items = []
    for li in all_links:
        for i in li.find_all('a'):
            not_formatted_link = i.get('href')
            if not re.match(r"^https://", not_formatted_link):
                if re.match(r"^(/esl-games/|/esl-quizzes/|/esl-forums/).", not_formatted_link):
                    link = f'{main_link}/{not_formatted_link}'
                else:
                    link = f'{main_link}/grammar/{not_formatted_link}'
            else:
                link = not_formatted_link
            items.append({'link': link, 'text': i.text})
    return items
