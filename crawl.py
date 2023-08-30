import requests
import random

from bs4 import BeautifulSoup


def get_random_user_agent():
    with open('./user-agents.txt', 'r') as file:
        user_agents = file.readlines()
    index = random.randint(1, len(user_agents)-1)

    return (user_agents[index].replace('\n', ''))


def returnInternalLinks(targetDomain):

    targetDomain = 'https://' + \
        targetDomain if 'https://' not in targetDomain else targetDomain

    internal_links = []
    page = requests.get(targetDomain, headers={
                        'User-Agent': get_random_user_agent()}, timeout=10)
    soup = BeautifulSoup(page.content, "html.parser")

    if len(soup.findAll('a')) > 0:
        for link in soup.findAll('a'):
            href_link = link.get('href')

            if href_link and '#' not in href_link and 'mailto:' not in href_link:

                if href_link and href_link[0] == '/':
                    internal_links.append(targetDomain+href_link)
                elif href_link and targetDomain.replace('https://', '') in href_link.replace('wwww.', '').replace('https://', ''):
                    internal_links.append(href_link)

    return list(set(internal_links))
