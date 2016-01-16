# import the twitter library
from twitter import *

# standard library
import html


# these tokens are necessary for user authentication
# (created within the twitter developer API pages)
# https://dev.twitter.com/rest/public
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def post_tweet(status_text, nick):
    new_status = '<{}>: {}'.format(nick, status_text)

    # create twitter API object
    auth = OAuth(access_key, access_secret, consumer_key, consumer_secret)
    twitter = Twitter(auth=auth)

    # post a new status
    twitter.statuses.update(status=new_status)
    print('updated status: {}'.format(new_status))


def get_latest_tweet():
    # create twitter API object
    auth = OAuth(access_key, access_secret, consumer_key, consumer_secret)
    twitter = Twitter(auth=auth)

    # request latest tweet
    tweet_info = html.unescape(twitter.statuses.home_timeline(count=1))
    status = tweet_info[0]
    return '({}) @{}: "{}"'.format(status['created_at'][:-11],
                                   status['user']['screen_name'],
                                   html.unescape(status['text'])
                                   )
