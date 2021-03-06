from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from src.cal import Cal
import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, 'credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def update_g_c(Cnn, day0):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    Cnn.add_all_Titems(day0)
    for one in Cnn.Titems:
        body = {}
        tup = one.get_all()
        body["summary"] = tup[0] + " " + tup[8]
        # print(tup[0])
        body["start"] = {}
        body["start"]["dateTime"] = tup[1] + "T" + tup[3] + "-04:00:00"
        body["end"] = {}
        body["end"]["dateTime"] = tup[2] + "T" + tup[4] + "-04:00:00"
        service.events().insert(
            calendarId='bloafkanpa3ud3k8dlqnq3qhdc@group.calendar.google.com', body=body).execute()


def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    s = service.calendarList().list().execute()

    body = {"summary": "test", "start": {"dateTime": "2017-09-18T14:00:00-04:00:00"},
            "end": {"dateTime": "2017-09-18T15:00:00-04:00:00"}}

    service.events().insert(
        calendarId='bloafkanpa3ud3k8dlqnq3qhdc@group.calendar.google.com', body=body).execute()


if __name__ == '__main__':
    Cnn = Cal()
    update_g_c(Cnn, "2017-09-18")
