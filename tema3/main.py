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
from __future__ import print_function
import logging
import httplib2
import os
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from flask import Flask


app = Flask(__name__)


def get_credentials():
    home_dir = os.path.expanduser('~')
    scopes_file = os.path.join(home_dir, '.scopes')
    if not os.path.exists(scopes_file):
        SCOPES = [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/calendar.readonly',
            'https://mail.google.com/',
            'https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/gmail.compose',
            'https://www.googleapis.com/auth/gmail.metadata',
        ]
        handler = open(scopes_file, "w")
        handler.write(json.dumps(SCOPES))
        handler.close()


    handler = open(scopes_file, "r")
    content = handler.read()
    handler.close()
    SCOPES = json.loads(content)

    CLIENT_SECRET_FILE = 'client_secret.json'

    if not os.path.exists(CLIENT_SECRET_FILE):
        handler = open(CLIENT_SECRET_FILE, "wb")
        handler.write("""{"installed":{"client_id":"514021309961-3s50gqong6grrmpa24v2eve1jh982ft2.apps.googleusercontent.com","project_id":"proiect-cloud-200117","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://accounts.google.com/o/oauth2/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"hp0vcAsTVkJ7PrW5S-Sun3p_","redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}""")
        handler.close()

    APPLICATION_NAME = 'Google Calendar API Python Quickstart'

    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    http = httplib2.Http()
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = tools.argparser.parse_args(args=[])
        credentials = tools.run_flow(flow, store, flags, http=http)
        print('Storing credentials to ' + credential_path)
    return credentials


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    credentials = get_credentials()
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = discovery.build('calendar', 'v3', http=http)
    return 'Hello World!'


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
    # app.run()
# [END app]
