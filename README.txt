purpose of function get_valid_tweets(influencer_name, followers_limit, first_load_limit, reload_limit, hashtag):
get valid tweets (tweets include hashtag which specified by parameter hashtag), from follower IDs, which are provided by 
get_followers_ids(au_api, screen_name=influencer_name, followers_limit=first_load_limit)
get_followers_ids(au_api, screen_name=influencer_name, followers_limit=reload_limit, t_cursor)

1. please use your own four keys (CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN
OAUTH_TOKEN_SECRET) in function oauth_login()

2. please run this program, get_valid_tweets_test will be called, which would show output of
get_valid_tweets

3. uncomment function get_valid_tweets, which is ONLY function you should care. 
Detailed instruction is provided above the function

4. import 
get_followers_ids(au_api, screen_name=influencer_name, followers_limit=first_load_limit)
get_followers_ids(au_api, screen_name=influencer_name, followers_limit=reload_limit, t_cursor)