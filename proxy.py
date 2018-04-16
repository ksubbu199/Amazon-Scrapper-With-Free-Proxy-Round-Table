import requests
from bs4 import BeautifulSoup
from random import randint

def get_random_number():
    return randint(1,9)

def get_random_proxy():
    res = requests.get('https://free-proxy-list.net/', headers={'User-Agent':'Mozilla/5.0'})
    soup = BeautifulSoup(res.text,"lxml")
    c = get_random_number()
    i = 1
    for items in soup.select("tbody tr"):
        if i == c :
            random_proxy = ':'.join([item.text for item in items.select("td")[:2]])
            return random_proxy
        i = i + 1

def get_all_proxies():
    res = requests.get('https://free-proxy-list.net/', headers={'User-Agent':'Mozilla/5.0'})
    soup = BeautifulSoup(res.text,"lxml")
    proxies = []
    for items in soup.select("tbody tr"):
        proxy = ':'.join([item.text for item in items.select("td")[:2]])
        proxies.append(proxy)
    return proxies
