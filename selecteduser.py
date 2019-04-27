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

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape = True
)

class SelectedUser(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        searchedUserName = self.request.get('username')

        if searchedUserName == None or searchedUserName == '':
            self.redirect('/')
            return

        tweetKey = ndb.Key('TweetDetail', searchedUserName)
        tweetdetail = tweetKey.get()

        logging.info(tweetdetail)

        template_values = {
            'tweetdetail': tweetdetail
        }
        template = JINJA_ENVIRONMENT.get_template('selecteduser.html')
        self.response.write(template.render(template_values))
