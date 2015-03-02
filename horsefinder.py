#!/usr/bin/python
# =======================================
#
#  File Name : twythontest.py
#
#  Purpose :
#
#  Creation Date : 15-01-2015
#
#  Last Modified : Sun 01 Mar 2015 11:55:24 PM CST
#
#  Created By : Brian Auron
#
# ========================================

import logging
import re
import json
import sys
import signal
import traceback
from datetime import datetime, timedelta
from horsedata import Banned, Retweets, bannedDB, retweetDB
from banned import annoying, hateful, dirty
from time import sleep
from twython import Twython, TwythonStreamer
from credentials import consumer, access
from threading import Thread
from difflib import SequenceMatcher

logging.basicConfig(filename='horsefinder.log',
                    format='[%(asctime)s] [%(levelname)s] %(message)s',
                    level=logging.INFO)
annoying_re = re.compile('|'.join(annoying), re.IGNORECASE)
hateful_re = re.compile('|'.join(hateful), re.IGNORECASE)
dirty_re = re.compile('|'.join(dirty), re.IGNORECASE)

def has_banned_word(tweet):
    searchtweet = json.dumps(tweet).encode('utf-8')
    text = tweet['text'].encode('utf-8')
    status = tweet['id']
    user = tweet['user']['screen_name'].encode('utf-8')
    now = datetime.now().strftime("%F %T")
    annoying_tweet = annoying_re.search(searchtweet)
    hateful_tweet = hateful_re.search(searchtweet)
    dirty_tweet = dirty_re.search(searchtweet)

    annoying_text = annoying_re.search(text)
    hateful_text = hateful_re.search(text)
    dirty_text = dirty_re.search(text)

    try:
        bannedDB.connect()
        if annoying_tweet:
            Banned.insert(flavor='annoying',
                          trigger=annoying_tweet.group(),
                          tweettext=text,
                          tweeter=user,
                          status=status,
                          datetime=now).execute()
        if hateful_tweet:
            Banned.insert(flavor='hateful',
                          trigger=hateful_tweet.group(),
                          tweettext=text,
                          tweeter=user,
                          status=status,
                          datetime=now).execute()
        if dirty_tweet:
            Banned.insert(flavor='dirty',
                          trigger=dirty_tweet.group(),
                          tweettext=text,
                          tweeter=user,
                          status=status,
                          datetime=now).execute()

        if annoying_text:
            Banned.insert(flavor='annoying',
                          trigger=annoying_text.group(),
                          tweettext=text,
                          tweeter=user,
                          status=status,
                          datetime=now).execute()
        if hateful_text:
            Banned.insert(flavor='hateful',
                          trigger=hateful_text.group(),
                          tweettext=text,
                          tweeter=user,
                          status=status,
                          datetime=now).execute()
        if dirty_text:
            Banned.insert(flavor='dirty',
                          trigger=dirty_text.group(),
                          tweettext=text,
                          tweeter=user,
                          status=status,
                          datetime=now).execute()
        bannedDB.close()
    except Exception as e:
        logging.info('Could not use db: {0}'.format(e))

    if any([annoying_text, hateful_text, dirty_text, annoying_tweet, hateful_tweet, dirty_tweet]):
        return True
    return False

def partial_ratio(text1, text2):
    # From: https://github.com/seatgeek/fuzzywuzzy/blob/master/fuzzywuzzy/fuzz.py
    """"Return the ratio of the most similar substring
    as a number between 0 and 100."""

    if text1 is None:
        raise TypeError("text1 is None")
    if text2 is None:
        raise TypeError("text2 is None")
    if len(text1) == 0 or len(text2) == 0:
        return 0

    if len(text1) <= len(text2):
        shorter = text1
        longer = text2
    else:
        shorter = text2
        longer = text1

    m = SequenceMatcher(None, shorter, longer)
    blocks = m.get_matching_blocks()

    # each block represents a sequence of matching characters in a string
    # of the form (idx_1, idx_2, len)
    # the best partial match will block align with at least one of those blocks
    #   e.g. shorter = "abcd", longer = XXXbcdeEEE
    #   block = (1,3,3)
    #   best score === ratio("abcd", "Xbcd")
    scores = []
    for block in blocks:
        long_start = block[1] - block[0] if (block[1] - block[0]) > 0 else 0
        long_end = long_start + len(shorter)
        long_substr = longer[long_start:long_end]

        m2 = SequenceMatcher(None, shorter, long_substr)
        r = m2.ratio()
        if r > .995:
            return 100
        else:
            scores.append(r)

    return int(100 * max(scores))

def is_retweet(tweet):
    text = tweet['text'].encode('utf-8')
    status = tweet['id']
    user = tweet['user']['screen_name'].encode('utf-8')
    now = datetime.now().strftime("%F %T")
    try:
        media = tweet['extended_entities']['media'][0]['expanded_url']
    except:
        media = ''
    retweetDB.connect()
    select = Retweets.select()
    matches = []
    for i in select:
        match = partial_ratio(text, i.tweettext)
        if match >= 81:
            matches.append(i.tweettext)
        if media != '' and media == i.media:
            matches.append(i.media)
    retweetDB.close()
    return matches

def store_retweet(tweet):
    text = tweet['text'].encode('utf-8')
    try:
        media = tweet['extended_entities']['media'][0]['expanded_url']
    except:
        media = ''
    status = tweet['id']
    user = tweet['user']['screen_name'].encode('utf-8')
    now = datetime.now().strftime("%F %T")
    retweetDB.connect()
    Retweets.insert(tweettext = text,
                    tweeter = user,
                    status = status,
                    media = media,
                    datetime = now).execute()
    retweetDB.close()


def getTwitter():
    twitter = Twython(consumer['key'],
                      consumer['secret'],
                      access['key'],
                      access['secret'])
    return twitter

class HorseTweeter(TwythonStreamer):
    def __init__(self, *args):
        self.lastTweetTime = datetime.now() - timedelta(0,600,0)
        super(HorseTweeter, self,).__init__(*args)

    def on_success(self, data):
        delta = datetime.now() - self.lastTweetTime
        if delta.seconds < 600:
            return

        if 'text' in data:
            print '"{0}"'.format(data['text'].encode('utf-8'))
            text = data['text'].encode('utf-8')
            if has_banned_word(data):
                logging.info('HorseTweeter found a bad word in some text: "{0}"'.format(text))
                return

            rts = is_retweet(data)
            if rts:
                logging.info('HorseTweeter found a duplicate of an earlier retweet: {0} :: {1}'.format(text, rts))
                return

            retweeted = True
            try:
                logging.info('HorseTweeter trying to retweet found horse id: {0}'.format(data['id']))
                getTwitter().retweet(id = data['id'])
            except Exception as e:
                logging.error('HorseTweeter could not retweet found horse, error: {0}'.format(e))
                retweeted = False

            try:
                store_retweet(data)
            except Exception as e:
                logging.error('Could not store retweet in db: {0}'.format(e))

            if retweeted:
                self.lastTweetTime = datetime.now()

    def on_error(self, status_code, data):
        logging.error('HorseTweeter twitter error code: {0}'.format(status_code))

class MessageStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'direct_message' not in data:
            return

        try:
            status = data['direct_message']['entities']['urls'][0]['expanded_url']
            status = status.split('/')[-1]
        except Exception as e:
            logging.error('MessageStreamer could not get status from DM: {0}'.format(e))
            return
        logging.info('MessageStreamer found a direct message')

        try:
            realTweet = getTwitter().show_status(id = status)
        except Exception as e:
            logging.error('MessageStreamer could not get real tweet: {0}'.format(e))
            return
        logging.info('MessageStreamer found a real tweet: {0}'.format(realTweet))

        if 'text' in realTweet:
            print realTweet['text']
            text = realTweet['text'].encode('utf-8')
            if has_banned_word(realTweet):
                logging.info('MessageStreamer found a bad word in some text: "{0}"'.format(text))
                return
            logging.info('MessageStreamer trying to retweet status: {0}'.format(status))

            rts = is_retweet(realTweet)
            if rts:
                logging.info('HorseTweeter found a duplicate of an earlier retweet: {0} :: {1}'.format(text, rts))
                return

            try:
                getTwitter().retweet(id = status)
            except Exception as e:
                logging.error('MessageStreamer could not retweet from DM: {0}'.format(e))
            try:
                store_retweet(realTweet)
            except Exception as e:
                logging.error('Could not store retweet in db: {0}'.format(e))


    def on_error(self, status_code, data):
        logging.error('MessageStreamer twitter error code: {0}'.format(status_code))

def main():
    streamer = MessageStreamer(consumer['key'],
                               consumer['secret'],
                               access['key'],
                               access['secret'],)
    streamthread = Thread(target = streamer.user)
    streamthread.daemon = True
    streamthread.start()

    horses = HorseTweeter(consumer['key'],
                          consumer['secret'],
                          access['key'],
                          access['secret'])
    while True:
        try:
            horses.statuses.filter(track='horse,horsefacts')
        except Exception as e:
            print traceback.format_exc()
            logging.error('HorseTweeter failed: {0}'.format(e))
            continue

if __name__ == '__main__':
    main()
