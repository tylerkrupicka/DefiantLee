import tweepy
import time
import threading
import nltk
from keys import keys

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


class Defiant:

    def __init__(self):
        #initialize class variables
        self.query = 'defiantly'
        self.count = 0
        self.tweets = []
        self.timerRunning = False
        self.ready = False
        self.delay = 120.0

    def main(self):
    	while True:
            #return tweets that contain the query
    		
    		 
    	

    def startTimer(self):
        t = Timer(self.delay,toggleReady)
        t.start()

    def toggleReady(self):
        if self.ready == False:
            self.ready == True
        else:
            self.ready == False

    def pollForTweets(self):
        currentPoll = api.search(q = query, rpp = 1)
        for tweet in currentPoll:
            tweet.text = tweet.text.lower()
        self.tweets.append(currentPoll)

    def postThanks(self):
        sn = tweet.user.screen_name
        message = "@%s " % (sn)
        message +=  "Thank you for your service"
        api.update_status(message,tweet.id)

        count += 1
        startTimer()
        print message + "  Count: " + str(count)

    def postCorrection(self, tweet):
        sn = tweet.user.screen_name
        message = "@%s " % (sn)
        message +=  "Did you mean definitely?"
        api.update_status(message,tweet.id)

        count += 1
        startTimer()
        print message + "  Count: " + str(count)



if __name__ == '__main__':
    Defiant().main()

	


