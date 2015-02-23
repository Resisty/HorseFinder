#!/usr/bin/python
# =======================================
#
#  File Name : twythontest.py
#
#  Purpose :
#
#  Creation Date : 15-01-2015
#
#  Last Modified : Sun 22 Feb 2015 09:00:21 PM CST
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
from datetime import datetime
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
    searchtext = json.dumps(tweet).encode('utf-8')
    text = tweet['text'].encode('utf-8')
    status = tweet['id']
    user = tweet['user']['screen_name'].encode('utf-8')
    now = datetime.now().strftime("%F %T")
    annoying_text = annoying_re.search(searchtext)
    hateful_text = hateful_re.search(searchtext)
    dirty_text = dirty_re.search(searchtext)
    try:
        bannedDB.connect()
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

    if any([annoying_text, hateful_text, dirty_text]):
        return True
    return False

def is_retweet(tweet):
    text = tweet['text'].encode('utf-8')
    status = tweet['id']
    user = tweet['user']['screen_name'].encode('utf-8')
    now = datetime.now().strftime("%F %T")
    retweetDB.connect()
    select = Retweets.select()
    matches = []
    for i in select:
        match = SequenceMatcher(None, text, i.tweettext)
        if match.ratio() > .9:
            matches.append(i.tweettext)
    retweetDB.close()
    return matches

def store_retweet(tweet):
    text = tweet['text'].encode('utf-8')
    status = tweet['id']
    user = tweet['user']['screen_name'].encode('utf-8')
    now = datetime.now().strftime("%F %T")
    retweetDB.connect()
    Retweets.insert(tweettext = text,
                    tweeter = user,
                    status = status,
                    datetime = now).execute()
    retweetDB.close()


def getTwitter():
    twitter = Twython(consumer['key'],
                      consumer['secret'],
                      access['key'],
                      access['secret'])
    return twitter

class HorseTweeter(TwythonStreamer):
    def on_success(self, data):
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
                logging.info('About to sleep for 10 minutes')
                sleep(600)

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

            rts = is_retweet(data)
            if rt:
                logging.info('HorseTweeter found a duplicate of an earlier retweet: {0} :: {1}'.format(text, rts))
                return

            try:
                getTwitter().retweet(id = status)
            except Exception as e:
                logging.error('MessageStreamer could not retweet from DM: {0}'.format(e))
            try:
                store_retweet(data)
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
