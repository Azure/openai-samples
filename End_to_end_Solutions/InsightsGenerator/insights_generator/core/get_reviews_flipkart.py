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

    profile_name = review_soup.find_all("p", class_ = "_2sc7ZR _2V5EHH")[0].text
    review_title = review_soup.find_all("p", class_ = "_2-N8zT")[0].text
    date = review_soup.find_all("p", class_ = "_2sc7ZR")[1].text
    location = review_soup.find_all("p", class_ = "_2mcZGG")[0].find_all("span")[1].text[2:]
    regex = re.compile('.*_3LWZlK .*_1BLPMq')
    stars = review_soup.find_all("div", {"class" : regex})[0].text
    # stars = "0"
    review_text = review_soup.find_all("div", class_ = "t-ZTKy")[0].find_all("div")[0].find_all("div", class_ ="")
    if len(review_text) > 0:
        review_text = review_text[0].text
    else:
        review_text = ""

    review = {
            "profile_name" : profile_name,
            "review_title" : review_title,
            "date" : date,
            "location" : location,
            "stars_parsed" : stars,
            "review_text" : review_text
            }

    return(review)

def get_reviews_from_page(url):

    print("Getting reviews from page: " + url)

    soup = html_code(url)
    #print(soup)
    
    
    
    reviews_soup = soup.find_all("div", class_ = "_27M-vq")
 
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
        if len(reviews) >= 30:
            break

    return(reviews)

def get_reviews_flipkart(url):

    reviews = get_all_reviews(url)

    return(reviews)

#reviews = get_reviews("https://www.flipkart.com/bose-quietcomfort-35-ii-active-noise-cancellation-enabled-bluetooth-headset/p/itm8742293cc76a3?pid=ACCEYZW7NNN7DZSF&lid=LSTACCEYZW7NNN7DZSFPRQZPG&marketplace=FLIPKART&q=bose+headphones&store=0pm%2Ffcn%2Fgc3&srno=s_1_2&otracker=search&otracker1=search&fm=Search&iid=f0659e9d-3cef-460e-bfd9-5dc7205d2ddf.ACCEYZW7NNN7DZSF.SEARCH&ppt=sp&ppn=sp&ssid=ggkpk7lexs0000001672660381041&qH=7fcff5e537fdb9c8")

#json_dump_to_filename(reviews, "test.json")
