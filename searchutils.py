def getAllMatchedTweets(keywordToMatch):
    userNames = ndb.key('UserNameList', 'common').get().userNames

    matchedTweets = []

    for userName in userNames:
        tweetDetails = ndb.key('TweetDetail', userName).get()
        matchedTweetsForUser = difflib.get_close_matches(keywordToMatch, tweetDetails.newTweet)
        matchedTweets.append(x in matchedTweetsForUser)

    return matchedTweets
