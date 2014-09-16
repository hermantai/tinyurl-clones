"""
RedirectHandler takes a url_hash and redirects to the underlying url given by
url_hash.
/g/<url_hash>

   Copyright 2014 Herman Tai

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import logging

import webapp2

import models as tmodels
import util as tutil


class RedirectHandler(webapp2.RequestHandler):
    def get(self, url_hash):
        entry = tmodels.get_entry(url_hash)
        if entry:
            self.redirect(entry.url.encode("utf-8"))
        else:
            logging.debug("referrer: %s", self.request.referer)
            self.response.write(
                "Bad url: {}".format(
                    tutil.construct_shortened_url(
                        self.request.host,
                        url_hash,
                    )
                )
            )
