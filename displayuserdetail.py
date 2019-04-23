import os
import webapp2
import jinja2
import logging
from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime

from userdetail import UserDetail

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape = True
)

class DisplayUserDetail(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        key = ndb.Key('UserDetail', user.user_id())
        userdetail = key.get()

        template_values = {
            'user': user,
            'userdetail': userdetail
            }

        template = JINJA_ENVIRONMENT.get_template('displayuserdetail.html')
        self.response.write(template.render(template_values))

    def post(self):
        action = self.request.get('button')

        if action == 'Edit':
            self.redirect('/edituserdetail')
