# BreakfastTweeter

## about
This was created as a project for BreakfastConference 2019. 

Mostly a silly arty project so I could get more experience with webscraping and twitter's API.

find the lil guy posting here: [https://twitter.com/BreakfastTweetr](https://twitter.com/BreakfastTweetr)

## data

The breakfast corpora is from [allrecipes.com](https://www.allrecipes.com). I have recipe descriptions,
 as well as the directions available as corpora. I think the description one is funnier.

Find the details of the scraping at my [recipe scraper repository](https://github.com/follperson/many-breakfasts).

I also have corpora scraped from wikipedia. You can find the data gathering tools in the other branch: `with-crawlers`
 
 
## Usage

### requirements

You will need your [twitter api access information](https://developer.twitter.com/en/docs), and 
to fill in the `config/config_example.py` with your own credentials. Then rename it `config/config.py` for the 
imports to work.

##

To run the program through an IDE, edit the `tweeter.py` file with your filepaths and parameters as needed

To run the program via command line, supplying file, state, and length positional arguments. 

ex: `python tweeter.py corpus/corpus.txt 4 300`

This would return a tweet which has a state of four (i.e the preceding window size), a message length of 300, and 
a data source text file at 'corpus/corpus.txt' 

```
tweeter.py [-h] file state length

Markov Tweeter

positional arguments:
  file
  state
  length

optional arguments:
  -h, --help  show this help message and exit
```
