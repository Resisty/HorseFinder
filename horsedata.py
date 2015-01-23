#!/usr/bin/python
# =======================================
#
#  File Name : horsedata.py
#
#  Purpose :
#
#  Creation Date : 21-01-2015
#
#  Last Modified : Thu 22 Jan 2015 04:53:04 PM CST
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
        Database = db

def create_tables():
    db.connect()
    db.create_tables([Banned])
