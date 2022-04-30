import twitter
import sys
import io, json
import time
from urllib.error import URLError
from http.client import BadStatusLine
import json
from functools import partial
from sys import maxsize as maxint
import csv


# BEARER_TOKEN
# 'AAAAAAAAAAAAAAAAAAAAAMrAaQEAAAAAQB%2BPxVET1n7Z%2BOtSFPonZIjJV5c%3D6an4V2CW6PRHHJOO3171Fnn3lbcV4rFf36YKT6In3oOlqgXbmR'

# Function oauth_login() from Twitter Cookbook
# The CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET is obtained from the Developer Portal of me
def oauth_login():
    CONSUMER_KEY = '7PZ9dnQoPH3mDukhqw4jVnP3S'
    CONSUMER_SECRET = 'tYMDWAbuLfa9Z8cmCft3pOkKPv02B3yZs2tf7UuGskiInCMmlR'
    OAUTH_TOKEN = '1505545116232081411-DCHbkDaQIZ0AjQD17JuZLYopW82nAz'
    OAUTH_TOKEN_SECRET = 'rDREYMDWa0XeSiEFyvClxLiLg9wrT288KYH1oipAim7Wh'

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

twitter_api = oauth_login()



def twitter_search(twitter_api, q, max_results=2000, **kw):
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets and
    # https://dev.twitter.com/docs/using-search for details on advanced
    # search criteria that may be useful for keyword arguments

    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    search_results = twitter_api.search.tweets(q=q, count=100, **kw)

    statuses = search_results['statuses']

    # Iterate through batches of results by following the cursor until we
    # reach the desired number of results, keeping in mind that OAuth users
    # can "only" make 180 search queries per 15-minute interval. See
    # https://dev.twitter.com/docs/rate-limiting/1.1/limits
    # for details. A reasonable number of results is ~1000, although
    # that number of results may not exist for all queries.

    # Enforce a reasonable limit
    max_results = min(1000, max_results)

    for _ in range(10):  # 10*100 = 1000
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError:  # No more results when next_results doesn't exist
            break

        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([kv.split('=')
                       for kv in next_results[1:].split("&")])

        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']

        if len(statuses) > max_results:
            break

    return statuses


# Sample usage

twitter_api = oauth_login()

q = "Apple M1 OR Apple Silicon OR mac M1"
results = twitter_search(twitter_api, q, max_results=10)
with open('tweet_data.json', 'w', encoding= "utf-8") as outfile:
    json.dump(results, outfile)

outfile.close()

f = open('tweet_data.json', 'r', encoding= "utf-8")
new_json = []

for item in f:
    new_json.append(json.loads(item))

print(new_json[0])
with open('out.csv', 'w', encoding= "utf-8") as csvf:
    wri = csv.writer(csvf)
    wri.writerow(["id", "user_name", "screen_name", "replies_count", "text"])

    for item in new_json[0]:
        #result =
        result = [item['id'], item['user']['name'], item['user']['screen_name'],
                  item['text']]
        wri.writerow(result)

f.close()


#print(json.dumps(results, indent=1))
