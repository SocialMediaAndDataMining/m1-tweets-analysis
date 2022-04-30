from GetFollowers import *
from TweetStore import TweetStore

tweetStore = TweetStore()
twitter_api = oauth_login()

for idx in range(0, 5):
    # Retrieve the cursor (offset) to the subsequent follower ids
    followers_offset = tweetStore.getInfluencerFollowersOffset()

   #
   # ************************
   # NEED TO CHANGE "katyperry" TO THE ACTUAL INFLUENCER WE ARE INTERESTED IN
   # ************************
   #

    # Get a list of follower ids and next cursor value (offset)
    next_followers_cursor, followers_ids = get_followers_ids(twitter_api, screen_name="katyperry",
                                 followers_limit=5000, cursor=followers_offset)

    # Save followers offset into database
    tweetStore.saveInfluencerFollowersOffset(str(next_followers_cursor))

    # Save influencers follower ids into database
    followers_idslist = []
    for followers_id in followers_ids:
        followers_idslist.append({
            "_id": followers_id,
        })

    tweetStore.saveInfluencerFollowers(followers_idslist)

