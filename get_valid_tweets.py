from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
import pytz

# login


def oauth_login():
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    return API(auth)

    # use userName to get user's
    '''https://www.geeksforgeeks.org/python-api-get_user-in-tweepy/
    screen_name : specifies the screen name of the user, useful to differentiate accounts when a valid screen name is also a user ID
    Returns : an object of the class User'''


def get_user_info(auth_api, user_id):
    user_info = auth_api.get_user(user_id=user_id)
    #print("user ID: "+str(user_info.id))
    return user_info


def print_user_info(user_info):
    print("user_id: " + str(user_info.id))
    print("name: " + user_info.name)
    print("screen_name: " + user_info.screen_name)
    print("description: " + user_info.description)
    print("created_date: " + str(user_info.created_at))
    print("statuses_count: " + str(user_info.statuses_count))
    print("friends_count: " + str(user_info.friends_count))
    print("followers_count: " + str(user_info.followers_count))
    print("total tweets: " + str(user_info.statuses_count))

    print()

    account_created_date = user_info.created_at
    delta = datetime.now(pytz.utc) - account_created_date

    account_age_days = delta.days
    print("Account age (in days): " + str(account_age_days))

    if account_age_days > 0:
        print("Average tweets per day: " + "%.2f" %
              (float(user_info.statuses_count) / float(account_age_days)))

    print()

# Cursor Tutorial: https://docs.tweepy.org/en/v3.5.0/cursor_tutorial.html


def find_user_post_hashtag(auth_api, screen_name, start_date, htag, user_id):
    userID_tweet = []
    for status in Cursor(auth_api.user_timeline, screen_name=screen_name).items():
        # print(str(status))
        if hasattr(status, "entities"):
            entities = status.entities
            if "hashtags" in entities:
                for ent in entities["hashtags"]:
                    if ent is not None:
                        if "text" in ent:
                            hashtag = ent["text"]
                            if hashtag == htag:
                                if hasattr(status, "text"):
                                    userID_tweet.append(user_id)
                                    userID_tweet.append(status.text)
                                    if len(userID_tweet) > 1:
                                        #print("user ID: "+str(userID_tweet[0]))
                                        #print("valid tweet: "+str(userID_tweet[1]))
                                        return len(userID_tweet) > 0, userID_tweet

        if status.created_at < start_date:
            break

    print()
    print(str(len(userID_tweet)) + " tweets found with hashtag: " + htag)
    print()

    return len(userID_tweet) > 0, userID_tweet


def get_valid_tweets_from_userids(followers_ids, hashtag, all_userID_tweet):

    au_api = oauth_login()

    for follower_id in followers_ids:
        user = get_user_info(au_api, follower_id)
        name = user.screen_name

        '''start_date = user.created_at'''
        start_date = datetime.now(pytz.utc) - timedelta(days=30)

        found, userID_tweet = find_user_post_hashtag(
            au_api, name, start_date, hashtag, follower_id)

        if found:
            all_userID_tweet.append(userID_tweet)


''':parameter
       influencer_name: screen_name of the chosen influencer
       followers_limit: least number of tweets required for future analysis
       first_load_limit: number of follower IDs loaded for the first time
       reload_limit: number of followers IDs loaded for each time if the first loading did not get enough valid tweets
    output
        all_userID_tweet: list of pair<user ID, valid tweet>'''

'''
def get_valid_tweets(influencer_name, followers_limit, first_load_limit, reload_limit, hashtag):
    au_api = oauth_login()

    # first-time get follower IDs
    t_cursor, t_followers_ids = get_followers_ids(
        au_api, screen_name=influencer_name, followers_limit=first_load_limit)
    all_userID_tweet = []
    get_valid_tweets_from_userids(t_followers_ids, hashtag, all_userID_tweet)

    # continue loading until enough valid tweets are found
    while len(all_userID_tweet) < followers_limit:
        cursor, followers_ids = get_followers_ids(au_api, screen_name=influencer_name, followers_limit=reload_limit, t_cursor)
        get_valid_tweets_from_userids(followers_ids, hashtag, all_userID_tweet)
        t_cursor = cursor

    return all_userID_tweet'''


def get_valid_tweets_test(influencer_name, followers_limit, first_load_limit, reload_limit, hashtag):
    au_api = oauth_login()

    # first-time get follower IDs
    t_followers_ids = ["189311978", "189311978"]
    all_userID_tweet = []
    get_valid_tweets_from_userids(t_followers_ids, hashtag, all_userID_tweet)

    '''while len(all_userID_tweet) < followers_limit:
        cursor, followers_ids = get_followers_ids(au_api, screen_name=influencer_name, followers_limit=reload_limit,t_cursor)
        get_valid_tweets_from_userids(followers_ids, hashtag, all_userID_tweet)
        t_cursor=cursor'''
    for userID_tweet in all_userID_tweet:
        print("follower ID: ", userID_tweet[0])
        print("tweet: ", userID_tweet[1])
        print()
    return all_userID_tweet


def main():
    '''
    #name = "Edmundyu1995"
    #userID = "189311978"
    followers_ids=["189311978", "189311978"]
    htag = "sigalaandbeckycollab"

    get_valid_tweets_from_userids(followers_ids, htag, all_userID_tweet)'''
    get_valid_tweets_test("katyperry", 1000, 10000,
                          5000, "sigalaandbeckycollab")


if __name__ == '__main__':
    main()
