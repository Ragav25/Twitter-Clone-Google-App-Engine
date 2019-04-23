import os
import webapp2
import jinja2
import logging
from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime

from userdetail import UserDetail
from tweetdetail import TweetDetail
from edituserdetail import EditUserDetail
from displayuserdetail import DisplayUserDetail
from usernamelist import UserNameList
# from tweetpage import TweetPage

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape = True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        userNamesKey = ndb.Key('UserNameList', 'common')
        userNames = userNamesKey.get()

        if userNames == None:
            userNames = UserNameList(id='common')
            userNames.put()

        if user == None:
            template_values = {
            'login_url': users.create_login_url(self.request.uri)
            }

            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            return

        key = ndb.Key('UserDetail', user.user_id())
        userdetail = key.get()

        # tweetKey = ndb.Key('TweetDetail', userdetail.userName)
        # tweetdetail = tweetKey.get()

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

            template_values = {
                'user': user,
                'logout_url': users.create_logout_url(self.request.uri),
                'userdetail': userdetail,
                'tweetdetail' : tweetdetail
                }
            template = JINJA_ENVIRONMENT.get_template('tweetpage.html')
            self.response.write(template.render(template_values))


    def post(self):
        action = self.request.get('button')
        user = users.get_current_user()

        if action == 'Enter':
            key = ndb.Key('UserDetail', user.user_id())
            userdetail = key.get()

            userNamesKey = ndb.Key('UserNameList', 'common')
            userNamesList = userNamesKey.get()

            userName = self.request.get('userName')
            userName = str(userName)

            tweetsKey = ndb.Key('TweetDetail', userName)
            tweets = tweetsKey.get()

            if tweets == None:
                userNamesList.userNames.append(userName)
                logging.info('%%%')
                logging.info(userNamesList.userNames)

                userdetail.userName = self.request.get('userName')
                userdetail.dateOfBirth = datetime.strptime(self.request.get('dateOfBirth'), '%Y-%m-%d')
                userdetail.shortProfile = self.request.get('shortProfile')
                if userdetail.shortProfile == None or userdetail.shortProfile == '' :
                    self.redirect('/')
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
            key = ndb.Key('TweetDetail', userdetail.userName)
            tweetdetail = key.get()

            tweetFetch = self.request.get('newTweet')

            if tweetFetch == None or tweetFetch == '':
                self.redirect('/')
                return

            tweetdetail.newTweets.append(tweetFetch)

            tweetdetail.put()

            self.redirect('/')

        elif action == 'Search':
            userNamesKey = ndb.Key('UserNameList', 'common')
            userNamesList = userNamesKey.get()

            searchOutput = self.request.get('output')

            for item in userNamesList.userNames:
                logging.info('$$' + item)
                if item == searchOutput:
                    logging.info('!!!')
                    matchedUserName = str(item)
                    url = '/?searchOutput=' + searchOutput
                    logging.info(item)
                    self.redirect(url)
                    return
            logging.info('No User Found')
            self.redirect('url')


app = webapp2.WSGIApplication([ ('/', MainPage), ('/edituserdetail', EditUserDetail),
('/displayuserdetail', DisplayUserDetail)], debug = True)
