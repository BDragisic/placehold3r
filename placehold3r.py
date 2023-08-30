import requests
import random
import random
import argparse

from termcolor import colored
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from detector import detector
from crawl import returnInternalLinks


def parse_args():
    parser = argparse.ArgumentParser(
        prog="placehold3r",
        description="A script to detect any forgotten about default pages hosted on a website.",
        epilog="Developed by github.com/BDragisic.",
    )

    parser.add_argument(
        "-d", "--domain", help="Specify a single domain to scan")

    return parser.parse_args()


if __name__ == '__main__':

    # Parse arguments
    args = parse_args()

    # ASCII Art
    print(f'''
          _                         _               _       _   ____         
         | |                       | |             | |     | | |___ \        
  _ __   | |   __ _    ___    ___  | |__     ___   | |   __| |   __) |  _ __ 
 | '_ \  | |  / _` |  / __|  / _ \ | '_ \   / _ \  | |  / _` |  |__ <  | '__|
 | |_) | | | | (_| | | (__  |  __/ | | | | | (_) | | | | (_| |  ___) | | |   
 | .__/  |_|  \__,_|  \___|  \___| |_| |_|  \___/  |_|  \__,_| |____/  |_|   
 | |                                                                         
 |_|      
                                                                    
Target: {args.domain}
                                                                            
''')

    # Internal links scraped from the target
    internalLinks = returnInternalLinks(args.domain)

    if len(internalLinks) == 0:
        print(f'[ERROR] No internal links found.', 'red')
        exit(1)
    print(
        colored(f'[INFO] Found {len(internalLinks)} internal links. Checking each for default pages', 'blue'))

    for link in internalLinks:
        parseLink = urlparse(link).path
        print(f'[INFO] Checking {parseLink}', end='\r')
