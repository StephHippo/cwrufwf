from Event import  Event
from google.appengine.ext import db
from datetime import timedelta
from datetime import datetime

def getEvents(user):
		query = "WHERE dateStart >= :1 "
		# if not user.verified:
			# query+="AND verified = TRUE "
		#query += "Limit " +(str)(limit*pageNum)+", " + (str)(limit)
		events = Event.gql(query, datetime.now()-timedelta(hours=2)).run()
		events = sorted(events, key=lambda event: event.dateStart) 
		return events