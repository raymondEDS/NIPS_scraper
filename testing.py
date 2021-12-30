from NIPS_Reviews_Crawler import *

y = 'https://proceedings.neurips.cc/paper/2016/file/5d616dd38211ebb5d6ec52986674b6e4-Reviews.html'
web_page_reviews = access_url(y)

#print(web_page_reviews.find('h3').find_next_sibling())
dictionary = {}
for x in web_page_reviews.find_all('p'):
    print('parent----------------------------------------------------------------------------------------------------')
    print(x.parent)    
    print('h3----------------------------------------------------------------------------------------------------')
    print(x.find_previous_sibling('h3').text)
    print('h4----------------------------------------------------------------------------------------------------')
    print(x.find_previous_sibling('h4').text)
    print('text----------------------------------------------------------------------------------------------------')
    print(x.text)
    column_name = x.find_previous_sibling('h3').text + ' '+x.find_previous_sibling('h4').text
    print(column_name)
    dictionary.update({column_name:x.text})
output = [dictionary]
print(output[0])
#print(web_page_reviews.find_all('div',{"class":"response"}))

#reviews_out = reviewer_comments_pre2016(web_page_reviews)
#print(reviews_out)

