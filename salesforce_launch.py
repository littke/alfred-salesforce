#!/usr/bin/python
# encoding: utf-8

from workflow import Workflow, ICON_WEB, ICON_WARNING, PasswordNotFound
from workflow.notify import notify
import sys
import salesforce_api
import subprocess
import logging
import os
import requests

logging.basicConfig(filename='logging.log',level=logging.INFO,format='%(asctime)s - %(filename)s - %(levelname)s : %(message)s')


def main(wf):

    # Get query from Alfred
    if len(wf.args):
        query = wf.args[0]
    else:
        query = ''

    # Splitting query
    query = query.split()
    if len(query) > 0:
        query_0 = query[0]
    else:
        query_0 = None
    if len(query) > 1:
        query_1 = query[1]
    else:
        query_1 = None

    # Trying to get access_token
    try:
        access_token = wf.get_password('access_token')
    except PasswordNotFound:
        access_token = None

    if query_0 == 'login':

        notify('Salesforce', 'Please connect to your Salesforce account')
        subprocess.Popen(['nohup', 'python', './server.py'])
        subprocess.call(['open', salesforce_api.get_oauth_url()])

    elif query_0 == 'logout':

        wf.delete_password('instance_url')
        wf.delete_password('refresh_token')
        wf.delete_password('access_token')
        
        notify('Salesforce', 'You are logged out')

    elif query_0 == 'debug':

        logging.info(os.path.dirname(requests.__file__))
        logging.info(requests.get("https://www.howsmyssl.com/a/check").text)
        notify("Debug sent to logs")

    elif query_0.startswith('http'):

        subprocess.call(['open', query_0])

    else:

        notify('Else', 'My Text')


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))