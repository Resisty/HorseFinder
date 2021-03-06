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
import codecs
from pygal.style import Style
from horsedata import Banned, bannedDB as db
from datetime import datetime, timedelta
import logging
from random import randint
import traceback

logging.basicConfig(filename='horseplot.log',
                    format='[%(asctime)s] [%(levelname)s] %(message)s',
                    level=logging.DEBUG)

def pull_data(since = None, until = None):
    if not since:
        since = datetime.today() - timedelta(3)
    if not until:
        until = datetime.now()
    if since > until:
        tmp = since
        since = until
        until = since
    db.connect()
    select = Banned.select()
    flavor_select = Banned.select(Banned.flavor).distinct()
    data_by_flavor = {}
    for i in flavor_select:
        data_by_flavor[i.flavor] = select.where(
            (Banned.flavor == i.flavor) &
            (Banned.datetime > since) &
            (Banned.datetime < until))

    return data_by_flavor

def x_label_datetime3(rows):
    try:
        maxdate = max([i.datetime for i in rows])
        mindate = min([i.datetime for i in rows])
        halfway = (maxdate - mindate) / 2 + mindate
    except ValueError:
        maxdate, mindate, halfway = ('Error: Bad date range' for i in range(3))
    return [mindate, halfway, maxdate]


def pygal_dateyify(select):
    try:
        flavor = select.get().flavor
    except:
        print 'Empty select!'
        return []
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


def make_datey(since = None, until = None):
    try:
        data_by_flavor = pull_data(since, until)
        custom_style = Style(
            background='transparent',
            plot_background='transparent',
            foreground='#000000',
            foreground_light='#585858',
            foreground_dark='#383838',
            opacity='.6',
            opacity_hover='.9',
            transition='400ms ease-in',
            colors=('#FF6600', '#9900CC', '#FF66FF'))

        datey = pygal.DateY(x_label_rotation=20,
                            title = 'Piecewise Trends of Filtered Tweets Over Time',
                            x_title = 'Datetime',
                            include_x_axis = True,
                            print_values = False,
                            disable_xml_declaration = True,
                            style = custom_style)
        datey.x_labels = x_label_datetime3([i for j in data_by_flavor.values() for i in j])
        for flavor, flavor_data in data_by_flavor.iteritems():
            pygal_data = pygal_dateyify(flavor_data)
            datey.add(flavor, pygal_data)
    except:
        print traceback.format_exc()
        return ''

    return datey

def pull_stats(since = None, until = None):
    if not since:
        since = datetime.today() - timedelta(3)
    if not until:
        until = datetime.now()
    if since > until:
        tmp = since
        since = until
        until = since
    data_by_flavor = pull_data(since, until)
    def colors():
        for i in ('#FF9933', '#9933FF', '#FFCCFF'):
            yield i
    color = colors()
    data = {}
    try:
        for flavor, select in data_by_flavor.iteritems():
            data[flavor] = {}
            data[flavor]['count'] = select.count()
            data[flavor]['color'] = color.next()
            diff = until - since
            hours = diff.days * 24 + diff.seconds / 3600.0
            try:
                hourly = data[flavor]['count'] / hours
                data[flavor]['hourly'] = '{0:.3}'.format(hourly)
            except ZeroDivisionError:
                data[flavor]['hourly'] = 0.0
        return data
    except:
        print traceback.format_exc()

def main():
    datey = make_datey()
    with codecs.open('horseplot.svg', 'w') as f:
        f.write(datey.render())
    print "Wrote out data"

if __name__ == '__main__':
    main()
