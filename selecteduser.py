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

        key = ndb.Key('UserDetail', user.user_id())
        userdetail = key.get()

        tweetKey = ndb.Key('TweetDetail', userdetail.userName)
        tweetdetailCurrentUser = tweetKey.get()

        searchedUserName = self.request.get('user')

        if searchedUserName == None or searchedUserName == '':
                self.redirect('/')
                return

        if searchedUserName in tweetdetailCurrentUser.followingUser:
            followed = True
        else:
            followed = False

        tweetKey = ndb.Key('TweetDetail', searchedUserName)
        tweetdetail = tweetKey.get()

        template_values = {
            'tweetdetail': tweetdetail,
            "searchedUserName": searchedUserName,
            'followed':followed,
            'CurrentUser' : userdetail.userName,
            'list': tweetdetailCurrentUser.followingUser

        }
        template = JINJA_ENVIRONMENT.get_template('selecteduser.html')
        self.response.write(template.render(template_values))

    def post(self):
        user = users.get_current_user()

        key = ndb.Key('UserDetail', user.user_id())
        userdetail = key.get()

        tweetKey = ndb.Key('TweetDetail', userdetail.userName)
        tweetdetailCurrentUser = tweetKey.get()


        action = self.request.get('button')

        if action == 'Follow':
            searchedUserName = self.request.get('user')

            if searchedUserName == None or searchedUserName == '':
                self.redirect('/')
                return

            tweetKey = ndb.Key('TweetDetail', searchedUserName)
            tweetdetail = tweetKey.get()

            followed = True

            # for Follwing users
            followingUserName = str(searchedUserName)
            tweetdetailCurrentUser.followingUser.append(followingUserName)
            tweetdetailCurrentUser.put()

            # For Followers
            if followed == True:
                followingUserName = str(searchedUserName)
                tweetdetail.followers.append(followingUserName)
                tweetdetail.put()

            template_values = {
                'tweetdetail': tweetdetail,
                "searchedUserName": searchedUserName,
                "followed": followed,
                'CurrentUser' : userdetail.userName,
                'list': tweetdetailCurrentUser.followingUser
            }
            template = JINJA_ENVIRONMENT.get_template('selecteduser.html')
            self.response.write(template.render(template_values))

        elif action == 'Following':
            searchedUserName = self.request.get('user')

            if searchedUserName == None or searchedUserName == '':
                self.redirect('/')
                return

            tweetKey = ndb.Key('TweetDetail', searchedUserName)
            tweetdetail = tweetKey.get()

            followed = False
            followingUserName = str(searchedUserName)

            # For following User
            if followed == False:
                if followingUserName in tweetdetailCurrentUser.followingUser:
                    tweetdetailCurrentUser.followingUser.remove(followingUserName)
                    tweetdetailCurrentUser.put()

            # For Followers
            if followed == False:
                followingUserName = str(searchedUserName)
                tweetdetail.followers.remove(followingUserName)
                tweetdetail.put()

            template_values = {
                'tweetdetail': tweetdetail,
                "searchedUserName": searchedUserName,
                "followed": followed,
                'CurrentUser' : userdetail.userName,
                'list': tweetdetailCurrentUser.followingUser
            }
            template = JINJA_ENVIRONMENT.get_template('selecteduser.html')
            self.response.write(template.render(template_values))
