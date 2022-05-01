from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
import pytz
from TweetStore import *

# login


def oauth_login():
    CONSUMER_KEY = '7MW0Wht4XDKD9XmsdYLMR8rW7'
    CONSUMER_SECRET = 'B7ZLnIwE2Bhzt2AJQWtcL2vQ2UJ7oYYqIHIIqDsi22tN1ALnyH'
    OAUTH_TOKEN = '792786443051601921-yQWxJALbBGIThpOnfvZKXz9ga5jjN6k'
    OAUTH_TOKEN_SECRET = 'uLDDvVliEcTdct8g6TmdtLNT7PzaJjDMLpuHZYpcPdbx1'

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    return API(auth)


def get_user_info(auth_api, user_id):
    user_info = auth_api.get_user(user_id=user_id)
    # print("user ID: "+str(user_info.id))
    return user_info


# filter tweets by substring in string
def filter_tweets1(auth_api, screen_name, userId, start_date, valid_tweets):
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


def get_valid_tweets(hashtag):
    au_api = oauth_login()
    valid_tweets = []
    tweetStore = TweetStore()
    limit = 10
    offset = int(tweetStore.getInfluencerTweetsOffset())
    followers_ids = tweetStore.getInfluencerFollowers()[offset:limit]

    #followers_ids = {"189311978"}
    for follower_id in followers_ids:
        user = get_user_info(au_api, str(follower_id['_id']))
        name = user.screen_name

        start_date = user.created_at
        #start_date = datetime.now(pytz.utc) - timedelta(days=30)

        # filter_tweets1: less time, filter tweets by matching substring in string
        # filter_tweets2: more time, filter tweets by spliting string into words, then match
        filter_tweets1(au_api, name, user.id, start_date, valid_tweets)

    print(valid_tweets)

    tweetStore.saveInfluencerM1Tweets(valid_tweets)
    tweetStore.saveInfluencerTweetsOffset(limit + offset)
    print(str(len(valid_tweets))+" valid tweets have been added to database.")


if __name__ == '__main__':
    '''
    #name = "Edmundyu1995"
    #userID = "189311978"
    followers_ids=["189311978", "189311978"]
    '''
    # please enter a keyword in lowercase
    htag = "apple"
    get_valid_tweets(htag)
