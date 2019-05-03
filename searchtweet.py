import os
import webapp2
import jinja2
import difflib
import logging
from google.appengine.api import users
from google.appengine.ext import ndb

from userdetail import UserDetail
from tweetdetail import TweetDetail
from edituserdetail import EditUserDetail
from displayuserdetail import DisplayUserDetail
from usernamelist import UserNameList
from searchutils import getAllMatchedTweets

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape = True
)

class SearchTweet(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        searchTweet = self.request.get('tweetSearchOutput')
        if searchTweet == None:
            self.redirect('/')

        userNamesKey = ndb.Key('UserNameList', 'common')
        userNamesList = userNamesKey.get()

        matchedTweets = []
        # tweets2 = []

        for userName in userNamesList.userNames:
            logging.info("{}{}{}")
            logging.info(userName)
            tweetDetails = ndb.Key('TweetDetail', userName).get()
            for x in tweetDetails.newTweets:
                if searchTweet.lower() in x.lower():
                    logging.info('[][]')
                    logging.info(x)
                    matchedTweets.append(x)

                    template_values = {
                        'username': userName,
                        'x': x
                    }

                    template = JINJA_ENVIRONMENT.get_template('searchtweet.html')
                    self.response.write(template.render(template_values))
