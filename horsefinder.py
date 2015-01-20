#!/usr/bin/python
# =======================================
#
#  File Name : twythontest.py
#
#  Purpose :
#
#  Creation Date : 15-01-2015
#
#  Last Modified : Tue 20 Jan 2015 01:54:33 PM CST
#
#  Created By : Brian Auron
#
# ========================================

import logging
import re
from annoying_stuff import words
from time import sleep
from twython import Twython, TwythonStreamer
from credentials import consumer, access
from threading import Thread

logging.basicConfig(filename='horsefinder.log',
                    format='%(asctime)s %(message)s',
                    level=logging.DEBUG)
banned_regex = re.compile('|'.join(words))

def has_banned_word(text):
    found = banned_regex.search(text)
    if found:
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
        if 'text' in data and not has_banned_word(data['text']):
            try:
                logging.info('HorseTweeter trying to retweet found horse id: {0}'.format(data['id']))
                getTwitter().retweet(data['id'])
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

        try:
            if 'text' in realTweet and not has_banned_word(realTweet['text']):
                getTwitter().retweet(id = status)
        except:
            logging.error('Could not retweet from DM: {0}'.format(e))

    def on_error(self, status_code, data):
        logging.error('MessageStreamer twitter error code: {0}'.format(status_code))

streamer = MessageStreamer(consumer['key'],
                         consumer['secret'],
                         access['key'],
                         access['secret'])
streamthread = Thread(target = streamer.user)
streamthread.daemon = True
streamthread.start()

horses = HorseTweeter(consumer['key'],
                     consumer['secret'],
                     access['key'],
                     access['secret'])
horses.statuses.filter(track='horse')
horsethread = Thread(target = horses.statuses.filter, args = ('horse',))
horsethread.daemon = True
horsethread.start()
