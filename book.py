import tweepy, re, time
import os
from os import environ
from access import *
from random import randint

# Setup API:


def twitter_setup():
    # Authenticate and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API access:
    api = tweepy.API(auth)
    return api

# Function to extract status (will return status for post):


def extract_status(path=None):

    # No path => return "No book opened!"
    if not path:
        return "No book opened!"

    # Try to search a sentence in book:
    try:
        # Open and read textbook:
        with open(path, 'r', encoding='utf-8', errors="surrogateescape") as book:
            text = book.read()

        # If successfully read, search sentence:
        if text:
            return search_sentence(text)
    # Book not found:
    except:
        return "Book not found!"

# Function to search a sentence in book:
def search_sentence(text):

    status = 200

    # While we have a long or very short status:
    while not (8 < status < 140):
        # Generate a random number:
        index = randint(0, len(text))

        # Set indices of sentence:
        init_index = text[index:].find(".") + 2 + index
        last_index = text[init_index:].find(".") + 2 + init_index
        status = len(text[init_index:last_index])

    # Replace breaks w/spaces:
    sentence = text[init_index:last_index]
    sentence = re.sub("\n", " ", sentence)
    return sentence


if __name__ == '__main__':
    # Setup Twitter API:
    bot = twitter_setup()

    # Set waiting time:
    segs = 18000
    # Eternal posting:
    while True:
        # Extract status:
        status = extract_status('texto.txt')

        # Try to post status:
        try:
            bot.update_status(status)
            print("successfully posted!")
        except tweepy.TweepError as e:
            print(e.reason)
        # Wait till next sentence extraction:
        time.sleep(segs)
