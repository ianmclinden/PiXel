import twitter
import json
from conf import *


def buildSearchTerm():
    """Returns a twitter-friendly query, from the QUERY config params"""
    return "%20OR%20".join(["from%3A"+user for user in QUERY_FROM_USERS] + QUERY_SPECIALS + QUERY_KEYWORDS)


def hasUserMatch(uList, tweetJSON):
    """Returns true if a tweet from any user in QUERY_FROM_USERS is found"""
    return any(keyword in tweetJSON['user']['screen_name'] for keyword in uList)


def hasQueryMatch(qList, tweetJSON):
    """Returns true if a tweet containing any keyword in QUERY_KEYWORDS is found"""
    return any(keyword in tweetJSON['text'] for keyword in qList)


def hasHashtagMatch(hList, tweetJSON):
    """Returns true if a tweet containing any hashtag in QUERY_HASHTAGS is found"""
    return any(keyword in str(tweetJSON['hashtags']) for keyword in hList)


class TwitterEngine:
    """Polls Twitter for QUERY config parameters"""

    def __init__(self):
        print("[!] Starting Twitter Engine ...")
        print("[!] Query: (%s)\n" % " OR ".join(["from:"+user for user in QUERY_FROM_USERS] + QUERY_SPECIALS + QUERY_KEYWORDS))
        self.maxId = 0
        self.api = twitter.Api(consumer_key=CONSUMER_KEY,
                               consumer_secret=CONSUMER_SECRET,
                               access_token_key=ACCESS_TOKEN_KEY,
                               access_token_secret=ACCESS_TOKEN_SECRET)

    def getNewMatches(self):
        """Returns the number of keywords, specials that matched"""
        tweetList = self.api.GetSearch(term=buildSearchTerm(),
                                       since_id=self.maxId,
                                       lang="en",
                                       result_type="recent",
                                       include_entities=False,
                                       count=LED_COUNT)

        jsonTweetList = [json.loads(str(tweet)) for tweet in tweetList]

        # maxId is used next poll to limit the oldest post to return
        ids = [jTweet['id'] for jTweet in jsonTweetList]
        if len(ids) > 0:
            self.maxId = max(ids)

        # Check for Keywords
        kList = [jTweet for jTweet in jsonTweetList if (
            hasQueryMatch(QUERY_KEYWORDS, jTweet) or hasHashtagMatch(QUERY_KEYWORDS, jTweet))]

        # Check for Specials
        sList = [jTweet for jTweet in jsonTweetList if (
            hasQueryMatch(QUERY_SPECIALS, jTweet) or
            hasHashtagMatch(QUERY_SPECIALS, jTweet)) or
            hasUserMatch(QUERY_FROM_USERS, jTweet)]

        return len(kList), len(sList)
