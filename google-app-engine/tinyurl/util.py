"""
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
from urlparse import urlparse

def construct_shortened_url(app_url, url_hash):
    return "{app_url}/g/{url_hash}".format(
        **locals()
    )


def validate_url(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme and parsed_url.netloc
