from google.appengine.ext import ndb

class TweetDetail(ndb.Model):
    newTweets = ndb.StringProperty(repeated=True)
