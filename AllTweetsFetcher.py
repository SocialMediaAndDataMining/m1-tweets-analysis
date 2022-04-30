from sklearn.linear_model import TweedieRegressor
import twitter
import json
from urllib.parse import unquote
from TwitterLoginApi import get_twitter_api
from TweetStore import TweetStore


def twitter_search(twitter_api, q, max_results=1000, **kw):

    # See https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
    # and https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
    # for details on advanced search criteria that may be useful for 
    # keyword arguments
    
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets    
    search_results = twitter_api.search.tweets(q=q, count=500, **kw)
    statuses = search_results['statuses']
    
    # Iterate through batches of results by following the cursor until we
    # reach the desired number of results, keeping in mind that OAuth users
    # can "only" make 180 search queries per 15-minute interval. See
    # https://developer.twitter.com/en/docs/basics/rate-limits
    # for details. A reasonable number of results is ~1000, although
    # that number of results may not exist for all queries.
    
    # Enforce a reasonable limit
    max_results = min(1000, max_results)
    
    kwargs = dict([ kv.split('=') for kv in unquote(search_results['search_metadata']['next_results'][1:]).split("&") ])
    cursor = kwargs['max_id']
    for _ in range(2): # 10*100 = 1000
        try:
            next_results = search_results['search_metadata']['next_results']
            
        except KeyError as e: # No more results when next_results doesn't exist
            break
            
        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=') for kv in unquote(next_results[1:]).split("&") ])
        
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']
        cursor = kwargs['max_id']
        print("len(statuses) - ",len(statuses))
        if len(statuses) >= max_results: 
            break
            
    return statuses, cursor

# Sample usage


def get_all_tweets():
    twitter_api = get_twitter_api()
    tweetStore = TweetStore()
    q = "(apple silicon) OR (apple M1) OR (mac M1) OR (M1 silicon) OR #applesilicon OR #macm1"

    # change this range to what you want. number of twweets fetched =  range * 300 and saved every loop into Tweetstore.
    for _ in range(50):
        max_id = tweetStore.getAllTweetsOffset()
        if(int(max_id) > 0):
            results, max_id = twitter_search(twitter_api, q, max_results=1000, max_id = max_id, lang='en')
        else:
            results, max_id = twitter_search(twitter_api, q, max_results=1000, lang='en')

        #save into db
        tweetStore.saveAllTweetsOffset(max_id)
        tweetStore.saveAllM1Tweets(results)

    # Show one sample search result by slicing the list...
    print("Offset is  -",max_id)


get_all_tweets()