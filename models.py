from google.appengine.ext import ndb

class Chat(ndb.Model):
    name = ndb.StringProperty()
    message = ndb.StringProperty()
    time = ndb.StringProperty()