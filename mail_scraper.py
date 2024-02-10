import argparse
import re
import requests
import sys
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Scrapes website for emails.')

parser.add_argument('url', type=str, help='target url, ex. "www.test.com"')
parser.add_argument('-o','--output', metavar='"filename"', help='save output to file')
args = parser.parse_args()
#To expand this tool we could scrape for internal links and recursivly scrape them
URL = sys.argv[1]
page = requests.get(URL)

soup = BeautifulSoup(page.content, "lxml")
text = soup.get_text()
results = re.findall(r'[a-zA-Z0–9._%+-]+@[a-zA-Z0–9.-]+\.[a-zA-Z]{2,}', text)
for i in results:
    print(i)

#Om -o, skriv results till argv
