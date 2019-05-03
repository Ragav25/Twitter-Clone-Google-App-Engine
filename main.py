import os
import webapp2
import jinja2
import difflib
import logging
from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime

# import sys
# sys.path.insert(0, 'python_scripts')

from userdetail import UserDetail
from tweetdetail import TweetDetail
from edituserdetail import EditUserDetail
from displayuserdetail import DisplayUserDetail
from usernamelist import UserNameList
from searchresults import SearchResults
from selecteduser import SelectedUser
from searchtweet import SearchTweet
# from searchmechanism import SearchMechanism
# from tweetpage import TweetPage

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape = True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # checking if usernames list is already created if not create one.
        userNamesKey = ndb.Key('UserNameList', 'common')
        userNamesList = userNamesKey.get()

        if userNamesList == None:
            userNamesList = UserNameList(id='common')
            userNamesList.put()

        user = users.get_current_user()
        if user == None:
            template_values = {
            'login_url': users.create_login_url(self.request.uri)
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            return

        key = ndb.Key('UserDetail', user.user_id())
        userdetail = key.get()

        if userdetail == None or userdetail.userName == None:
            userdetail = UserDetail(id=user.user_id())
            userdetail.put()

            template_values = {
                'user': user,
                'logout_url': users.create_logout_url(self.request.uri),
                'userdetail': userdetail,

                }

            template = JINJA_ENVIRONMENT.get_template('userdetail.html')
            self.response.write(template.render(template_values))

        else:
            key = ndb.Key('UserDetail', user.user_id())
            userdetail = key.get()

            tweetKey = ndb.Key('TweetDetail', userdetail.userName)
            tweetdetail = tweetKey.get()

            logging.info('###')
            logging.info(tweetdetail.followingUser)

            userNamesKey = ndb.Key('UserNameList', 'common')
            userNamesList = userNamesKey.get()

            template_values = {
                'user': user,
                'logout_url': users.create_logout_url(self.request.uri),
                'userdetail': userdetail,
                'tweetdetail' : tweetdetail,
                'names': None
                }
            template = JINJA_ENVIRONMENT.get_template('tweetpage.html')
            self.response.write(template.render(template_values))


    def post(self):
        action = self.request.get('button')
        user = users.get_current_user()

        key = ndb.Key('UserDetail', user.user_id())
        userdetail = key.get()

        userNamesKey = ndb.Key('UserNameList', 'common')
        userNamesList = userNamesKey.get()

        if userdetail != None and userdetail.userName != None:
            tweetKey = ndb.Key('TweetDetail', userdetail.userName)
            tweetdetail = tweetKey.get()

        if action == 'Enter':
            userName = self.request.get('userName')
            userName = str(userName)

            tweetsKey = ndb.Key('TweetDetail', userName)
            tweets = tweetsKey.get()


            if tweets == None:
                userNamesList.userNames.append(userName)
                logging.info('%%%')
                logging.info(userNamesList.userNames)

                userdetail.userName = self.request.get('userName')
                userdetail.put()
                tweetdetail = TweetDetail(id=userdetail.userName)
                tweetdetail.put()
                userNamesList.put()

                self.redirect('/')
            else:
                # To do..!!
                self.redirect('/')


        elif action == 'Tweet':
            # key = ndb.Key('UserDetail', user.user_id())
            userdetail =  ndb.Key('UserDetail', user.user_id()).get()

            tweetFetch = self.request.get('newTweet')

            if tweetFetch == None or tweetFetch == '':
                self.redirect('/')
                return

            tweetdetail.newTweets.append(tweetFetch)

            tweetdetail.put()

            self.redirect('/')

        elif action == 'Search':
            userSearchOutput = self.request.get('output')
            self.redirect('/searchresults?searchterm='+ userSearchOutput)

        elif action == 'Tweet Search':
            tweetSearchOutput = self.request.get('tweetsearch')
            self.redirect('/searchtweet?tweetSearchOutput='+ tweetSearchOutput)



app = webapp2.WSGIApplication([ ('/', MainPage),
('/edituserdetail', EditUserDetail),
('/displayuserdetail', DisplayUserDetail),
('/searchresults', SearchResults),
('/selecteduser', SelectedUser),
('/searchtweet', SearchTweet)], debug = True)
