#!/usr/bin/python
# =======================================
#
#  File Name : twythontest.py
#
#  Purpose :
#
#  Creation Date : 15-01-2015
#
#  Last Modified : Fri 16 Jan 2015 04:23:35 PM CST
#
#  Created By : Brian Auron
#
# ========================================

import logging
from time import sleep
from twython import Twython, TwythonStreamer
from credentials import consumer, access
from threading import Thread

logging.basicConfig(format='%(asctime)s %(message)s')

class HorseTweeter(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            try:
                retwython = Twython(consumer['key'],
                                    consumer['secret'],
                                    access['key'],
                                    access['secret'])
                retwython.retweet(id = data['id'])
            except Exception as e:
                logging.error('Could not retweet: {0}'.format(e))
            sleep(1800)

    def on_error(self, status_code, data):
        print status_code

class MessageStreamer(TwythonStreamer):
    def on_success(self, data):
        try:
            status = data['direct_message']['entities']['urls'][0]['expanded_url']
            status = status.split('/')[-1]
            try:
                retwython = Twython(consumer['key'],
                                    consumer['secret'],
                                    access['key'],
                                    access['secret'])
                retwython.retweet(id = status)
            except Exception as e:
                logging.error('Could not retweet: {0}'.format(e))
        except:
            try:
                logging.info('Stream entry that wasn\'t a DM of a shared tweet: {1}'.format(data.text))
            except:
                logging.info('Stream entry with no text attribute.  ???')

    def on_error(self, status_code, data):
        print status_code
        self.disconnect()

streamer = MessageStreamer(consumer['key'],
                         consumer['secret'],
                         access['key'],
                         access['secret'])
streamthread = Thread(target = streamer.user)
streamthread.start()

horses = HorseTweeter(consumer['key'],
                     consumer['secret'],
                     access['key'],
                     access['secret'])
horses.statuses.filter(track='horse')
horsethread = Thread(target = horses.statuses.filter, args = ('horse',))
horsethread.start()
