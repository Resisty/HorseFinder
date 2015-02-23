#!/usr/bin/python
# =======================================
#
#  File Name : horsedata.py
#
#  Purpose :
#
#  Creation Date : 21-01-2015
#
#  Last Modified : Sun 22 Feb 2015 07:32:15 PM CST
#
#  Created By : Brian Auron
#
# ========================================

from peewee import *

bannedDB = SqliteDatabase('banned.db')
retweetDB = SqliteDatabase('retweet.db')

class Retweets(Model):
    tweettext = TextField()
    tweeter = TextField()
    status = TextField()
    datetime = DateTimeField()

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
