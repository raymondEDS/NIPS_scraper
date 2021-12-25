from NIPS_Reviews_Crawler import *


website_url = "https://proceedings.neurips.cc"
nips_year = '2015'
starting_url = "https://proceedings.neurips.cc/paper/" + nips_year
file_name = "nips_paper_links_" + nips_year +'.csv'
reviewer_comments_output = "nips_paper_reviews_" + nips_year +'.csv'
# Access and test the starting URL
web_page = access_url(starting_url)

collection = web_page.find_all('li')

# Delete the first two `li` element as they are not the paper items we need
collection.pop(0)
collection.pop(0)
#create_nips_abstract_link_csv(collection,nips_year,website_url)


def reviewer_comments_pre2016(webpage):
    #returns reviewer number and comment in a list
    paper_reviews = []
    i = 0
    for i in range(len(webpage.find_all('div',{"class":"response"}))):
        comments = webpage.find_all('div',{"class":"response"})
        
        #must have the reviewer + i + 1 or else reviewer_comments_csv() will break
        paper_reviews.append(['reviewer '+ str(i+1),comments[i].text])
        i += 1
    return(paper_reviews)

y = 'https://papers.nips.cc/paper/2015/file/020c8bfac8de160d4c5543b96d1fdede-Reviews.html'
web_page_reviews = access_url(y)

print(web_page_reviews.find_all('div',{"class":"response"}))

#reviews_out = reviewer_comments_pre2016(web_page_reviews)
#print(reviews_out)

