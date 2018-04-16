import json
from time import sleep
from amazon import *
from ua import uaLib
from proxy import *
from datetime import datetime
import logging
import pickle
import sched
from time import sleep
from random import randint
import threading

logging.basicConfig(filename='log.txt',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

Asins = {}
WaitingAsins = []
Proxies = []
BannedProxies = []
def merge_asins(new_asins):
    for asin in new_asins:
        #check_waiting = WaitingAsins.index(asin) if asin in WaitingAsins else None
        if asin not in Asins and asin not in WaitingAsins:
            WaitingAsins.append(asin)
        #else:
        #    logging.info("fucked up with "+ asin)

def get_proxy_from_cache():
    if len(Proxies) == 0:
        update_proxies()
    i = randint(0,len(Proxies))
    return Proxies[i-1]

def scrape_with_pid(pid):
    WaitingAsins.remove(pid)
    Asins[pid] = {}
    ua = uaLib.random()
    proxy = get_proxy_from_cache()
    logging.info("Scrapping p:"+pid+" proxy:"+proxy)
    ( data, new_asins) = AmazonParser(pid,ua,proxy)
    if not data and not new_asins:
        logging.info("Failed! Proxy failed to connect proxy:"+proxy)
        WaitingAsins.append(pid)
        Asins.pop(pid,None)
        Proxies.remove(proxy)
        BannedProxies.append(proxy)
        return

    if data:
        logging.info("success! p:"+pid+" proxy:"+proxy+" data:"+json.dumps(data))
        Asins[pid]['data']=data
    else:
        logging.info("Failed! p:"+pid+" proxy:"+proxy)
        Asins[pid]['data']= -1
        Proxies.remove(proxy)
        BannedProxies.append(proxy)

    if new_asins:
        #logging.info("new assins:" + json.dumps(new_asins))
        logging.info("Got "+str(len(new_asins))+" new asins! from "+ pid +" merging ")
        merge_asins(new_asins)
        #logging.info("all asins:"+json.dumps(WaitingAsins))
    else:
        logging.info("Failed! to get new asins! from "+ pid +" ignoring")

def merge_new_proxies(new_proxies):
    for proxy in new_proxies:
        if proxy not in Proxies and proxy not in BannedProxies:
            Proxies.append(proxy)

def update_proxies():
    new_proxies = get_all_proxies()
    merge_new_proxies(new_proxies)
    threading.Timer(60.0, update_proxies).start()

def infinite_scrapping():
    while True:
        if len(WaitingAsins) > 0:
            scrape_with_pid(WaitingAsins[0])
        else:
            logging.info("Queue is empty! Waiting")
            sleep(1)

def backup_data():
    with open('asins.pkl', 'wb') as fp:
        pickle.dump(Asins, fp)
    fp.close()
    with open('waiting.pkl', 'wb') as fp:
        pickle.dump(WaitingAsins, fp)
    fp.close()
    with open('proxies.pkl', 'wb') as fp:
        pickle.dump(Proxies, fp)
    fp.close()
    threading.Timer(60.0, backup_data).start()


update_proxies()
backup_data()
start_asin = 'B073ZG89XM'
WaitingAsins.append(start_asin)
scrape_with_pid(start_asin)
scrapping_thread = threading.Thread(target=infinite_scrapping,args=())
scrapping_thread.start()
scrapping_thread.join()
