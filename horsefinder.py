#!/usr/bin/python
# =======================================
#
#  File Name : horsefinder.py
#
#  Purpose :
#
#  Creation Date : 14-01-2015
#
#  Last Modified : Wed 14 Jan 2015 03:40:36 PM CST
#
#  Created By : Brian Auron
#
# ========================================

import twitter
import requests
import threading
from random import choice
from annoying_stuff import words
from time import sleep
from getpass import getpass
from pprint import pprint

def get_authed():
    consumer_key = getpass('Consumer key: ')
    consumer_secret = getpass('Consumer secret: ')
    access_token_key = getpass('Access token key: ')
    access_token_secret = getpass('Access token secret: ')
    api = twitter.Api(consumer_key,
                      consumer_secret,
                      access_token_key,
                      access_token_secret)
    if not api.VerifyCredentials():
        return False
    else:
        return api

def rt_direct_messages():
    while True:
        api = get_authed()
        dms = api.GetDirectMessages()
        statuses = set()
        for i in dms:
            try:
                link = requests.get(i.text)
                status_id = link.url.split('/')[-1]
                statuses.add(status_id)
            except:
                print "Bad or nonexistent link in DM. Discarding."
            api.DestroyDirectMessage(i.id)
        for s in statuses:
            api.PostRetweet(s)
        sleep(600)

def remove_annoyances(statuses):
    good_statuses = statuses
    for s in statuses:
        if not s.urls:
            good_statuses.remove(s)
        else:
            for word in words:
                if word in s:
                    good_statuses.remove(s)
    return remove_annoyances

def find_horses():
    while True:
        api = get_authed()
        horses = api.GetSearch('horse',include_entities=True)
        good_horses = remove_annoyances(horses)
        sid = choice(good_horses).id
        api.PostRetweet(sid)
        sleep(1800)

def main():
    dm_thread = threading.Thread(target=rt_direct_messages)
    dm_thread.daemon = True
    dm_thread.start()

    horses_thread = threading.Thread(target=find_horses)
    horses_thread.daemon = True
    horses_thread.start()

main()
