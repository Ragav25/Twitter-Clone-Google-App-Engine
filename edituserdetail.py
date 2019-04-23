import os
import jinja2
import webapp2
import logging
# import re
from google.appengine.api import users
from google.appengine.ext import ndb

from datetime import datetime

from userdetail import UserDetail
from tweetdetail import TweetDetail

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape = True
)

class EditUserDetail(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        key = ndb.Key('UserDetail', user.user_id())
        userdetail = key.get()

        template_values ={
        'user': user,
        'userdetail': userdetail
        }

        template = JINJA_ENVIRONMENT.get_template('edituserdetail.html')
        self.response.write(template.render(template_values))

    def post(self):
        action = self.request.get('button')
        user = users.get_current_user()

        if action == 'Cancel':
            self.redirect('/')

        elif action == 'Update':
            key = ndb.Key('UserDetail', user.user_id())
            userdetail = key.get()

            userdetail.dateOfBirth = datetime.strptime(self.request.get('dateOfBirth'), '%Y-%m-%d')
            userdetail.shortProfile = self.request.get('shortProfile')
            logging.info('&&&***')
            logging.info(userdetail.dateOfBirth)
            userdetail.put()

            self.redirect('/displayuserdetail')
