#!/usr/bin/env python3
#
# Copyright (c) 2019 Nutanix Inc. All Rights Reserved
#
# Nutanix REST API v2
#
# Script Name: SetAlerts.py
# Script Version: 1.0
# Author: Bob Relyea, SE Nutanix bob.relyea@nutanix.com
#
# This script uses Python 3.7.3.
# This script is to bulk edit the alerts in the 'Alert Policy
# Editor'. Those alerts are triggered by Health Checks, hence the
# health_check branch of the API.
#
# The script looks for a command line argument which woulb be a simple
# text file containing of alert information. The lines are as follows:
# '{healthcheck id},{'true' or 'false'},{alert Severity}
# 	ex: '000586cd-743f-f6dd-4425-001fc69c383b::11024,false,kWarning'
# The single quotes are delimeters only. There are no spaces after the
# commas. The first value is the healthcheck id. It is usually, though not
# always the ClusterID::AlertID. The healthcheck id can actually be obtained
# by doing a GET against the healthcheck branch of the API. They will all
# be listed as the "id": value in the JSON.
#
# The script will loop through the file indicated on the command line for
# each line in the file.
# The Response Code return (hopefully 200) can be piped to a text file for
# record keeping. Future versions will likely do this automatically.
# NOTE: You will need a Python library called "requests" which is available from
# the url: http://docs.python-requests.org/en/latest/user/install/#install
#
# Special thanks to Mark Leighty, and Ian Noble, my scripting mentor. Without 
# them, this code never gets written. One day I will be worthy!!!

import json
import os
import random
import requests
import sys
import unicodedata
import traceback
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# open alert configuration file indicated on the command line

alert_file = str(sys.argv[1])

# Authenticate cluster connection with following
# define cluster IP, username, password, and base URL

class NtxRestApi():
	def __init__(self):

		self.serverIPAddress = "10.68.69.102"
		self.username = "admin"
		self.password = "5up3rM@n1"
		BASE_URL = 'https://%s:9440/PrismGateway/services/rest/v2.0'
		self.base_url = BASE_URL % self.serverIPAddress
		self.session = self.get_server_session(self.username, self.password)

# Create REST client session for server connection
# SSL cert verification must be disabled or script will not run

	def get_server_session(self, username, password):

		session = requests.Session()
		session.auth = (username, password)
		session.verify = False
		session.headers.update({'Content-Type': 'application/json; charset=utf-8'})
		return session

	def setAlert(self):
		healthChkURL = self.base_url + "/health_checks"

		# open the file here instead

		alert_config = open(alert_file)
		for line in alert_config:
			lineStrAry = []
			lineStrAry = line.split(',')
			hlthChkid = lineStrAry[0]
			alertState = lineStrAry[1]
			alertSev = lineStrAry[2]
			alertSev = alertSev.replace("\n","")

		# create JSON from open file

			payload = {}
			payload["id"] = hlthChkid
			payload["severity_threshold_infos"] = [{'enabled': alertState, 'severity': alertSev}]
			payloadInJson = json.dumps(payload)
			#print(healthChkURL)
			print(payloadInJson)
			serverResponse = self.session.put(healthChkURL, data=payloadInJson)
			print ("Response code: %s" % serverResponse.status_code)
		return json.loads(serverResponse.text)

if __name__ == "__main__":
	try:
		requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
		callRestApi = NtxRestApi()
		ntxHlthCkAlert = callRestApi.setAlert()

	except Exception as ex:
		print (ex)
		sys.exit(1)