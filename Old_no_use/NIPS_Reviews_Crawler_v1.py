import numpy as np
import pandas as pd
import os
import sys
import shutil
import csv
import re
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

def access_url(url):
    #credit goes to https://github.com/daines-analytics/web-scraping-projects/tree/master/py_webscraping_neurips_proceedings_2020
    # Creating an html document from the URL
    uastring = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
    headers={'User-Agent': uastring}
    # Adding random wait time so we do not hammer the website needlessly
    waitTime = randint(1,3)
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



def reviews_hash_link(webpage):
#this is a more complete solution but it requires inputing additional variable of base website
#you will need to pair this with a base url
   hash_href_url = webpage.find('a', class_='btn btn-light btn-spacer',text='Reviews').get('href')
   return hash_href_url



def reviews_url(url_str):
    reviews_url = url_str.replace("Abstract","Reviews")
    reviews_url = reviews_url.replace("hash","file")
    return(reviews_url)


def reviewer_comments_post2017(webpage):
    #returns reviewer number and comment in a list
    #only works for 2017 onwards so far
    paper_reviews = []
    i = 0
    for i in range(len(webpage.find_all('h3'))):
        reviewers = webpage.find_all('h3')
        comments = webpage.find_all('div')
        paper_reviews.append([reviewers[i].text,comments[i].text])
        i += 1
    return(paper_reviews)

def reviewer_comments_pre2016(webpage):
    #returns reviewer number and comment in a list, this is for reviews before 2016
    paper_reviews = []
    i = 0
    for i in range(len(webpage.find_all('div',{"class":"response"}))):
        comments = webpage.find_all('div',{"class":"response"})
        
        #must have the reviewer + i + 1 or else reviewer_comments_csv() will break
        paper_reviews.append(['reviewer '+ str(i+1),comments[i].text]) # replace with paper_reviews.append({'reviewer '+ str(i+1):comments[i].text})
        #paper_reviews.append({'reviewer '+ str(i+1):comments[i].text})
        i += 1
    return(paper_reviews)

def reviewer_comments_2016(webpage):
    #returns reviewer number and comment in a list for 2016
    #todo
    return(True)

def create_nips_abstract_link_csv(bsoup_processed_file,nips_year,website_url):
    #creates CSV of author,paper title, abstract link
    file_name = "nips_paper_links_" + nips_year +'.csv'
    file_exist = os.path.exists(file_name)

    if file_exist:
        print ('Remove the ' + file_name +' in the directory')
        exit()
    else:
        #create cvs for all abstract links for conference
        file = open(file_name,'w')
        writer = csv.writer(file)

        #write into csv file
        for item in bsoup_processed_file:
            doc_title = item.a.string
            authors = item.i.string
            doc_link = website_url + item.a['href']
            #print('Found abstract link at:', doc_link)
            #print('Found collaborating authors:', authors)
            writer.writerow([doc_title,authors,doc_link])
        file.close()


def reviewer_comments_csv(links_csv,output_csv):
    #creates final csv with reviews
    #to do make sure i have the nips year set up
    #the assumption is that there is a max of 3 reviewers, i need to test to see if that is the case
    nips_papers = csv.reader(open(links_csv))
    file = open(output_csv,'w')
    writer = csv.writer(file)

    for paper_link in nips_papers:
        #there is a better way of doing this I dont know how yet
        #gets reviews for each paper in file
        reviews_out = reviewer_comments_post2017(access_url(reviews_url(paper_link[2])))
        if len(reviews_out) == 3:
            writer.writerow([paper_link[0],paper_link[1],paper_link[2],reviews_out[0][1],reviews_out[1][1],reviews_out[2][1]])
        elif len(reviews_out) == 2:
            writer.writerow([paper_link[0],paper_link[1],paper_link[2],reviews_out[0][1],reviews_out[1][1]])
        elif len(reviews_out) == 1:
            writer.writerow([paper_link[0],paper_link[1],paper_link[2][1],reviews_out[0][1]])
        elif len(reviews_out) == 1:
            writer.writerow([paper_link[0],paper_link[1],paper_link[2],'No Reviews'])


def run_script():
    #run script when ready
    #Specifying the URL of desired web page to be scrapped
    website_url = "https://proceedings.neurips.cc"
    nips_year = '2021'
    starting_url = "https://proceedings.neurips.cc/paper/" + nips_year
    file_name = "nips_paper_links_" + nips_year +'.csv'
    reviewer_comments_output = "nips_paper_reviews_" + nips_year +'.csv'
    # Access and test the starting URL
    web_page = access_url(starting_url)


    # Gather all document links from the starting URL (Two Levels)
    collection = web_page.find_all('li')

    # Delete the first two `li` element as they are not the paper items we need
    collection.pop(0)
    collection.pop(0)

    create_nips_abstract_link_csv(collection,nips_year,website_url)

    reviewer_comments_csv(file_name,reviewer_comments_output)


#run_script()
