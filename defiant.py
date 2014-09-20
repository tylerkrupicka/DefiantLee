import tweepy
import time
from keys import keys

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

query = "defiantly"
count = 0

while True:

	defiant_tweets = api.search(q = query, rpp = 1)


	tweet = defiant_tweets[0]
	sn = tweet.user.screen_name
	message = "@%s " % (sn)
	if "definitely" in tweet.text:
		message += "Thank you for your service"
	else:
		message +=  "Did you mean definitely?"
		
	api.update_status(message,tweet.id)
	count += 1
	print message + "  Count: " + str(count) 
	

	time.sleep(240)

	


