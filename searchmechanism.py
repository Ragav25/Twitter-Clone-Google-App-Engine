import os
import webapp2
import jinja2
import logging
import difflib
from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime

from userdetail import UserDetail
from tweetdetail import TweetDetail
from usernamelist import UserNameList

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape = True
)

class SearchMechanism(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        searchOutput = self.request.get('output')

        userNamesKey = ndb.Key('UserNameList', 'common')
        userNamesList = userNamesKey.get()

        if userNames == None:
            userNames = UserNameList(id='common')
            userNames.put()

        output = difflib.get_close_matches(searchOutput, userNamesList.userNames)

        template_values = {
        'userNames': userNamesList,
        'names': output,
        'searchedNames': None
        }

        template = JINJA_ENVIRONMENT.get_template('tweetpage.html')
        self.response.write(template.render(template_values))

    def post(self):
        action = self.request.get('button')
        user = users.get_current_user()

        userNamesKey = ndb.Key('UserNameList', 'common')
        userNamesList = userNamesKey.get()

        if action == 'Search':

            searchOutput = self.request.get('output')

            searchedNames = None

            output = difflib.get_close_matches(searchOutput, userNamesList.userNames)
            searchedNames = output
            logging.info('@@@@')
            logging.info(searchedNames)

            for item in userNamesList.userNames:
                if item == searchOutput:
                    matchedUserName = str(item)
                    url = '/?searchOutput=' + searchOutput
                    logging.info("!!! " + item)
                    self.redirect(url)
                    return
            logging.info('No User Found')
            url = '/?searchOutput=' + searchOutput
            self.redirect('url')

        template_values = {
        'userNames': userNamesList,
        'names': output,
        'searchedNames': None
        }

        template = JINJA_ENVIRONMENT.get_template('tweetpage.html')
        self.response.write(template.render(template_values))
