import random
from html_similarity import similarity


class detector():

    def __init__(self, soup):
        self.soup = soup

    def iis10_check(self):
        with open('./pages_html/IIS10.html', 'r') as f:
            file = f.read()

        return round(similarity(file, str(self.soup)) * 100, 2)

    def iis7_check(self):
        with open('./pages_html/IIS7.html', 'r') as f:
            file = f.read()

        return round(similarity(file, str(self.soup)) * 100, 2)

    def lorem_ipsum_check(self):
        return "Lorem ipsum dolor sit amet" in " ".join(list(filter(None, self.soup.get_text().split("\n"))))

    def nginx_default(self):
        with open('./pages_html/nginx.html', 'r') as f:
            file = f.read()

        return round(similarity(file, str(self.soup)) * 100, 2)

    def apache_default(self):
        with open('./pages_html/apache.html', 'r') as f:
            file = f.read()

        return round(similarity(file, str(self.soup)) * 100, 2)
