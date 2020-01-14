#!/usr/bin/env python3
import tweepy
import time
from config import key, secret, token_key, token_secret
import markovify as mk
par_delim = ' -- '


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


def tweet_from_file(fp, message_size=280, n_tweets=999, chain_size=3, decode=True):
    print(fp)
    twitter_api = TwitterObj()
    run = 1
    while run < n_tweets:
        message = get_tweet(fp, message_size, chain_size, decode)
        if message is not None:
            if len(message) > 279:
                continue
            print('Run %s' % run)
            print(message)
            try:
                twitter_api.tweet(message)
            except tweepy.error.TweepError as e:
                print('error', str(e))
            run += 1
            time.sleep(60*30)


def get_tweet(fp, size=280, chain_size=3, decode=True, max_attempts=20):
    """
        this function loads a model from a file path and returns a sentence with a maximum number of characters
    :param fp: text filepath, with training texts on each lines
    :param size: number of characters allowed in message
    :param chain_size: number of tokens used to seed the model
    :param decode: bool - depending on the encoding type we need to clean the text file
    :param max_attempts: max number of attempts to make a sentence
    :return:
    """
    decoded = read_corpus(fp,decode=decode)
    text_model = mk.NewlineText('\n'.join(decoded), chain_size)
    print('_'*100)
    attempts = 0
    for i in range(max_attempts):
        attempts += 1
        message = text_model.make_short_sentence(size)
        if message is not None:
            print('Took %s tries to get message' % attempts)
            return message


def read_corpus(fp,decode=True):
    """
        load the corpus from a filepath
    :param fp:
    :param decode:
    :return:
    """
    if decode:
        with open(fp, 'rb') as docs:
            data = docs.readlines()
            decoded = [line.decode('utf8').replace(par_delim, '').replace('=', '') for line in data]
    else:
        with open(fp, 'r') as docs:
            decoded = docs.readlines()
    decoded = list(set(decoded))
    return decoded



def breakfast_tweet():
    tweet_from_file('corpus\\breakfast\\breakfast.txt')


def general_wiki_summary(size=280):
    tweet_from_file('corpus\\corpus.txt', size)


def allrecipes_description():
    while True:
        tweet_from_file('corpus\\breakfast\\description - article level.txt',
                        message_size=240, chain_size=5, decode=False)


def allrecipes_directions_line():
    while True:
        tweet_from_file('corpus\\breakfast\\directions_cleaned - line level.txt',
                        message_size=240, chain_size=5, decode=False)


def allrecipes_directions_article():
    while True:
        tweet_from_file('corpus\\breakfast\\directions_cleaned - article level.txt',
                        message_size=240, chain_size=3, decode=False)

def allrecipes_blend():
    while True:
        print('Description')
        tweet_from_file('corpus\\breakfast\\description - article level.txt', n_tweets=2,
                        message_size=240, chain_size=5, decode=False)
        print('Direction Line')
        tweet_from_file('corpus\\breakfast\\directions_cleaned - line level.txt', n_tweets=2,
                        message_size=240, chain_size=5, decode=False)
        print('Direction Article')
        tweet_from_file('corpus\\breakfast\\directions_cleaned - article level.txt', n_tweets=2,
                        message_size=240, chain_size=3, decode=False)

if __name__ == "__main__":
    # breakfast_tweet()
    # general_wiki_summary()
    # allrecipes_directions_article()
    # allrecipes_description()
    allrecipes_blend()
