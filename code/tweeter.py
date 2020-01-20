#!/usr/bin/env python3
import tweepy
import time
from config.config import key, secret, token_key, token_secret
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


def tweet_from_file(fp, message_size=280, n_tweets=999, chain_size=3, decode=True, wait_sec=60*30):
    print(fp)
    twitter_api = TwitterObj()
    run = 1
    while run <= n_tweets:
        message = get_tweet(fp, message_size, chain_size, decode)
        if message is not None:
            if len(message) > 279:
                continue
            print('Run %s' % run)
            print(message)
            try:
                pass
                twitter_api.tweet(message)
            except tweepy.error.TweepError as e:
                print('error', str(e))
            run += 1
            time.sleep(wait_sec)


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
