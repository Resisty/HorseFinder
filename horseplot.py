#!/usr/bin/python
# =======================================
#
#  File Name : horseplot.py
#
#  Purpose : Plot data from horsedata.db
#            use DateY plot from pygal
#            reference: http://pygal.org/chart_types/#iddatey
#
#  Creation Date : 27-01-2015
#
#  Last Modified :
#
#  Created By : Brian Auron
#
# ========================================

#TODO: Set y-axis coordinate as cumulative number of tweets for category
# Make xlinks point to actual tweets
# Data collector/collator function for putting into DateY graph

import pygal
from horsedata import Banned, db
from datetime import datetime, timedelta
import logging
from random import randint

logging.basicConfig(filename='horseplot.log',
                    format='[%(asctime)s] [%(levelname)s] %(message)s',
                    level=logging.DEBUG)

def pull_data():
    db.connect()
    select = Banned.select()
    flavor_select = Banned.select(Banned.flavor).distinct()
    data_by_flavor = {}
    for i in flavor_select:
        data_by_flavor[i.flavor] = select.where(Banned.flavor == i.flavor)

    return data_by_flavor

def pygalify_flavor_data(flavor_data):
    flavor = flavor_data.get().flavor
    try:
        assert all([i.flavor == flavor for i in flavor_data])
    except Exception:
        logging.error('Different flavors returned in query. Unable to plot.')

    data = []
    linkfmt = 'https://twitter.com/{0}/status/{1}'
    for i in flavor_data:
        node = {'value': (i.datetime, randint(1,21)),
                'label': i.tweettext,
                'xlink': linkfmt.format(i.tweeter, i.status)}
        data.append(node)
    return data


def main():
    datey = pygal.DateY(x_label_rotation=20)
    data_by_flavor = pull_data()
    for flavor, flavor_data in data_by_flavor.iteritems():
        pygal_data = pygalify_flavor_data(flavor_data)
        datey.add(flavor, pygal_data)

    with open('horseplot.svg', 'w') as f:
        f.write(datey.render())
    print "Wrote out data"

if __name__ == '__main__':
    main()
#data = [{'value': (datetime(2015, 1, 27, 8, 39, 6), 1),
#         'label': 'annoying',
#         'xlink': 'http://buttgenerator.com'},
#        {'value': (datetime(2015, 1, 26, 13, 42, 42), 1),
#         'label': 'annoying',
#         'xlink': 'http://buttgenerator.com'}]
#datey.add('annoying', data)
#
#data = [{'value': (datetime(2015, 1, 26, 23, 13, 0), 2),
#         'label': 'hateful',
#         'xlink':
#         'http://art.penny-arcade.com/photos/215499488_8pSZr/0/1050x10000/215499488_8pSZr-1050x10000.jpg'},
#        {'value': (datetime(2015, 1, 25, 10, 35, 35), 2),
#         'label': 'hateful',
#         'xlink': 'http://art.penny-arcade.com/photos/215499488_8pSZr/0/1050x10000/215499488_8pSZr-1050x10000.jpg'}]
#datey.add('hateful', data)
#
#data = [{'value': (datetime(2015, 1, 25, 12, 0, 0), 3),
#         'label': 'dirty',
#         'xlink': 'http://jamesgunn.com/pg-porn'},
#        {'value': (datetime(2015, 1, 27, 17, 12, 12), 3),
#         'label': 'dirty',
#         'xlink': 'http://jamesgunn.com/pg-porn'}]
#datey.add('dirty', data)
#
#with open('butts','w') as f:
#    f.write(datey.render())
