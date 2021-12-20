import tweepy, re, time
import os
from os import environ
from access import *
from random import randint



def twitter_setup():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth)
    return api


def extract_status(path=None):

    if not path:
        return "No book opened!"

    try:
        with open(path, 'r', encoding='utf-8', errors="surrogateescape") as book:
            text = book.read()

        if text:
            return search_sentence(text)
    except:
        return "Book not found!"


def search_sentence(text):

    status = 200

    while not (8 < status < 140):
        index = randint(0, len(text))

        init_index = text[index:].find(".") + 2 + index
        last_index = text[init_index:].find(".") + 2 + init_index
        status = len(text[init_index:last_index])

    sentence = text[init_index:last_index]
    sentence = re.sub("\n", " ", sentence)
    return sentence


if __name__ == '__main__':
    bot = twitter_setup()

    # Waiting time until next post:
    segs = 18000

    while True:
        status = extract_status('texto.txt')

        try:
            bot.update_status(status)
            print("successfully posted!")
        except tweepy.TweepError as e:
            print(e.reason)

        time.sleep(segs)
