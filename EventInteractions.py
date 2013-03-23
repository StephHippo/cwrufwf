import webapp2
import os
import urllib
from google.appengine.ext.webapp import template

from datetime import datetime
from datetime import date
from datetime import time

from AppUser import AppUser
from Event import Event

from google.appengine.ext import db
from google.appengine.api import users


class Verify(webapp2.RequestHandler):
	def post(self):
		key =getInt("key", self)
		event = db.get(key)
		event.verify()
		# push update
		self.redirect('/?' + urllib.urlencode({'message':'Event Verified!'}))

class Report(webapp2.RequestHandler):
	def post(self):
		key =getInt("key", self)
		event = db.get(key)
		# get user
		# get user comment on report
		# check with admins/verified
		# tenative reject count +1
		# if reject>3, kill Event, neg appuser ?
		# TODO Needs a special form.

class Attend(webapp2.RequestHandler):
	def post(self):
		key =getInt("key", self)
		event = db.get(key)
		event.attending = event.attending+1
		event.put
		self.redirect('/?' + urllib.urlencode({'message':'''Attendance noted!'''}))

class View(webapp2.RequestHandler):
	def get(self):
		key =getInt("key", self)
		event = db.get(key)
		# banner, full info


def getDate(key, page):
#Expects data in MM/DD/YYYY format.
	n=getString(key, page).split("/")
	return date(year=(int)(n[2]), month=(int)(n[0]), day = (int)(n[1]))

def getDateTime(key, date, page):
#Expects format of time to be "HH:MM" in 24 hour time.
	n=getString(key,page).split(":")
	t=time(hour=(int)(n[0]), minute=(int)(n[1]))
	return datetime.combine(date,t)

def getInt(key, page):
	return (int)(getString(key, page))

def getString(key, page):
	return page.request.get(key)