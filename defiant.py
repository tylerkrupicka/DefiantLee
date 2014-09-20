import tweepy
import time
import timeit
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


    def main(self):
    	while True:
            #return tweets that contain the query
    		
    		sn = tweet.user.screen_name
    		message = "@%s " % (sn)
    		if "definitely" in tweet.text:
    			message += "Thank you for your service"
    		else:
    			message +=  "Did you mean definitely?"
    			
    		api.update_status(message,tweet.id)
    		count += 1
    		print message + "  Count: " + str(count) 
    		

    		time.sleep(120)

    def ready(self):

    def pollForTweets(self):
        currentPoll = api.search(q = query, rpp = 1)
        for tweet in currentPoll:
            tweet.text = tweet.text.lower()
        self.tweets.append(currentPoll)

if __name__ == '__main__':
    Defiant().main()

	


