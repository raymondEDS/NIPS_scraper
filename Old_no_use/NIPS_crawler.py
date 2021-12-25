#https://github.com/daines-analytics/web-scraping-projects/tree/master/py_webscraping_neurips_proceedings_2020
import numpy as np
import pandas as pd
import os
import sys
import shutil
from datetime import datetime
import requests
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from random import randint
from time import sleep

# Begin the timer for the script processing
startTimeScript = datetime.now()

# Set up the verbose and debug flags to print detailed messages for debugging (setting True will activate!)
verbose = True
debug = False

# Set up the executeDownload flag to download files (setting True will download!)
executeDownload = True

def access_url(url):
    # Creating an html document from the URL
    uastring = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
    headers={'User-Agent': uastring}
    # Adding random wait time so we do not hammer the website needlessly
    waitTime = randint(2,5)
    print("Waiting " + str(waitTime) + " seconds to retrieve the next URL.")
    sleep(waitTime)
    try:
        s = requests.Session()
        resp = s.get(url, headers=headers)
        if (debug): print(resp.text)
    except HTTPError as e:
        print('The server could not serve up the web page!')
        sys.exit("Script processing cannot continue!!!")
    except ConnectionError as e:
        print('The server could not be reached due to connection issues!')
        sys.exit("Script processing cannot continue!!!")

    if (resp.status_code==requests.codes.ok):
        print('Successfully accessed the web page: ' + url)
        bsoup_obj = BeautifulSoup(resp.text, 'lxml')
        return(bsoup_obj)

def download_to_local(doc_path):
    # Adding random wait time so we do not hammer the website needlessly
    waitTime = randint(2,5)
    print("Waiting " + str(waitTime) + " seconds to retrieve " + doc_path)
    sleep(waitTime)
    local_file = doc_path.split('/')[-1]
    if (os.path.isfile(local_file) == False):
        with requests.get(doc_path, stream=True) as r:
            with open(local_file, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        print('Downladed file:', local_file, '\n')
    else:
        print('Skipped existing file:', local_file, '\n')

# Specifying the URL of desired web page to be scrapped
starting_url = "https://proceedings.neurips.cc/paper/2017"
website_url = "https://proceedings.neurips.cc"
# Access and test the starting URL
web_page = access_url(starting_url)

# Gather all document links from the starting URL (Two Levels)
collection = web_page.find_all('li')

# Delete the first two `li` element as they are not the paper items we need
collection.pop(0)
collection.pop(0)

print('Number of items collected:', len(collection))

i = 0
for item in collection:
    if debug: print(item)
    doc_title = item.a.string
    authors = item.i.string
    doc_link = website_url + item.a['href']
    if verbose: print('Found abstract link at:', doc_link)
    if verbose: print('Found collaborating authors:', authors)

    doc_page = access_url(doc_link)
    artifact_list = doc_page.find_all('a', class_="btn")
    for artifact_item in artifact_list:
        if artifact_item.string == "Paper":
            doc_path = website_url + artifact_item['href']
            if verbose: print('Found paper at:', doc_path, '\n')
            if (executeDownload):
                download_to_local(doc_path)
    i = i + 1

print('Finished finding all available documents on the web pages!')
print('Number of abstracts processed:', i)