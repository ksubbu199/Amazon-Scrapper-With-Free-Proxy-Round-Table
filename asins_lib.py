import requests
from bs4 import BeautifulSoup
from ua import uaLib
from proxy import get_random_proxy

def get_asin_from_url(url):
    url_split = url.split('/')
    dp_index = url_split.index('dp') if 'dp' in url_split else None
    if dp_index:
        return url_split[dp_index + 1][0:10]
    else:
        return None

def scrape_asins_from_url(url,ua,proxy):
    headers = {'User-Agent': ua}
    proxy = {'http': 'http://'+proxy}
    page = requests.get(url,headers=headers, proxies=proxy)
    html_content = page.text
    soup = BeautifulSoup(html_content, 'lxml')
    links = soup.find_all('a',href=True)
    asins = []
    for atag in links:
        link = atag.get('href')
        asin = get_asin_from_url(link)
        if asin:
            asins.append(asin)
    return asins

def scrape_asins_from_html(page):
    html_content = page.text
    soup = BeautifulSoup(html_content, 'lxml')
    links = soup.find_all('a',href=True)
    asins = []
    for atag in links:
        link = atag.get('href')
        asin = get_asin_from_url(link)
        if asin:
            asins.append(asin)
    return asins
