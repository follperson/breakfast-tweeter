#!/usr/bin/env python3
import tweepy
import time
import sys
# import markoviy
import datetime
from brekky import write_breakfast
from config import key, secret, token_key, token_secret
from wiki_gen import get_tweet

class TwitterObj(object):
    def __init__(self):
        consumer_key = key
        consumer_secret = secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = token_key
        access_token_secret = token_secret
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        self.api.update_status(status=message)

def general_wiki_summary(size=280):
    tweet_from_file('corpus\\corpus.txt',size)

def tweet_from_file(fp,size=280):
    twitter_api = TwitterObj()
    run = 1
    while True:
        message = get_tweet(fp,False,size)
        print('Run %s' % run)
        print(message)
        twitter_api.tweet(message)
        run += 1
        time.sleep(60*30)


def breakfast_tweet():
    tweet_from_file('corpus\\breakfast\\breakfast.txt')

if __name__ == "__main__":
    # breakfast_tweet()
    general_wiki_summary()