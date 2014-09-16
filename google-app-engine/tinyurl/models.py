"""
Store all the models for TinyURL

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
import uuid

from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import ndb


class Entry(ndb.Model):
    created_time = ndb.DateTimeProperty(auto_now_add=True)
    creator = ndb.StringProperty(required=True)
    url_hash = ndb.StringProperty(required=True)
    url = ndb.StringProperty(required=True)


@ndb.transactional
def create_new_entry(url):
    user = users.get_current_user()
    if not user:
        raise Exception("Not logged in")

    url_hash = generate_url_hash()

    entry = get_entry(url_hash)
    if entry:
        # call this function again to generate a new hash and attempt to
        # create the entry again
        return create_new_entry(url)
    else:
        entry = Entry(
            key=make_entry_key(url_hash),
            creator=user.user_id(),
            url_hash=url_hash,
            url=url,
        )
        entry.put()
        return entry


def get_entry(url_hash):
    key = make_entry_key(url_hash)
    key_str = str(key)
    entry = memcache.get(key_str)

    if entry:
        return entry
    else:
        entry = key.get()
        memcache.set(key_str, entry, time=60 * 10)
        return entry


def make_entry_key(url_hash):
    return ndb.Key("Entry", url_hash)


def generate_url_hash():
    return str(uuid.uuid4())[:6]

