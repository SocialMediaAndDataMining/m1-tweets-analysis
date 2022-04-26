from turtle import update
from TweetStore import TweetStore

"""
Install the following packages - 
Pip install Pymongo
Pip install ‘pymongo[srv]’

When running this if there is an which returns a certificate error after running for more
than the expected running time -
The fix is to manually install in the certificate store the "ISRG Root X1" and "ISRG Root X2" root certificates, 
and the "Let’s Encrypt R3" intermediate one - link to their official site - https://letsencrypt.org/certificates/
Download the .der field from the 1st category, download, double click and follow the wizard to install it.

This python file shows the usage of the TweetStore.
"""
if __name__ == "__main__":
    tweetStore = TweetStore()

    allM1Tweets = tweetStore.getAllM1Tweets()
    print("All M1 Tweets - ")
    for tweet in allM1Tweets:
        print(tweet)
    
    tweetStore.saveAllTweetsOffset("1")

    print("All tweet offset- ")
    print(tweetStore.getAllTweetsOffset()[0])