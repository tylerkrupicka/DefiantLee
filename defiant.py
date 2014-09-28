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
        self.determiners = ["difference between","hate","spell","mean", "differ"]
        self.incCorpus = []
        self.corCorpus = []
        self.taggedCorpus = []
        self.classifier = ""

    def main(self):
        print "loading corpus and creating classifier"
        self.createClassifier()
        print "Checking accuracy"
        print "tested accuracy: " + str((nltk.classify.accuracy(self.classifier, self.taggedCorpus)))
        
        while True:
            if self.timerRunning == False:
                self.ready = False
                self.startTimer()
            
            self.pollForTweets()
            self.famous()
            if self.ready == True or self.count == 0:
                self.decideTweet()

            time.sleep(20)

    def decideTweet(self):
        #in case of empty list
        while len(self.tweets) == 0:
            self.pollForTweets()
            time.sleep(30)

        for tweet in self.tweets:
            if tweet.user.screen_name not in self.lastUsers:                
                if "definitely" in tweet.text:
                    for term in self.determiners():
                        if term in tweet.text:
                            self.postThanks(tweet)
                            break
                else:
                    self.postCorrection(tweet)
                    break

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
        try:
            currentPoll = [status for status in tweepy.Cursor(api.search, q=self.query).items(20)]
        except tweepy.TweepError, e:
            print 'poll failed because of %s' % e.reason
    
        for tweet in currentPoll:
            tweet.text = tweet.text.lower()
            clean = self.cleanText(tweet.text)
            clean = clean.split()
            
            if self.classifier.classify(self.generateFeatures(clean)) == 'correct':
                pass
            elif tweet.user.screen_name in self.lastUsers:
                pass 
            elif hasattr(tweet, 'retweeted_status'):
                pass
            elif "rt @" in tweet.text or " rt " in tweet.text:
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
            message = 'Definitely. RT "'                          
        message += "@%s " % (sn)
        message += tweet.text + ' "'
        message = message[0:140]        
        
        try:
            api.update_status(message,tweet.id)
        except tweepy.TweepError, e:
            print 'thanks failed because of %s' % e.reason
            if len(self.tweets) != 0:
                self.tweets = self.tweets[1:]
                self.decideTweet()
        
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
        
        try:
            api.update_status(message,tweet.id)
        except tweepy.TweepError, e:    
            print 'correction failed because of %s' % e.reason
            if len(self.tweets) != 0:
                self.tweets = self.tweets[1:]
            self.decideTweet()

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
    #print self.lastUsers

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
            if len(line) != 0 and len(line) != 1:
                sp = line.split()
                if len(sp) == 0 or len(sp) == 1:
                    pass
                else:
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
            if len(line) != 0 and len(line) != 1:
                sp = line.split()
                if len(sp) == 0 or len(sp) == 1:
                    pass
                else:
                    self.corCorpus.append(sp)
            #remove user names
            for sentence in self.corCorpus:
                for word in sentence:
                    if word[0] == "@":
                        sentence.remove(word)

    def cleanText(self,text):
        valid_chars = ' @abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        text = ''.join(c for c in text if c in valid_chars)
        text = text.strip()
        #remove user names
        sent = text.split()
        for word in sent:
            if word[0] == "@":
                sent.remove(word)
        clean = " "
        return clean.join(sent)    

    def generateFeatures(self,tweet):
        index = 0
        features = {}
        #get index
        for i in range(0,len(tweet)):
            if tweet[i] == self.query:
                index = i
        pos = nltk.pos_tag(tweet)
        #previous word feature
        if index != 0:
            previousWord = tweet[index-1]
            token = pos[index-1]
            features['previousWord'] = previousWord
            #previous letter
            features['previousWordEndL'] = previousWord[-1]
            features['previousWordPos'] = token[1]
        else:
            features['previousWord'] = "none"
            features['previousWordEndL'] = "none"
            features['previousWordPos'] = "none"
        
        #next word feature
        if index < len(tweet)-1:
            #print str(index) + " " + str(len(tweet))
            nextWord = tweet[index + 1]
            token = pos[index+1]
            features['nextWord'] = nextWord
            features['nextWordEndL'] = nextWord[-1]
            features['nextWordPos'] = token[1]
        else:
            features['nextWord'] = "none"
            features['nextWordEndL'] = "none"
            features['nextWordPos'] = "none"

        return features

    def createClassifier(self):
        self.createData()
        #create training corpus
        for tweet in self.incCorpus:
            self.taggedCorpus.append((self.generateFeatures(tweet),'incorrect'))
        for tweet in self.corCorpus:
            self.taggedCorpus.append((self.generateFeatures(tweet),'correct'))  

        self.classifier = nltk.NaiveBayesClassifier.train(self.taggedCorpus)

    def testClassifier(self):
        self.createClassifier()
        print "tested accuracy: " + str((nltk.classify.accuracy(self.classifier, self.taggedCorpus)))
        while True:
            phrase = ""
            phrase = raw_input("Enter Phrase to Classify: ")
            phrase = phrase.split()
            print phrase
            print self.classifier.classify(self.generateFeatures(phrase))

if __name__ == '__main__':
    #run program main
    Defiant().main()
