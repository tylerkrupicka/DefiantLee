DefiantLee
==========

A twitter bot for helping people see if they typed "defiantly" when they meant definitely. The bot uses NLTK to create a Naive Bayes machine learning classifier to determine use correctness. Features for analysis are nearby words, as well as comparison using part of speech tagging. 

Uses:
Python 2.7
Tweepy
NLTK

Looks for uses of the word defiantly that are in places when definitely would normally be used, and chooses one every time interval to reply to and let them know.

https://twitter.com/DefiantLee_/with_replies

Writeup: http://tylerkrupicka.com/blog/Defiant-Lee-A-Naive-Bayes-Twitter-Bot.html

So this bot had its API key removed - I decided to transfer some of the machine learning and corpus over to a site that displays misuse. Now running on defiantly.me.

Writeup: http://tylerkrupicka.com/blog/defiantly.me.html
