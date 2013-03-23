import webapp2
import os
import urllib

from google.appengine.ext.webapp import template

from Event import Event
from AppUser import AppUser
from EventInteractions import getString
from EventInteractions import getDate
from EventInteractions import getDateTime
from EventInteractions import getInt


from google.appengine.ext import db
from google.appengine.api import users


class ViewUser(webapp2.RequestHandler):
	def get(self):
		userKey=self.request.path[6:] #Chops off the end of the request path to get the user key
		user=AppUser.get_by_key_name(userKey)
		if not user:
			self.redirect('/?' + urllib.urlencode({'message':'Error: No such user found.'}))

		currentUser = AppUser.getUser()

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'			
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'url': url,
			'url_linktext': url_linktext,
			'user': user,
			'events': [],
			'currentUser':currentUser
		}

		#Displays:
		#Username (nickname)
		#Good/bad event counts
		#Verified status
		#Events (later)

		path = os.path.join(os.path.dirname(__file__), './templates/UserProfile.html')
		self.response.out.write(template.render(path, template_values))


class ViewEvent(webapp2.RequestHandler):
	def get(self):
		eventKey=self.request.path[7:] #Chops off the end of the request path to get the event key
		event=Event.get(eventKey)
		currentUser = AppUser.getUser()
		#if ((not event) or  (not event.verified and not currentUser.verified)):
		#	self.redirect('/?' + urllib.urlencode({'message':'Error: Event not found or could not be accessed.'}))

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'url': url,
			'url_linktext': url_linktext,
			'event' : event,
			'currentUser' : currentUser
		}
		path=os.path.join(os.path.dirname(__file__), './templates/viewEvent.html')
		self.response.out.write(template.render(path, template_values))
		
class ViewMake(webapp2.RequestHandler):
	def get(self):
		user=AppUser.getUser()

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			"user":user,
			'url':url,
			'url_linktext':url_linktext
		}
		path = os.path.join(os.path.dirname(__file__), './templates/MakeEvent.html')
		self.response.out.write(template.render(path, template_values))

	def post(self):
		user = AppUser.getUser()
		eventName=getString("name", self)
		loc=getString("location", self)
		date = getDate("date", self)
		start=getDateTime("start",date, self)
		event = Event(creator=user,name=eventName, location=loc, dateStart=start)
		event.dateEnd=getDateTime("end",date, self)
		event.description=getString("description", self)
		event.host=getString("host", self)
		event.attending=0
		event.put()

		if user.verified:
			event.verify();
			# Auto-verified if the user is, and thanks the user.
			self.redirect('/?' + urllib.urlencode({'message':'''Thanks, yum!'''}))
		self.redirect('/?' + urllib.urlencode({'message':'''Event Created! You'll need to wait for someone to verify it.'''}))
		# redirect message if the user isn't verified.