#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import jinja2
import webapp2
import sys
from models import Chat
from datetime import datetime
from operator import attrgetter

reload(sys)
sys.setdefaultencoding("utf8")

template_dir = os.path.join(os.path.dirname(__file__), "html")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        message_list = Chat.query().fetch()
        ordered_list = sorted(message_list, key=attrgetter("time"), reverse=True)
        params = {"message_list": ordered_list}
        return self.render_template("index.html", params=params)

    def post(self):
        name = self.request.get("name")
        message = self.request.get("message")
        time = datetime.now().strftime("%d.%m.%Y ob %H:%M")
        save_message = Chat(name=name, message=message, time=time)
        save_message.put()
        return self.redirect_to("main-page")


app = webapp2.WSGIApplication([
    webapp2.Route("/", MainHandler),
    webapp2.Route("/", MainHandler, name="main-page")
], debug=True)
