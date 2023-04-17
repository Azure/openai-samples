# import module
import requests
from bs4 import BeautifulSoup
import pdb
import json
import re
from urllib.request import urlopen
from .get_reviews_flipkart import get_reviews_flipkart
from .get_reviews_amazonus import get_reviews_amazonus
from .get_reviews_walmart import get_reviews_walmart
from .get_reviews_opentable import get_reviews_opentable
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

def parse_review_soup_domestic(review_soup):

    profile_name = review_soup.find_all("span", class_ = "a-profile-name")[0].text
    review_title = review_soup.find_all("a", class_ = "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold")[0].find_all("span")[0].text
    date_location = review_soup.find_all("span", class_ = "a-size-base a-color-secondary review-date")[0].text
    stars = review_soup.find_all("span", class_ = "a-icon-alt")[0].text
    review_text = review_soup.find_all("span", class_ = "a-size-base review-text review-text-content")[0].find_all("span")
    if len(review_text) > 0:
        review_text = review_text[0].text
    else:
        review_text = ""

    review = {
            "profile_name" : profile_name,
            "review_title" : review_title,
            "date_location" : date_location,
            "stars" : stars,
            "review_text" : review_text
            }
    return(review)

def parse_review_soup_foreign(review_soup):

    profile_name = review_soup.find_all("span", class_ = "a-profile-name")[0].text
    review_title = review_soup.find_all("span", class_ = "a-size-base review-title a-color-base review-title-content a-text-bold")[0].find_all("span")[0].text
    date_location = review_soup.find_all("span", class_ = "a-size-base a-color-secondary review-date")[0].text
    stars = review_soup.find_all("span", class_ = "a-icon-alt")[0].text
    review_text = review_soup.find_all("span", class_ = "a-size-base review-text review-text-content")[0].find_all("span")
    if len(review_text) > 0:
        review_text = review_text[0].text
    else:
        review_text = ""

    review = {
            "profile_name" : profile_name,
            "review_title" : review_title,
            "date_location" : date_location,
            "stars" : stars,
            "review_text" : review_text
            }
    return(review)

def get_reviews_from_page(url):

    print("Getting reviews from page: " + url)

    soup = html_code(url)
    #print(soup)
    
    
    
    reviews_soup = soup.find_all("div", class_ = "a-section review aok-relative")
 
    reviews = []
    for review_soup in reviews_soup:

        is_foreign = len(review_soup.find_all("div", id=  re.compile("customer_review_foreign"))) > 0

        if not is_foreign:
            review = parse_review_soup_domestic(review_soup)
        else:
            review = parse_review_soup_foreign(review_soup)

        
        date_location_search = re.search('Reviewed in (.*) on (.*)', review["date_location"], re.IGNORECASE)

        # Post processing
        review["id"] = str(uuid.uuid4())
        review["location"] = date_location_search.group(1)
        review["date"] = date_location_search.group(2)

        stars_search = re.search('(.*) out of 5 stars', review["stars"], re.IGNORECASE)
        review["stars_parsed"] = stars_search.group(1)

        review.pop("date_location")

        reviews.append(review)
    
    
    print("Got {} reviews".format(len(reviews)))

    return(reviews)

def get_all_reviews(product_name, product_id):

    print("Getting reviews for {} with product id {}".format(product_name, product_id))

    pageNumber = 1
    reviews = []
    while True:

        print("Getting reviews from page number" + str(pageNumber))
        url = "https://www.amazon.in/" + product_name + "/product-reviews/" + product_id + "/ref=cm_cr_getr_d_paging_btm_prev_1?pageNumber=" + str(pageNumber)
        reviews_from_page = get_reviews_from_page(url)
        if len(reviews_from_page) == 0:
            break
        reviews.extend(reviews_from_page)
        pageNumber += 1
        if len(reviews) >= 30:
            break

    return(reviews)

def json_dump_to_filename(data, filename):
    print('Writing json to file: ' + filename)
    file = open(filename, 'w', encoding = 'utf-8')
    results = json.dump(data, file, indent = 4, sort_keys = True)
    file.close()
    return


def get_reviews_amazon(url):

    prod_details_search = re.search('https://www.amazon.in/(.*)/dp/(.*)/', url, re.IGNORECASE)
    
    if prod_details_search:
        product_name = prod_details_search.group(1)
        product_id = prod_details_search.group(2)
    
    #product_name = "Bose-Quietcomfort-Bluetooth-Headphones-Cancelling"
    #product_id = "B098FKXT8L"
    
    reviews = get_all_reviews(product_name, product_id)

    return(reviews)

def get_reviews(url):

    is_amazon_url = re.search("www.amazon.in", url)
    is_flipkart_url = re.search("www.flipkart.com", url)
    is_amazonus_url = re.search("www.amazon.com", url)
    is_walmart_url = re.search("www.walmart.com", url)
    is_opentable_url = re.search("www.opentable.com", url)
    is_json_file_url = re.search(".json$", url)

    if is_amazon_url:
        reviews = get_reviews_amazon(url)
    elif is_flipkart_url:
        reviews = get_reviews_flipkart(url)
    elif is_amazonus_url:
        reviews = get_reviews_amazonus(url)
    elif is_walmart_url:
        reviews = get_reviews_walmart(url)
    elif is_opentable_url:
        reviews = get_reviews_opentable(url)
    elif is_json_file_url:
        url_file = urlopen(url)
        reviews = json.load(url_file)
        url_file.close()
    else:
        reviews = []

    return(reviews)
