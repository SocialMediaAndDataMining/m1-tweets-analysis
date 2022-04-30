import twitter
import os
from dotenv import load_dotenv

load_dotenv()





def get_twitter_api():
    # XXX: Go to http://twitter.com/apps/new to create an app and get values
    # for these credentials that you'll need to provide in place of these
    # empty string values that are defined as placeholders.
    # See https://developer.twitter.com/en/docs/basics/authentication/overview/oauth
    # for more information on Twitter's OAuth implementation.
    
<<<<<<< HEAD
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    OAUTH_TOKEN = os.getenv('OAUTH_TOKEN')
    OAUTH_TOKEN_SECRET = os.getenv('OAUTH_TOKEN_SECRET')
=======
    CONSUMER_KEY = 'rk58XIhnqTYdmSWpp19YLNwoU'
    CONSUMER_SECRET = 'KHPUpfvGPHDreVDo7qNNwMI3ixmhKoN7dHaVq35qHlsVo23hWE'
    OAUTH_TOKEN = '710852134229647360-NELjId5GR0TOgtCd1Mo0KDq6PozAw89'
    OAUTH_TOKEN_SECRET = 'zmNW9jtrrlJ8AXjd4ClKKQFm8PpdgyiTVeNH5WeaG6q6r'
>>>>>>> refs/remotes/origin/daniel
    
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api
 