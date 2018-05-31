# Copyright 2015 Google Inc. All Rights Reserved.
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

# [START app]
import logging

from flask import Flask
import os
import requests

app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    index_page_path = os.path.join("resources", "index.html")
    handler = open(index_page_path, "rb")
    content = handler.read()
    handler.close()
    return content

@app.route('/maps')
def get_maps():
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=123+main+street&key=AIzaSyA9gJYeSa9mWVM5GEPzY0JazaqDRvB8tDQ'
    rr = requests.get(url=url)
    content = rr.json()
    if content["status"] == "OK":
        s = ''
        for item in content["results"]:
            s += "{} {}<br>".format(item["formatted_address"].encode("utf-8"), item["name"].encode("utf-8"))
        return s
    else:
        return "Invalid Request"

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
