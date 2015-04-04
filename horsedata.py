#!/usr/bin/python
# =======================================
#
#  File Name : horsedata.py
#
#  Purpose :
#
#  Creation Date : 21-01-2015
#
#  Last Modified : Fri 03 Apr 2015 10:09:54 PM CDT
#
#  Created By : Brian Auron
#
# ========================================

from peewee import *
import os
dbdir = os.path.dirname(os.path.realpath(__file__))

bannedDB = SqliteDatabase(os.path.join(dbdir, 'banned.db'))
retweetDB = SqliteDatabase(os.path.join(dbdir, 'retweet.db'))

class Retweets(Model):
    tweettext = TextField()
    tweeter = TextField()
    status = TextField()
    datetime = DateTimeField()
    media = TextField()

    class Meta:
        database = retweetDB

class Banned(Model):
    flavor = CharField()
    trigger = CharField()
    tweettext = TextField()
    tweeter = TextField()
    status = TextField()
    datetime = DateTimeField()

    class Meta:
        database = bannedDB

def create_banned():
    bannedDB.connect()
    bannedDB.create_tables([Banned])

def create_retweet():
    retweetDB.connect()
    retweetDB.create_tables([Retweets])
