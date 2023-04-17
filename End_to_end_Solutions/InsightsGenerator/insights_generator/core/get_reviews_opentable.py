# import module
import requests
from bs4 import BeautifulSoup
import pdb
import json
import re
from urllib.request import urlopen
import uuid

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

# user define function
# Scrape the data
def getdata(url):
    r = requests.get(url, headers=HEADERS)
    return r.text


def html_code(url):

    # pass the url
    # into getdata function
    htmldata = getdata(url)
    soup = BeautifulSoup(htmldata, 'html.parser')

    # display html code
    return (soup)

def parse_review_soup(review_soup):
    try:
        profile_name = review_soup.find_all("p", class_ = "V0gqMM0V5nr33Ha56k83 BoZ_Hzg4GGZ1XXDaNyct")[0].text
    except:
        profile_name = ""
    review_title = ""
    date = review_soup.find_all("p", class_ = "Xfrgl6cRPxn4vwFrFgk1")[0].text
    try:
        location = review_soup.find_all("p", class_ = "UGzxfqPCuflxNBXSUvL_ BoZ_Hzg4GGZ1XXDaNyct")[0].text
    except:
        location = ""
    stars = review_soup.find_all("span", class_ = "Q2DbumELlxH4s85dk8Mj")[0].text
    review_text = review_soup.find_all("div", class_ = "f3cNr0xDcwvMaBkpjQj5")[0].find("span")
    if len(review_text) > 0:
        review_text = review_text.text
    else:
        review_text = ""

    # HARD CODED HACK # TODO: Fix
    date = "2022-01-01"

    review = {
            "profile_name" : profile_name,
            "review_title" : review_title,
            "date" : date,
            "location" : location,
            "stars" : stars,
            "stars_parsed" : stars,
            "review_text" : review_text
            }
    
    return(review)

def get_reviews_from_page(url):

    print("Getting reviews from page: " + url)

    soup = html_code(url)
    #print(soup)
    
    reviews_soup = soup.find_all("li", class_ = "mbK0eco4h3AaJgKLBhb9")
 
    reviews = []
    for review_soup in reviews_soup:

        review = parse_review_soup(review_soup)
        review["id"] = str(uuid.uuid4())

        reviews.append(review)
    
    
    print("Got {} reviews".format(len(reviews)))

    return(reviews)

def get_all_reviews(base_url):

    print("Getting reviews for {}".format(base_url))

    pageNumber = 1
    reviews = []
    while True:

        print("Getting reviews from page number " + str(pageNumber))
        #url = "https://www.flipkart.com/" + product_name + "/product-reviews/" + product_id + "&marketplace=FLIPKART&page=" + str(pageNumber)
        url = base_url + "&page=" + str(pageNumber)
        reviews_from_page = get_reviews_from_page(url)
        if len(reviews_from_page) == 0:
            break
        reviews.extend(reviews_from_page)
        pageNumber += 1
        if len(reviews) >= 100:
            break

    reviews = reviews[0:100]

    return(reviews)

def get_reviews_opentable(url):

    base_url_search = re.search('(.*)&page=(.*)', url, re.IGNORECASE)
    
    if base_url_search:
        base_url = base_url_search.group(1)

    reviews = get_all_reviews(base_url)

    return(reviews)

# reviews = get_reviews_opentable("https://www.opentable.com/r/spinasse-seattle?corrid=93cc5a4f-87f7-4d25-9ac2-04b0f4c9e066&avt=eyJ2IjoyLCJtIjoxLCJwIjowLCJzIjowLCJuIjowfQ&p=2&sd=2023-01-05T19%3A00%3A00&page=1")
#json_dump_to_filename(reviews, "test.json")
