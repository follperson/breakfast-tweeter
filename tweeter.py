import argparse
from code.tweeter import *


def cli():
    """
        pick up potential parameters using argparse lib
    :return:
    """
    parser = argparse.ArgumentParser(description="""
        Markov Tweeter
    """)
    parser.add_argument('file', type=str, default='corpus/corpus.txt')

    parser.add_argument('--state', type=int, default=3)  # order arg. default provided as example
    parser.add_argument('--length', type=int, default=280)  # length arg. default provided as example
    parser.add_argument('-n', type=int, default=-1)  # length arg. default provided as example
    parser.add_argument('-s', type=int, default=60*60*24/4)  # time between tweets

    args = parser.parse_args()
    if args.n <= 0:
        n_tweets = 1e6
    else:
        n_tweets = args.n
    tweet_from_file(args.file,message_size=args.length, n_tweets=n_tweets, chain_size=args.state, wait_sec=args.s)


if __name__ == '__main__':
    cli()