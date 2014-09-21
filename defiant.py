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
        self.last = []
        self.record = 0

    def main(self):
    	while True:
            if self.timerRunning == False:
                self.ready = False
                self.startTimer()
            self.pollForTweets()
            self.famous()
            if self.ready == True or self.count == 0:
                for tweet in self.tweets:
                    if tweet.text not in self.last:
                        if "definitely" in tweet.text:
                            if("difference between" in tweet.text
                                or "hate" in tweet.text or "spell" in tweet.text
                                    or "mean" in tweet.text or "differ" in tweet.text):
                                self.postThanks(tweet)
                                break
                        else:
                            self.postCorrection(tweet)
                            break

            time.sleep(15)

    def startTimer(self):
        #start the timer and set to toggleReady after delay
        t = threading.Timer(self.delay,self.setReady)
        self.timerRunning = True
        t.daemon = True
        t.start()

    def setReady(self):
        #toggle ready to post depending on value
            self.ready = True

    def pollForTweets(self):
        #add the current pulling tweets with lowered text
        #to the array for processing for the next post
        currentPoll = api.search(q = self.query, rpp = 100)
        for tweet in currentPoll:
            tweet.text = tweet.text.lower()
            self.tweets.append(tweet)
        print len(self.tweets)
        self.tweets = self.tweets[0:100]

    def postThanks(self,tweet):
        #post a thank you message to the user
        self.store(tweet.text)
        sn = tweet.user.screen_name
        if(len(tweet.text)+len(sn)<=97):
            message =  'Thank you for knowing the difference RT "'
        else:
            message = 'Thank Youn RT "'                          
        message += "@%s " % (sn)
        message += tweet.text + ' "'        
        api.update_status(message,tweet.id)
        self.afterPost(message)


    def postCorrection(self, tweet):
        #post the standard correction message in reply
        #to the tweet
        self.store(tweet.text)
        sn = tweet.user.screen_name
        message = "@%s " % (sn)
        message +=  "Did you mean definitely?"
        api.update_status(message,tweet.id)
        self.afterPost(message)

    def afterPost(self, message):
        #add to count, reset the ready timer, print status,
        #reset tweets to analyze
        self.count += 1
        self.ready = False
        print (message + "  Count: " + str(self.count) + " Record: " + str(self.record))
        self.tweets = []
        self.timerRunning = False

    def famous(self):
        self.tweets = sorted(self.tweets, key=lambda tweet: tweet.user.followers_count, reverse=True)
        best = self.tweets[0]
        if best.user.followers_count > self.record:
            self.record = best.user.followers_count

    def store(self,tweet):
        self.last.append(tweet)
        self.last = self.last[0:100]

if __name__ == '__main__':
    #run program main
    Defiant().main()
