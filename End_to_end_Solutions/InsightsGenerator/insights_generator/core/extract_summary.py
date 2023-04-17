from . import OAI_client
import re
from . import extract_statistical_summary
import random
import pdb

def extract_direct_answer(reviews, user_query:str):
    print ("Reached summary from {len(reviews)} reviews")
    print (reviews[0])
    prompt_template_filename = "insights_generator/core/prompt_template_direct_summary.txt"
    prompt_template_file = open(prompt_template_filename, encoding = "utf-8")
    prompt_template_summary = prompt_template_file.read()
    
    review_texts = []
    for i, review in enumerate(reviews):
        review_text = review["review_text"]
        if len(review_text) > 0:
            review_texts.append(review_text)
            #stars = review["stars"]
            #sentiment_aspects = sentiment_aspects + [f"## Review {i + 1} - {stars}"] + review["sentiment_aspects_NL"]

    prompt_parameters = {"review_texts" : "\n".join(review_texts), "question": user_query}

    prompt = OAI_client.construct_prompt(prompt_parameters, prompt_template_summary)
    print (f"Interactive prompt: {prompt}")
    completion = OAI_client.make_prompt_request(prompt, max_tokens = 200, timeout = 10)
    out_summary = {"answer" : completion}

    return out_summary

def extract_summary_old(reviews, user_query:str):
    # This function was giving bad results. This is obsoleted

    print ("Reached summary from {len(reviews)} reviews")
    print (reviews[0])
    prompt_template_filename = "insights_generator/core/prompt_template_summary.txt"
    prompt_template_file = open(prompt_template_filename, encoding = "utf-8")
    prompt_template_summary = prompt_template_file.read()
    
    sentiment_aspects = []
    for i, review in enumerate(reviews):
        sentiment_aspects = sentiment_aspects + review["sentiment_aspects_NL"]

    prompt_parameters = {"sentiment_aspects" : "\n".join(sentiment_aspects)}
    prompt = OAI_client.construct_prompt(prompt_parameters, prompt_template_summary)
    if len(user_query) > 0:
        prompt = prompt.replace("### Questions", f"### Questions: {user_query}")
        print (f"Interactive prompt: {prompt}")

    completion = OAI_client.make_prompt_request(prompt, max_tokens = 200, timeout = 10)
    completion_lines = completion.split("\n")
    print("Extracted summaries")

    # Parse the summary
    p = re.compile("1\)((.|\n)*)2")
    result = p.search(completion)
    if not result is None:
        overall = result.group(1)
    else:
        overall = ""

    p = re.compile("2\)((.|\n)*)3")
    result = p.search(completion)
    if not result is None:
        high_lowlights = result.group(1)
    else:
        high_lowlights = ""

    p = re.compile("3\)((.|\n)*)")
    result = p.search(completion)
    if not result is None:
        actions = result.group(1)
    else:
        actions = ""

    out_summary = {"summary" : completion, "overall" : overall, "high_lowlights" : high_lowlights, "actions" : actions}

    return out_summary

def overall_statistics_to_raw_text(overall_statistics_dict):

    # Get the positive and negative aspects separately
    positive_aspects = []
    negative_aspects = []
    for top_aspect, statistics in overall_statistics_dict.items():
        percentage_positive = statistics["percentage_positive"]
        if not percentage_positive is None:
            if percentage_positive >= 75:
                positive_aspects.append(top_aspect)
            elif percentage_positive <= 25:
                negative_aspects.append(top_aspect)

    # Convert into raw text
    raw_text = ""
    for positive_aspect in positive_aspects:
        raw_text += "{} is good.\n".format(positive_aspect)

    for negative_aspect in negative_aspects:
        raw_text += "{} is bad.\n".format(negative_aspect)

    return(raw_text)

def extract_statistical_summary_NL(product_category, overall_statistics_dict):

    statistics_raw_text = overall_statistics_to_raw_text(overall_statistics_dict)
    prompt_template_filename = "insights_generator/core/prompt_template_statistics_raw_text_to_NL.txt"
    prompt_template_file = open(prompt_template_filename, encoding = "utf-8")
    prompt_template_summary = prompt_template_file.read()
    
    prompt_parameters = {"product_category" : product_category, "comments" : statistics_raw_text}

    prompt = OAI_client.construct_prompt(prompt_parameters, prompt_template_summary)

    completion = OAI_client.make_prompt_request(prompt, max_tokens = 200, timeout = 10)
    overall_summary = completion.strip()

    print("Extracted NL version of statistical summary.")

    summary = {"overall" : overall_summary}

    return(summary)


def summarize_aspect_summaries(product_category, aspect_summaries):

    if len(aspect_summaries) == 0:
        return("")

    prompt_template_filename = "insights_generator/core/prompt_template_summarize_aspect_summaries.txt"
    prompt_template_file = open(prompt_template_filename, encoding = "utf-8")
    prompt_template = prompt_template_file.read()

    # Limit to random sample of 10 aspects
    if len(aspect_summaries) > 10:
        aspect_summaries = random.sample(aspect_summaries, 10)

    prompt_parameters = {
            "product_category" : product_category,
            "aspect_summaries" : "\n".join(aspect_summaries)
            }

    prompt = OAI_client.construct_prompt(prompt_parameters, prompt_template)

    completion = OAI_client.make_prompt_request(prompt, max_tokens = 500, timeout = 10)

    # Strip whitespace
    completion = completion.strip()

    return(completion)

def extract_highlights_lowlights(product_category, aspects_dict):

    # Get the positive aspect summaries
    # and the negative aspect summaries
    positive_aspect_summaries = []
    negative_aspect_summaries = []
    for aspect, aspect_information in aspects_dict.items():

        aspect_summary = aspect_information["aspect_summary"]

        if not aspect_summary is None:
            overall_sentiment = aspect_information["overall_sentiment"]

            if overall_sentiment == "positive":
                positive_aspect_summaries.append(aspect_summary)
            elif overall_sentiment == "negative":
                negative_aspect_summaries.append(aspect_summary)

    # Get the highlights
    highlights = summarize_aspect_summaries(product_category, positive_aspect_summaries)
    lowlights = summarize_aspect_summaries(product_category, negative_aspect_summaries)

    
    summary = {"highlights" : highlights, "lowlights" : lowlights}

    return(summary)


def extract_summary(product_category, aspects_dict):

    summary = {}

    # Get the overall
    overall_summary = extract_statistical_summary_NL(product_category, aspects_dict)
    summary.update(overall_summary)

    # Get the high and low lights
    high_low_lights_summary = extract_highlights_lowlights(product_category, aspects_dict)
    summary.update(high_low_lights_summary)

    # Get the action items
    action_items = {}
    for aspect, aspect_information in aspects_dict.items():
        aspect_action_items = aspect_information["aspect_action_items"]
        if not aspect_action_items is None:
            action_items[aspect] = aspect_action_items

    summary["action_items"] = action_items

    return(summary)
