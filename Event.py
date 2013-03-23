from datetime import datetime
from datetime import timedelta

import urllib
from AppUser import AppUser

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import mail

class Event(db.Model):
	"""Models an individual Event item, describing the entirety of the event."""
	creator 	= db.ReferenceProperty(AppUser, required=True)
	host		= db.StringProperty(indexed=False)
	name 		= db.StringProperty(indexed=False, required=True)
	location 	= db.StringProperty(indexed=False, required=True)
	description	= db.StringProperty(multiline=True)
	dateStart 	= db.DateTimeProperty(required=True)
	dateEnd 	= db.DateTimeProperty()
	lastUpdated = db.DateTimeProperty(auto_now=True)
	verified 	= db.BooleanProperty()
	attending	= db.IntegerProperty(indexed=False)

	def verify(self):
		if self.verified:
			return
		self.verified=True
		#push
  
	def getXMLFormat(self):
		return """<Event name='""" + self.name + """'>
		<location>""" + self.location + """</location>
		<start>""" + self.startTime.isoformat()[:16] + """</start>
		<end>""" + (self.dateEnd.isoformat()[:16] if dateEnd is not None else "") + """</end>
		<host>""" + self.host + """</host>
		<creator>""" + self.creator.id.nickname() + """</creator>
		<attending>""" + (str)(self.attending) + """</attending>
		<description>""" + self.description + """</description>
		<verified>""" + ("1" if self.verified else "0") + """</verified>
		<key>""" + self.key() + """</key>
		</Event>"""

	def getEventLink(self):
		return """/Event/"""+str(self.key()) #Update to actual page.