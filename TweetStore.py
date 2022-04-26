import pymongo

class TweetStore:
    allOffsetId = "ALL_TWEETS"
    influencerOffsetId = "INFLUENCER_TWEETS"
    followersOffsetId = "INFLUENCER_FOLLOWERS"
    def __init__(self):
        client = pymongo.MongoClient("mongodb+srv://smdm:8udib9AXCH7-xR3@cluster0.heice.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client['M1_analysis']
        self.allTweetsCollection = db['all_tweets']
        self.influencerTweetsCollection = db['influencer_tweets']
        self.tweetsOffsetCollection = db['tweets_offset']
        self.influencerFollowersCollection = db['influencer_followers']

    def getAllM1Tweets(self):
        return self.allTweetsCollection.find({})

    def saveAllM1Tweets(self, tweets):
        self.allTweetsCollection.insert_many(tweets)

    def getAllTweetsOffset(self):
        return self.tweetsOffsetCollection.find({"_id": self.allOffsetId})

    def saveAllTweetsOffset(self, offset):
        dataToSave = {"_id": self.allOffsetId, "offset": offset}
        self.tweetsOffsetCollection.replace_one({"_id": self.allOffsetId}, dataToSave)

    def getInfluencerM1Tweets(self):
        return self.influencerTweetsCollection.find({})

    def saveInfluencerM1Tweets(self, tweets):
        self.influencerTweetsCollection.insert_many(tweets)

    def getInfluencerTweetsOffset(self):
        return self.tweetsOffsetCollection.find({"_id": self.influencerOffsetId})

    def saveInfluencerTweetsOffset(self, offset):
        dataToSave = {"_id": self.influencerOffsetId, "offset": offset}
        self.tweetsOffsetCollection.replace_one({"_id": self.allOffsetId}, dataToSave)

    def getInfluencerFollowers(self):
        return self.influencerFollowersCollection.find({})

    def saveInfluencerFollowers(self, tweets):
        self.influencerFollowersCollection.insert_many(tweets)

    def getInfluencerFollowersOffset(self):
        return self.tweetsOffsetCollection.find({"_id": self.followersOffsetId})

    def saveInfluencerFollowersOffset(self, offset):
        dataToSave = {"_id": self.followersOffsetId, "offset": offset}
        self.tweetsOffsetCollection.replace_one({"_id": self.allOffsetId}, dataToSave)