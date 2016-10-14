import pandas as pd
from twython import Twython, TwythonRateLimitError, TwythonError
from time import sleep
import itertools

APP_KEY = '<MY_APP_KEY>'
APP_SECRET = '<MY_APP_SECRET>'
OAUTH_TOKEN = '<MY_OAUTH_TOKEN>'
OAUTH_SECRET = '<MY_OAUTH_SECRET>'

csv_path = 'tweet_ids_and_sentiments.csv'

# Pagination code shamelessly reproduced from http://stackoverflow.com/a/3744531

def paginate(iterable, page_size):
    while True:
        i1, i2 = itertools.tee(iterable)
        iterable, page = (itertools.islice(i1, page_size, None),
                list(itertools.islice(i2, page_size)))
        if len(page) == 0:
            break
        yield page
        
def get_twython_client():
    return Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_SECRET)

def get_twitter_posts_from_list(client, post_id_list):
    return client.lookup_status(id=post_id_list)

def get_all_tweets(csv_path):
    tweet_ids_and_sentiments = pd.read_csv(csv_path)
    
    twitter_client = get_twython_client()

    pages = list(paginate(tweet_ids_and_sentiments.tweet_id, 100))

    all_tweets = []

    for page in pages:
        try:
            posts = get_twitter_posts_from_list(twitter_client, page)
        except TwythonRateLimitError as e:
            print 'Whoops, we exceeded the rate limit somehow. Pausing for 15 minutes...'
            sleep(15 * 60 + 1)
            posts = get_twitter_posts_from_list(twitter_client, page)
        except TwythonError as e:
            print e

        all_tweets += posts
        print 'got %d posts from page %d...' % (len(posts), pages.index(page) + 1)
    print 'got all pages - %d posts in total' % (len(all_tweets))
    return all_tweets, tweet_ids_and_sentiments

def get_tweet_dataframe(all_tweets, tweet_ids_and_sentiments):
    # List comprehension to grab just the text and ID
    relevant_tweet_info = [
        {
            'text':t['text'],
            'tweet_id':t['id']
        } for t in all_tweets
    ]

    # Turning that list into a dataframe so it can be merged with the dataframe that has the sentiment of each post
    tweet_texts = pd.DataFrame(relevant_tweet_info)
    df = pd.merge(tweet_ids_and_sentiments, tweet_texts)
    
    return df

def fetch_the_data():
    all_tweets , tweet_ids_and_sentiments = get_all_tweets(csv_path)
    df = get_tweet_dataframe(all_tweets, tweet_ids_and_sentiments)
    
    return df