#!/usr/bin/python
# =======================================
#
#  File Name : twythontest.py
#
#  Purpose :
#
#  Creation Date : 15-01-2015
#
#  Last Modified : Wed 04 Feb 2015 01:21:07 PM CST
#
#  Created By : Brian Auron
#
# ========================================

import logging
import re
import json
import sys
import signal
from datetime import datetime
from horsedata import Banned, db
from banned import annoying, hateful, dirty
from time import sleep
from twython import Twython, TwythonStreamer
from credentials import consumer, access
from threading import Thread

logging.basicConfig(filename='horsefinder.log',
                    format='[%(asctime)s] [%(levelname)s] %(message)s',
                    level=logging.DEBUG)
annoying_re = re.compile('|'.join(annoying), re.IGNORECASE)
hateful_re = re.compile('|'.join(hateful), re.IGNORECASE)
dirty_re = re.compile('|'.join(dirty), re.IGNORECASE)

def has_banned_word(tweet):
    text = tweet['text'].encode('utf-8')
    status = tweet['id']
    user = tweet['user']['screen_name'].encode('utf-8')
    now = datetime.now().strftime("%F %T")
    annoying_text = annoying_re.search(text)
    hateful_text = hateful_re.search(text)
    dirty_text = dirty_re.search(text)
    try:
        db.connect()
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
        db.close()
    except Exception as e:
        logging.info('Could not use db: {0}'.format(e))

    if any([annoying_text, hateful_text, dirty_text]):
        return True
    return False

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
            else:
                try:
                    logging.info('HorseTweeter trying to retweet found horse id: {0}'.format(data['id']))
                    getTwitter().retweet(id = data['id'])
                    sleep(1800)
                except Exception as e:
                    logging.error('HorseTweeter could not retweet found horse, error: {0}'.format(e))

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
            try:
                getTwitter().retweet(id = status)
            except Exception as e:
                logging.error('MessageStreamer could not retweet from DM: {0}'.format(e))


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
            logging.error('HorseTweeter failed: {0}'.format(e))
            continue

if __name__ == '__main__':
    main()
