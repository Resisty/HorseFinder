#!/usr/bin/python
# =======================================
#
#  File Name : horsedata.py
#
#  Purpose :
#
#  Creation Date : 21-01-2015
#
#  Last Modified : Fri 23 Jan 2015 11:24:59 AM CST
#
#  Created By : Brian Auron
#
# ========================================

from peewee import *

db = SqliteDatabase('horsedata.db')

class Banned(Model):
    flavor = CharField()
    trigger = CharField()
    tweettext = TextField()
    tweeter = TextField()
    status = TextField()
    datetime = DateTimeField()

    class Meta:
        database = db

def create_tables():
    db.connect()
    db.create_tables([Banned])
