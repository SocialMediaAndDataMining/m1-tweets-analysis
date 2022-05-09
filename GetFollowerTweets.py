from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
import pytz
from TweetStore import *
from datetime import datetime
from datetime import timedelta
import sys
import time

# login


def oauth_login():
#     CONSUMER_KEY = 'oTt0t3KtY5zyy31yLdVIOfPGD'
#     CONSUMER_SECRET = 'piplLdrjEXpchSH3yrFTLW0mfUcFclbMXK5UzFmvH0y1m9sp8b'
#     OAUTH_TOKEN = '963697391261175808-LlAzIBbtq0RQJ0OD59MKm3jgr6bYPnA'
#     OAUTH_TOKEN_SECRET = 'WAMTDcHrj6Y5nfu4GdprDaw5FJGITLM4tY7gA5UhthMKo'

    CONSUMER_KEY = 'Nfwl7vJj6KhIutwHShaWxgQAp'
    CONSUMER_SECRET = 'j89pWunk3rDLyIGVLm9l4RBQSeCYCiHwf8WuDzM3pl7IQgcNnW'
    OAUTH_TOKEN = '1503575118831931394-K35j5nNpFpYlxV0CCIs9lfiILUeURE'
    OAUTH_TOKEN_SECRET = 'IRUQxn3xBf3q4PkHZFAmB1MNRln0whIVlMwVB42DL11pr'

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    return API(auth)


def get_user_info(auth_api, user_id):
    user_info = auth_api.get_user(user_id=user_id)
    # print("user ID: "+str(user_info.id))
    return user_info


# filter tweets by substring in string
def filter_tweets1(auth_api, screen_name, userId, start_date, valid_tweets):
    try:
        for status in Cursor(auth_api.user_timeline, screen_name=screen_name).items():
            # print(str(status))
            valid_tweet = {
                'user_id': userId,
                'user_screen_name': screen_name
            }
            if hasattr(status, "text"):
                tweet_body = status.text
                tweet_body_lower = tweet_body.lower()
                if "apple" in tweet_body_lower:
                    if "silicon" in tweet_body_lower:
                        valid_tweet['text'] = tweet_body
                        valid_tweets.append(valid_tweet)
                        print("valid tweet: " + str(tweet_body))
                        break
                    elif "m1" in tweet_body_lower:
                        valid_tweet['text'] = tweet_body
                        valid_tweets.append(valid_tweet)
                        print("valid tweet: " + str(tweet_body))
                        break
                if "m1" in tweet_body_lower:
                    if "silicon" in tweet_body_lower:
                        valid_tweet['text'] = tweet_body
                        valid_tweets.append(valid_tweet)
                        print("valid tweet: " + str(tweet_body))
                        break
                    elif "mac" in tweet_body_lower:
                        valid_tweet['text'] = tweet_body
                        valid_tweets.append(valid_tweet)
                        print("valid tweet: " + str(tweet_body))
                        break

            if status.created_at < start_date:
                break
    except Exception as e:
        if(e.response.status_code == 429):
            print("Too many request to twitter api. Try after 15 mins. After - ", str(datetime.now() + timedelta(minutes=15)))
            exit()
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)
        return
# filter tweets by spliting string into words


def filter_tweets2(auth_api, screen_name, start_date, hashtag, valid_tweets):
    for status in Cursor(auth_api.user_timeline, screen_name=screen_name).items():
        # print(str(status))
        if hasattr(status, "text"):
            tweet_body = status.text
            tweet_body_lower = tweet_body.lower()
            words_in_tweet = tweet_body_lower.split()
            for word in words_in_tweet:
                if hashtag == word:
                    valid_tweets.append(tweet_body)
                    print("valid tweet first: " + str(tweet_body))

        if status.created_at < start_date:
            break


def get_valid_tweets_for_followers():
    au_api = oauth_login()
    valid_tweets = []
    tweetStore = TweetStore()
    limit = 100
    offset = int(tweetStore.getInfluencerTweetsOffset())
    followers_ids = tweetStore.getInfluencerFollowers()[offset:offset + limit]

    count = 0
    #followers_ids = {"189311978"}
    for follower_id in followers_ids:
        count = count + 1
        user = get_user_info(au_api, str(follower_id['_id']))
        name = user.screen_name

        start_date = user.created_at
        #start_date = datetime.now(pytz.utc) - timedelta(days=30)

        # filter_tweets1: less time, filter tweets by matching substring in string
        # filter_tweets2: more time, filter tweets by spliting string into words, then match
        filter_tweets1(au_api, name, user.id, start_date, valid_tweets)

        if count >= 1:
            if(len(valid_tweets) > 0):
                tweetStore.saveInfluencerM1Tweets(valid_tweets)
            offset = offset + count
            tweetStore.saveInfluencerTweetsOffset(offset)
            print(str(len(valid_tweets))+" valid tweets have been added to database.")
            print(valid_tweets)
            valid_tweets = []
            count = 0

def get_valid_tweets_for_followers1000():
    au_api = oauth_login()
    valid_tweets = []
    tweetStore = TweetStore()
    limit = 100
    offset = int(tweetStore.getInfluencerTweetsOffset1000())
    followers_ids = tweetStore.getInfluencerFollowers()[offset:offset + limit]

    count = 0
    #followers_ids = {"189311978"}
    for follower_id in followers_ids:
        count = count + 1
        user = get_user_info(au_api, str(follower_id['_id']))
        name = user.screen_name

        start_date = user.created_at
        #start_date = datetime.now(pytz.utc) - timedelta(days=30)

        # filter_tweets1: less time, filter tweets by matching substring in string
        # filter_tweets2: more time, filter tweets by spliting string into words, then match
        filter_tweets1(au_api, name, user.id, start_date, valid_tweets)

        if count >= 1:
            if(len(valid_tweets) > 0):
                tweetStore.saveInfluencerM1Tweets(valid_tweets)
            offset = offset + count
            tweetStore.saveInfluencerTweetsOffset1000(offset)
            print(str(len(valid_tweets))+" valid tweets have been added to database.")
            print(valid_tweets)
            valid_tweets = []
            count = 0

def get_valid_tweets_for_followers2000():
    au_api = oauth_login()
    valid_tweets = []
    tweetStore = TweetStore()
    limit = 100
    offset = int(tweetStore.getInfluencerTweetsOffset2000())
    followers_ids = tweetStore.getInfluencerFollowers()[offset:offset + limit]

    count = 0
    #followers_ids = {"189311978"}
    for follower_id in followers_ids:
        count = count + 1
        user = get_user_info(au_api, str(follower_id['_id']))
        name = user.screen_name

        start_date = user.created_at
        #start_date = datetime.now(pytz.utc) - timedelta(days=30)

        # filter_tweets1: less time, filter tweets by matching substring in string
        # filter_tweets2: more time, filter tweets by spliting string into words, then match
        filter_tweets1(au_api, name, user.id, start_date, valid_tweets)

        if count >= 1:
            if(len(valid_tweets) > 0):
                tweetStore.saveInfluencerM1Tweets(valid_tweets)
            offset = offset + count
            tweetStore.saveInfluencerTweetsOffset2000(offset)
            print(str(len(valid_tweets))+" valid tweets have been added to database.")
            print(valid_tweets)
            valid_tweets = []
            count = 0
if __name__ == '__main__':
    # rahul and Peiyi
    #get_valid_tweets_for_followers()

    # Yuhui and Jiarui
    #get_valid_tweets_for_followers1000()

    # Kris and Tian
    get_valid_tweets_for_followers2000()
