from GetFollowers import *
from TweetStore import TweetStore

twitter_api = oauth_login()

"""
t_cursor, t_followers_ids = get_followers_ids(twitter_api, screen_name="katyperry",
                                 followers_limit=10000)
"""

#print("Returned cursor:", t_cursor)
#print("Returned follower ids:",t_followers_ids[:5])


cursor, followers_ids = get_followers_ids(twitter_api, screen_name="katyperry",
                                 followers_limit=5000, cursor=1730734262261304917)

tweetStore = TweetStore()
#save followers offset
tweetStore.saveInfluencerFollowersOffset(str(cursor))

#save influencers follower ids
followers_idslist = []
for followers_id in followers_ids:
    followers_idslist.append({
        "_id": followers_id,
    })
tweetStore.saveInfluencerFollowers(followers_idslist)