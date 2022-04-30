import twitter
import sys
import time
import json
from urllib.error import URLError
from http.client import BadStatusLine
from functools import partial


def oauth_login():
    """
        Authentication
    """
    
    CONSUMER_KEY = 'mYdfcMZDJIpEE5cvstEEo4Ygv'
    CONSUMER_SECRET = 'ZLkfq36c7d97ea7kTs4uX9DMpplDpx7vo6Dyig9AxSpBzMgLtn'
    OAUTH_TOKEN = '1503535128601153538-49IJXG0mwZry9QPCdNavYPqVDkuvRc'
    OAUTH_TOKEN_SECRET = 'n48tUKo0I7gG1IvfmlwUWfBGKcr3JQIDPwLyqOwjopOov'
    
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api




def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw): 
    
    # A nested helper function that handles common HTTPErrors. Return an updated
    # value for wait_period if the problem is a 500 level error. Block until the
    # rate limit is reset if it's a rate limiting issue (429 error). Returns None
    # for 401 and 404 errors, which requires special handling by the caller.
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
    
        if wait_period > 3600: # Seconds
            print('Too many retries. Quitting.')
            raise e
    
        # See https://developer.twitter.com/en/docs/basics/response-codes
        # for common codes
    
        if e.e.code == 401:
            print('Encountered 401 Error (Not Authorized)')
            return None
        elif e.e.code == 404:
            print('Encountered 404 Error (Not Found)')
            return None
        elif e.e.code == 429: 
            print('Encountered 429 Error (Rate Limit Exceeded)')
            if sleep_when_rate_limited:
                print("Retrying in 15 minutes...ZzZ...")
                sys.stderr.flush()
                time.sleep(60*15 + 5)
                print('...ZzZ...Awake now and trying again.')
                return 2
            else:
                raise e # Caller must handle the rate limiting issue
        elif e.e.code in (500, 502, 503, 504):
            print('Encountered {0} Error. Retrying in {1} seconds'\
                  .format(e.e.code, wait_period))
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e

    # End of nested helper function
    
    wait_period = 2 
    error_count = 0 

    while True:
        try:
            return twitter_api_func(*args, **kw)
        except twitter.api.TwitterHTTPError as e:
            error_count = 0 
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("URLError encountered. Continuing.")
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.")
                raise
        except BadStatusLine as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("BadStatusLine encountered. Continuing.")
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.")
                raise




def get_followers_ids(twitter_api, screen_name=None, user_id=None,
                              followers_limit=5000, cursor = -1):

    """
        Get a list of follwer ids for a given screen_name or user_id, 
        and a cursor value to the subsequent follower ids that are beyond the range 
        of followers_limit

        If no follwers_limit is sepcified, this function will return 5,000 followers 
        or the number of follwers that the given follwee has (which is less than 5,000)

        If no cursor value is specified, the most recent follower ids will be returned
        otherwise, the subsequent follwer ids that are pointed by cursor will be returned
    """


    # Must have either screen_name or user_id (logical xor)
    assert (screen_name != None) != (user_id != None), \
    "Must have screen_name or user_id, but not both"
    
    
    get_followers_ids = partial(make_twitter_request, twitter_api.followers.ids, 
                                count=5000)

    followers_ids = []
    
    for twitter_api_func, limit, ids, label in [
                    [get_followers_ids, followers_limit, followers_ids, "followers"]
                ]:
        
        if limit == 0: continue
        
        while cursor != 0:
        
            # Use make_twitter_request via the partially bound callable...
            if screen_name: 
                response = twitter_api_func(screen_name=screen_name, cursor=cursor)
            else: # user_id
                response = twitter_api_func(user_id=user_id, cursor=cursor)

            if response is not None:
                ids += response['ids']
                cursor = response['next_cursor']
                print("Cursor to next follower:", cursor)
            
            print('Fetched {0} total {1} ids for {2}'.format(len(ids),\
                  label, (user_id or screen_name)))
        
            if len(ids) >= limit or response is None:
                break

    # cursor: value of pointer to the subsequent followers
    # followers_ids: a list of follower ids
    return cursor, followers_ids