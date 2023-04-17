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

def get_all_reviews(base_url):

    print("Getting reviews for {}".format(base_url))

    pageNumber = 1
    reviews = []
    while True:

        print("Getting reviews from page number " + str(pageNumber))
        #url = "https://www.flipkart.com/" + product_name + "/product-reviews/" + product_id + "&marketplace=FLIPKART&page=" + str(pageNumber)
        url = base_url + "&pageNumber=" + str(pageNumber)
        reviews_from_page = get_reviews_from_page(url)
        if len(reviews_from_page) == 0:
            break
        reviews.extend(reviews_from_page)
        pageNumber += 1
        if len(reviews) >= 50:
            break

    reviews = reviews[0:50]

    return(reviews)

def get_reviews_amazonus(url):

    reviews = get_all_reviews(url)

    return(reviews)

# reviews = get_reviews_amazonus("https://www.amazon.com/Bose-QuietComfort-45-Bluetooth-Canceling-Headphones/product-reviews/B098FKXT8L/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews")
#json_dump_to_filename(reviews, "test.json")
