#!/usr/bin/env python
import requests, os, xively, datetime
from pyquery import PyQuery


FEED_ID = os.environ["FEED_ID"]
API_KEY = os.environ["API_KEY"]

KNESSET_URL = 'http://www.knesset.gov.il/presence/heb/PresentList.aspx'

# initialize api client
api = xively.XivelyAPIClient(API_KEY)

def get_attendees():
    try:
        pq = PyQuery(url=KNESSET_URL)
    except requests.HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)
        return 0

    return pq('[color="#C47400"]').eq(0).text()

def run():
    print "Starting Knesset Members Attendance Meter"

    feed = api.feeds.get(FEED_ID)

    try:
        datastream = feed.datastreams.get("attendees")
    except:
        datastream = feed.datastreams.create("attendees")

    datastream.max_value = 120
    datastream.min_value = 0

    datastream.current_value = get_attendees()
    datastream.at = datetime.datetime.utcnow()
    try:
        datastream.update()
    except requests.HTTPError as e:
        print "HTTPError({0}): {1}".format(e.errno, e.strerror)

run()
