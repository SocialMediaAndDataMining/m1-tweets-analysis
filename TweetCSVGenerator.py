from TweetStore import TweetStore
import csv

def generate_csv_for_all_tweets():
    tweetStore = TweetStore()
    with open('allM1Tweets.csv', 'w', encoding="utf-8") as csvf:
        wri = csv.writer(csvf)
        wri.writerow(["user_name", "user_id", "text"])

        for item in tweetStore.getAllM1Tweets():
            # result =
            result = [item['user_screen_name'], item['user_id'], item['text']]
            wri.writerow(result)

    csvf.close()


def generate_csv_for_influencer_tweets():
    tweetStore = TweetStore()
    with open('influencerM1Tweets.csv', 'w', encoding="utf-8") as csvf:
        wri = csv.writer(csvf)
        wri.writerow(["user_name", "user_id", "text"])

        for item in tweetStore.getInfluencerM1Tweets():
            # result =
            result = [item['user_screen_name'], item['user_id'], item['text']]
            wri.writerow(result)

    csvf.close()

generate_csv_for_all_tweets()
# generate_csv_for_influencer_tweets()