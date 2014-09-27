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
        self.name = "@DefiantLee_"
        self.query = 'defiantly'
        self.count = 0
        self.tweets = []
        self.timerRunning = False
        self.ready = False
        self.delay = 90.0
        self.lastUsers = []
        self.record = 0
        self.recordHolder = " "
        self.corpusFile = "corpus.txt"
        self.correctFile = "correct.txt"
        self.recordFile = "records.txt"
        #swear words to NOT retweet
        self.swear = ["fuck","shit","bitch","ass"]
        self.incCorpus = []
        self.corCorpus = []
        self.taggedCorpus = []

    def main(self):
        while True:
            if self.timerRunning == False:
                self.ready = False
                self.startTimer()
            
            self.pollForTweets()
            self.famous()
            if self.ready == True or self.count == 0:
                #print len(self.tweets)
                for tweet in self.tweets:
                    if "definitely" in tweet.text:
                                if("difference between" in tweet.text
                                    or "hate" in tweet.text or "spell" in tweet.text
                                            or "mean" in tweet.text or "differ" in tweet.text):
                                    self.postThanks(tweet)
                                    break
                    else:
                        self.postCorrection(tweet)
                        break

            time.sleep(20)

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
        currentPoll = [status for status in tweepy.Cursor(api.search, q=self.query).items(20)]
        for tweet in currentPoll:
            tweet.text = tweet.text.lower()
            if tweet.user.screen_name in self.lastUsers:
                pass 
            elif hasattr(tweet, 'retweeted_status'):
                pass
            elif "rt @" in tweet.text:
                pass
            elif self.name in tweet.text:
                pass
            else:
                self.tweets.append(tweet)

    def postThanks(self,tweet):
        #post a thank you message to the user
        self.store(tweet.user.screen_name)
        sn = tweet.user.screen_name

        for word in self.swear:
            if word in tweet.text:
                tweet.text.replace(word, "*")

        if(len(tweet.text)+len(sn)<=70):
            message =  'Thank you for knowing the difference RT "'
        else:
            message = 'Thank You RT "'                          
        message += "@%s " % (sn)
        message += tweet.text + ' "'
        message = message[0:140]        
        api.update_status(message,tweet.id)
        self.afterPost(message)


    def postCorrection(self, tweet):
        #post the standard correction message in reply
        #to the tweet
        self.store(tweet.user.screen_name)
        sn = tweet.user.screen_name
        message = "@%s " % (sn)

        f = open(self.corpusFile, 'a')
        save =  message + tweet.text + ' \n'
        f.write(save.encode('utf8')) 
        f.close()

        message +=  "Did you mean definitely?"
        api.update_status(message,tweet.id)

        self.afterPost(message)

    def afterPost(self, message):
        #add to count, reset the ready timer, print status,
        #reset tweets to analyze
        self.count += 1
        self.ready = False
        print (message + "  Count: " + str(self.count) + " Record: " + str(self.record) + " Holder: " + str(self.recordHolder))
        self.tweets = []
        self.tweetsText = []
        self.timerRunning = False

    def famous(self):
        self.tweets = sorted(self.tweets, key=lambda tweet: tweet.user.followers_count, reverse=True)
        best = self.tweets[0]
        if best.user.followers_count > self.record:
            self.record = best.user.followers_count
            self.recordHolder = best.user.screen_name

        if best.user.followers_count > 100000 and best.user.screen_name not in self.lastUsers:
            save = best.user.screen_name + " Followers: " + str(best.user.followers_count) + "\n"
            f = open(self.recordFile, 'a')
            f.write(save.encode('utf8'))
            f.close()

    def store(self,user):
        self.lastUsers.append(user)
        self.lastUsers = self.lastUsers[0:100]

    def createData(self):
        #read incorrect corpus
        c = open(self.corpusFile)
        inc = c.readlines()
        c.close

        #remove special characters, users, and newlines
        for line in inc:
            #clean characters
            valid_chars = ' @abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            line = ''.join(c for c in line if c in valid_chars)
            line = line.strip()
            #save to incorrect corpus
            if len(line) != 0 or len(line != 1:
                sp = line.split()
                self.incCorpus.append(sp)
            #remove user names
            for sentence in self.incCorpus:
                for word in sentence:
                    if word[0] == "@":
                        sentence.remove(word)

        #correct tweets
        c = open(self.correctFile)
        cor = c.readlines()
        c.close

        #remove special characters, users, and newlines
        for line in cor:
            #clean characters
            valid_chars = ' @abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            line = ''.join(c for c in line if c in valid_chars)
            line = line.strip()
            #save to incorrect corpus
            if len(line) != 0 or len(line != 1:
                sp = line.split()
                self.corCorpus.append(sp)
            #remove user names
            for sentence in self.corCorpus:
                for word in sentence:
                    if word[0] == "@":
                        sentence.remove(word)


    def generateFeatures(self,tweet):
        index = 0
        features = {}
        #get index
        for i in range(len(tweet)):
            if tweet[i] == "self.query":
                index = i
        #previous word feature
        if index != 0:
            previousWord = tweet[index-1]
            features['previousWord'] = previousWord
            #previous letter
            feaures[previousWordEndL] = previousWord[-1]
        else:
            features['previousWord'] = "none"
        
        #next word feature
        if index != len(tweet)-1:
            nextWord = tweet[index+1]
            features['nextWord'] = nextWord
            feaures[nextWordEndL] = nextWord[-1]
        else:
            features['nextWord'] = "none"

        return features



if __name__ == '__main__':
    #run program main
    Defiant().createData()
