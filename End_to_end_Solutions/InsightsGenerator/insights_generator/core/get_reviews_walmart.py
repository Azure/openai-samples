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
        profile_name = review_soup.find_all("div", class_ = "f6 gray pr2")[0].text
    except:
        profile_name = ""
    review_title = review_soup.find_all("span", class_ = "b w_V_DM")[0].text
    date = review_soup.find_all("div", class_ = "f7 gray")[0].text
    location = ""
    stars = str(len(review_soup.find_all("i", class_ = "ld ld-StarFill")))
    review_text = review_soup.find_all("span", class_ = "tl-m db-m")[0].find("span")
    if len(review_text) > 0:
        review_text = review_text.text
    else:
        review_text = ""

    stars_parsed = stars
    stars = stars + " out of 5 stars"

    review = {
            "profile_name" : profile_name,
            "review_title" : review_title,
            "date" : date,
            "location" : location,
            "stars" : stars,
            "stars_parsed" : stars_parsed,
            "review_text" : review_text
            }
    
    return(review)

def get_reviews_from_page(url):

    print("Getting reviews from page: " + url)

    soup = html_code(url)
    #print(soup)
    
    reviews_soup = soup.find_all("li", class_ = "dib w-100 mb3")
 
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
        url = base_url + "?page=" + str(pageNumber)
        reviews_from_page = get_reviews_from_page(url)
        if len(reviews_from_page) == 0:
            break
        reviews.extend(reviews_from_page)
        pageNumber += 1
        if len(reviews) >= 50:
            break

    reviews = reviews[0:50]

    return(reviews)

def get_reviews_walmart(url):

    reviews = get_all_reviews(url)

    return(reviews)

# reviews = get_reviews_walmart("https://www.walmart.com/reviews/product/376188834")
#json_dump_to_filename(reviews, "test.json")
