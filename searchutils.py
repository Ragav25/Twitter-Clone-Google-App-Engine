from google.appengine.api import users
from google.appengine.ext import ndb
import difflib
import logging

from userdetail import UserDetail
from tweetdetail import TweetDetail
from usernamelist import UserNameList

def getAllMatchedTweets(keywordToMatch):
    userNamesKey = ndb.Key('UserNameList', 'common')
    userNamesList = userNamesKey.get()

    matchedTweets = []
    # tweets2 = []

    for userName in userNamesList.userNames:
        logging.info("{}{}{}")
        logging.info(userName)
        tweetDetails = ndb.Key('TweetDetail', userName).get()
        # matchedTweetsForUser = difflib.get_close_matches(keywordToMatch, tweetDetails.newTweets)
        for x in tweetDetails.newTweets:
            if keywordToMatch.lower() in x.lower():
                logging.info('[][]')
                logging.info(x)
                matchedTweets.append(x)

    return matchedTweets
