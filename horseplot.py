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

def x_label_datetime3(rows):
    maxdate = max([i.datetime for i in rows])
    mindate = min([i.datetime for i in rows])
    halfway = (maxdate - mindate) / 2 + mindate
    return [mindate, halfway, maxdate]


def pygal_dateyify(select):
    flavor = select.get().flavor
    try:
        assert all([i.flavor == flavor for i in select])
    except Exception:
        logging.error('Different flavors returned in query. Unable to plot.')

    data = []
    ordered_by_date = select.order_by(Banned.datetime)
    value = 1
    linkfmt = 'https://twitter.com/{0}/status/{1}'
    for i in ordered_by_date:
        node = {'value': (i.datetime, value),
                'label': i.tweettext,
                'xlink': linkfmt.format(i.tweeter, i.status)}
        data.append(node)
        value += 1
    return data


def main():
    data_by_flavor = pull_data()
    datey = pygal.DateY(x_label_rotation=20,
                        title = 'Piecewise Trends of Filtered Tweets Over Time',
                        x_title = 'Datetime',
                        include_x_axis = True)
    datey.x_labels = x_label_datetime3([i for j in data_by_flavor.values() for i in j])
    for flavor, flavor_data in data_by_flavor.iteritems():
        pygal_data = pygal_dateyify(flavor_data)
        datey.add(flavor, pygal_data)

    with open('horseplot.svg', 'w') as f:
        f.write(datey.render())
    print "Wrote out data"

if __name__ == '__main__':
    main()
