import pymongo

class TweetStore:
    allOffsetId = "ALL_TWEETS"
    influencerOffsetId = "INFLUENCER_TWEETS"
    followersOffsetId = "INFLUENCER_FOLLOWERS"
    followersOffsetId1000 = "INFLUENCER_FOLLOWERS1000"
    followersOffsetId2000 = "INFLUENCER_FOLLOWERS2000"

    def __init__(self):
        client = pymongo.MongoClient("mongodb+srv://smdm:8udib9AXCH7-xR3@cluster0.heice.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client['M1_analysis']
        self.allTweetsCollection = db['all_tweets']
        self.influencerTweetsCollection = db['influencer_tweets']
        self.tweetsOffsetCollection = db['tweets_offset']
        self.influencerFollowersCollection = db['influencer_followers']

    def getAllM1Tweets(self):
        tweets = self.allTweetsCollection.find({})
        only_tweets = []

        for tweet in tweets:
            new_tweet = {
                'user_screen_name' : tweet['user']['screen_name'],
                'user_id' : tweet['user']['id'],
                'text' : tweet['text']
            }
            only_tweets.append(new_tweet)
        
        return only_tweets

    def saveAllM1Tweets(self, tweets):
        self.allTweetsCollection.insert_many(tweets)

    def getAllTweetsOffset(self):
        return self.tweetsOffsetCollection.find_one({"_id": self.allOffsetId})['offset']

    def saveAllTweetsOffset(self, offset):
        dataToSave = {"_id": self.allOffsetId, "offset": offset}
        self.tweetsOffsetCollection.replace_one({"_id": self.allOffsetId}, dataToSave)

    def getInfluencerM1Tweets(self):
        tweets = self.influencerTweetsCollection.find({})
        only_tweets = []

        for tweet in tweets:
            new_tweet = {
                'user_screen_name': tweet['user']['screen_name'],
                'user_id': tweet['user']['id'],
                'text': tweet['text']
            }
            only_tweets.append(new_tweet)

        return only_tweets

    def saveInfluencerM1Tweets(self, tweets):
        self.influencerTweetsCollection.insert_many(tweets)

    def getInfluencerTweetsOffset(self):
        return self.tweetsOffsetCollection.find_one({"_id": self.influencerOffsetId})['offset']

    def saveInfluencerTweetsOffset(self, offset):
        dataToSave = {"_id": self.influencerOffsetId, "offset": offset}
        self.tweetsOffsetCollection.replace_one({"_id": self.influencerOffsetId}, dataToSave)

    def getInfluencerFollowers(self):
        return self.influencerFollowersCollection.find({})

    def saveInfluencerFollowers(self, tweets):
        self.influencerFollowersCollection.insert_many(tweets)

    def getInfluencerFollowersOffset(self):
        return self.tweetsOffsetCollection.find_one({"_id": self.followersOffsetId})['offset']

    def saveInfluencerFollowersOffset(self, offset):
        dataToSave = {"_id": self.followersOffsetId, "offset": offset}
        self.tweetsOffsetCollection.replace_one({"_id": self.followersOffsetId}, dataToSave)

    def getInfluencerFollowersOffset1000(self):
        return self.tweetsOffsetCollection.find_one({"_id": self.followersOffsetId1000})['offset']

    def saveInfluencerFollowersOffset1000(self, offset):
        dataToSave = {"_id": self.followersOffsetId, "offset": offset}
        self.tweetsOffsetCollection.replace_one({"_id": self.followersOffsetId1000}, dataToSave)

    def getInfluencerFollowersOffset2000(self):
        return self.tweetsOffsetCollection.find_one({"_id": self.followersOffsetId2000})['offset']

    def saveInfluencerFollowersOffset2000(self, offset):
        dataToSave = {"_id": self.followersOffsetId, "offset": offset}
        self.tweetsOffsetCollection.replace_one({"_id": self.followersOffsetId2000}, dataToSave)