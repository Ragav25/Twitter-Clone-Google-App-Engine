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
class SearchResults(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        searchTerm = self.request.get('searchterm')
        if searchTerm == None:
            self.redirect('/')
        userNamesList = ndb.Key('UserNameList', 'common').get()
        names = difflib.get_close_matches(searchTerm, userNamesList.userNames)
        names = [str(x) for x in names]
        template_values = {
            'names': names,
            'namelength': len(names),
            'searchterm': searchTerm
        }
        template = JINJA_ENVIRONMENT.get_template('searchresults.html')
        self.response.write(template.render(template_values))
