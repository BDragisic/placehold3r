import os
from bs4 import BeautifulSoup
import requests
import random
import sys
from termcolor import colored
import urllib3
from urllib.parse import urlparse
import httplib2
import random
from html_similarity import style_similarity, structural_similarity, similarity


def get_random_user_agent():
    with open('./user-agents.txt', 'r') as file:
        user_agents = file.readlines()
    index = random.randint(1, len(user_agents)-1)

    return (user_agents[index].replace('\n', ''))


def iis10_check(soup):
    with open('./pages_html/IIS10.html', 'r') as f:
        file = f.read()

    return round(similarity(file, str(soup)) * 100, 2)


def iis7_check(soup):
    with open('./pages_html/IIS7.html', 'r') as f:
        file = f.read()

    return round(similarity(file, str(soup)) * 100, 2)


def lorem_ipsum_check(soup):
    return "Lorem ipsum dolor sit amet" in " ".join(list(filter(None, soup.get_text().split("\n"))))


def nginx_default(soup):
    with open('./pages_html/nginx.html', 'r') as f:
        file = f.read()

    return round(similarity(file, str(soup)) * 100, 2)


def apache_default(soup):
    with open('./pages_html/apache.html', 'r') as f:
        file = f.read()

    return round(similarity(file, str(soup)) * 100, 2)


def default_pages_main(target_domain):
    print('Scraping site....')
    # For now just pulls every link present on home page, no recursion yet

    internal_links = []
    page = requests.get(target_domain, headers={
                        'User-Agent': get_random_user_agent()}, timeout=10)
    soup = BeautifulSoup(page.content, "html.parser")

    if len(soup.findAll('a')) > 0:
        for link in soup.findAll('a'):
            href_link = link.get('href')
            if href_link != None:
                if target_domain in href_link.replace('www.', ''):
                    if href_link[0] == "/":
                        href_link = target_domain+href_link

                    if href_link != None and '#' not in href_link:
                        internal_links.append(href_link)

    return internal_links


uInput = 'https://'+sys.argv[1]
internal_links = default_pages_main(uInput)

print(colored(f"Starting default page check on {sys.argv[1]}", "green"))
if len(internal_links) == 0:
    internal_links.append(uInput)


for link in internal_links:
    print(colored(f"\n[*] Checking path: {urlparse(link).path}", 'blue'))

    # Only make 1 request per link and send the soup object itself into each function to reduce load sent to server
    soup = BeautifulSoup(requests.get(link, headers={
                         'User-Agent': get_random_user_agent()}, timeout=10).content, "html.parser")

    lorem_present = lorem_ipsum_check(soup)
    if lorem_present:
        print(colored("    [*] Lorem Ipsum Detected", 'red'))
    else:
        print(colored("    [*] No Lorem Ipsum Present", 'green'))

    nginx_score = nginx_default(soup)
    if nginx_score > 30:
        print(
            colored(f"    [*] Similar score to nginx Default Page: {nginx_score}%", 'red'))
    else:
        print(colored(
            f"    [*] Similar score to nginx Default Page: {nginx_score}%", 'green'))

    apache_score = apache_default(soup)
    if apache_score > 30:
        print(colored(
            f"    [*] Similar score to apache Default Page: {apache_score}%", 'red'))
    else:
        print(colored(
            f"    [*] Similar score to apache Default Page: {apache_score}%", 'green'))

    iis10 = iis10_check(soup)
    if iis10 > 30:
        print(colored(
            f"    [*] Similar score to IIS10 Default Page: {iis10}%", 'red'))
    else:
        print(colored(
            f"    [*] Similar score to IIS10 Default Page: {iis10}%", 'green'))

    iis7 = iis7_check(soup)
    if iis7 > 30:
        print(colored(
            f"    [*] Similar score to IIS7 Default Page: {iis7}%", 'red'))
    else:
        print(colored(
            f"    [*] Similar score to IIS7 Default Page: {iis7}%", 'green'))
