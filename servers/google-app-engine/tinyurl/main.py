#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
Main page of TinyURL. It shows a form for users to create a shortened url for
a given url. This handler also handles the creation of the shortened url.
"""
import os
from urlparse import urlparse

import jinja2
import webapp2

import models as tmodels
from redirect import RedirectHandler
import util as tutil


TEMPLATE_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.getcwd())
)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = TEMPLATE_ENV.get_template("home.html")
        context = {
            'req': self.request,
        }

        self.response.write(template.render(context))

    def post(self):
        url = self.request.params['url']

        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            # valid url
            new_entry = tmodels.create_new_entry(url)
            new_url = tutil.construct_shortened_url(
                self.request.application_url,
                new_entry.url_hash,
            )
        else:
            new_url = None

        template = TEMPLATE_ENV.get_template("creation_confirmed.html")
        context = {
            'new_url': new_url,
            'original_url': url,
        }

        self.response.write(template.render(context))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/g/(.*)', RedirectHandler),
], debug=True)
