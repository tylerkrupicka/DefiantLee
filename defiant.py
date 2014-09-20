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
        self.version = 1.5
        self.query = 'defiantly'
        self.count = 0
        self.tweets = []
        self.timerRunning = False
        self.ready = False
        self.delay = 120.0

    def main(self):
    	while True:
            if self.timerRunning == False:
                startTimer()
            pollForTweets()
            famous()
            if self.ready = True:
                self.timerRunning = False
                
                for tweet in self.tweets:
                    if "definitely" in tweet.text:
                        if("difference between" in tweet.text
                            or "hate" in tweet.text or "spell" in tweet.text
                                or "mean" in tweet.text or "differ" in tweet.text)
                            postThanks(tweet)
                    else:
                        postCorrection(tweet)

            timer.sleep(30)

    def startTimer(self):
        #start the timer and set to toggleReady after delay
        t = Timer(self.delay,toggleReady)
        self.timerRunning = True
        t.start()

    def toggleReady(self):
        #toggle ready to post depending on value
        if self.ready == False:
            self.ready == True
        else:
            self.ready == False

    def pollForTweets(self):
        #add the current pulling tweets with lowered text
        #to the array for processing for the next post
        currentPoll = api.search(q = query, rpp = 1)
        for tweet in currentPoll:
            tweet.text = tweet.text.lower()
        self.tweets.append(currentPoll)

    def postThanks(self,tweet):
        #post a thank you message to the user
        sn = tweet.user.screen_name
        if(len(tweet.text)+len(sn)<=97):
            message =  'Thank you for knowing the difference RT "'
        else:
            messege = 'Thank Youn RT "'                          
        message += "@%s " % (sn)
        message += tweet.text + ' "'        
        api.update_status(message,tweet.id)
        afterPost()


    def postCorrection(self, tweet):
        #post the standard correction message in reply
        #to the tweet
        sn = tweet.user.screen_name
        message = "@%s " % (sn)
        message +=  "Did you mean definitely?"
        api.update_status(message,tweet.id)
        afterPost()

    def afterPost(self):
        #add to count, reset the ready timer, print status,
        #reset tweets to analyze
        count += 1
        toggleReady()
        startTimer()
        print (message + "  Count: " + str(count) +
        " Version: " + str(self.version))
        self.tweets = []

    def famous(self)
        self.tweets = sorted(self.tweets, key=lambda tweet: tweet.user.followers_count)


if __name__ == '__main__':
    #run program main
    Defiant().main()
