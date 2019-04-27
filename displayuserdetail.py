import os
import webapp2
import jinja2
import logging
from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime
from tweetdetail import TweetDetail

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape = True
)

class DisplayUserDetail(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        userKey = ndb.Key('UserDetail', user.user_id())
        userdetail = userKey.get()

        key = ndb.Key('TweetDetail', userdetail.userName)
        tweetdetail = key.get()

        template_values = {
            'user': user,
            'tweetdetail': tweetdetail,
            'userdetail': userdetail
            }

        path = 'displayuserdetail.html'

        template = JINJA_ENVIRONMENT.get_template(path)
        self.response.write(template.render(template_values))

    def post(self):
        action = self.request.get('button')

        if action == 'Edit':
            self.redirect('/edituserdetail')
