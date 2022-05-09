# m1-tweets-analysis
Analyzing tweets about Apple M1 processor for positive and negative reviews


## packages you may need - append more packages here if you need

```
>> pip install dotenv tweepy pymongo "pymongo[srv]"
```

## create a .env file for dotenv module
```
CONSUMER_KEY=""
CONSUMER_SECRET=""
OAUTH_TOKEN=""
OAUTH_TOKEN_SECRET=""
```
Following python files to be run in a sequential order - 
1. AllTweetsFetcher.py - This downloads the tweets about M1 stores them in the Tweetstore(MongoDB)
2. GetFollowers.py - This downloads the followers of the given user and stores them in the Tweetstore(MongoDB)
3. GetFollowerTweets.py - This loops through each of the follower and downloads their tweets aobut M1 and stores those into the Tweetstore(MongoDB)
4. TweetCSVGenerator.py - This gets the tweets from the Tweetstore and generates the CSV for both all M1 and influencer followers' tweets.
5. M1_Tweets_NLTK_SA.ipynb - This reads the CSV files generated above and analyses using NLTK

The system running these will need access to the DB which is hosted on MongoDB atlas.
The ip address of this system is therefore required to add to the list of network access.

Request read access to the project by emailing bhattrahul712@gmail.com.
