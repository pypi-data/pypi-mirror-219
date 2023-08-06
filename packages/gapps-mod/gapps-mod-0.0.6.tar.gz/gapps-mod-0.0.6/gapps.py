#!/usr/bin/env python3.8

#
# Google API/Gapps Service Py Lib
#

#
# Imports
#

# The Usual Suspects
import os, sys, io
import re, random, time, datetime
from datetime import datetime

# For parsing things
import argparse, configparser

# Because... there is web stoof in here
import requests, json

# Stoof for Email/MIME/Base64 crapola
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

import mimetypes
import base64

# My Py Helper Lib
import py_helper as ph
from py_helper import Msg, DbgMsg, ErrMsg, DebugMode, ModuleMode

# Google Stuff
from googleapiclient.discovery import build
from googleapiclient import errors
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

#
# Classes
#


#
# Variables
#

# Version Stuff
VERSION=(0,0,6)
Version = __version__ = ".".join([ str(x) for x in VERSION ])

# Config Location (if in Use)
GappsConfigSection = "gapps"
GappsCredsValue = "gappscreds"
GappsTokenValue = "gappstoken"

ConfigFile = "config.ini"
Config = None
GappsConfig = None

# Gapps App Scopes
GappsAppScopes = {
	"spreadsheets.readonly" : "https://www.googleapis.com/auth/spreadsheets.readonly",
	"gmail.readonly" : "https://www.googleapis.com/auth/gmail.readonly",
	"gmail" : "https://mail.google.com/"
}

# Official Service Names Translation Table
ServiceNames = {
	"sheets" : "sheets",
	"gmail" : "gmail",
	"email" : "gmail"
}

# Service API Version
ServiceVersion = "v4"

Scopes = list()
CredsFile = None
Creds = None
TokenFile = None
Service = None

#
# General Functions
#

# Build a Scope List for GetService Call
def BuildScopes(scopes):
	global GappAppScopes, Scopes

	scopelist = list()
	url_chk = re.compile("^http[s]{0,1}\://[\w\-\.]+$")

	if type(scopes) is str:
		if url_chk.search(scopes):
			scopelist.append(scopes)
		else:
			scopelist.append(GappsAppScopes[scopes])
	elif type(scopes) is list:
		for scope in scopes:
			if url_chk.search(scope):
				scopelist.append(scope)
			else:
				scopelist.append(GappsAppScopes[scope])

	Scopes = list(scopelist)

	return scopelist

def ReAuthToken(credfile,scopes):
	"""Reauthorize a Refresh Token"""

	# This will activate a Lynx like web browser
	# If using the supplied reauth URL, the browser being used must be running on the host
	# Where this script is running

	flow = InstalledAppFlow.from_client_secrets_file(credfile,scopes)
	creds = flow.run_local_server(port=0)

	return creds

#
# Get Service Function (The Main Function)
#

# Get Google Service (for email, spreadsheets, etc)
def GetService(scopes=None,credfile='credentials.json',tokenfile='token.json',svc_name=ServiceNames["gmail"],svc_version=ServiceVersion):
	global Creds, Service, Scopes

	service = None
	creds = None

	if scopes == None:
		scopes = Scopes

	DbgMsg(scopes)

	if os.path.exists(tokenfile):
		creds = Creds = Credentials.from_authorized_user_file(tokenfile,scopes)

	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			try:
				creds.refresh(Request())
			except Exception as err:
				# This will create an interactive Lynx like web browser
				creds = Creds = ReAuthToken(credfile,scopes)
		else:
			# This will create an interactive Lynx like web browser
			creds = Creds = ReAuthToken(credfile,scopes)

		with open(tokenfile,"w") as token:
			token.write(creds.to_json())

	Service = build(svc_name,svc_version,credentials=creds)

	return Service

#
# Email Specific Helpers
#

# List Email Labels
def ListLabels(service=None):
	global Service

	if not service:
		service = Service

	results = service.users().labels().list(userId="me").execute()
	labels = results.get('labels',[])

	return labels

# Find Messages
def FindMessages(query, user_id="me", service=None):
	"""List Messages from inbox that match query"""

	global Service

	messages = None

	if service == None:
		service = Service

	try:
		messages = list()

		response = service.users().messages().list(userId=user_id, q=query).execute()

		if 'messages' in response:
			messages.extend(response['messages'])

		while 'nextPageToken' in response:
			page_token = response['nextPageToken']

			response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()

			messages.extend(response['messages'])

	except Exception as err:
		ErrMsg(err,"An error occurred trying to get messages list with query")

	return messages

# List Messages in Inbox
def ListMessages(user_id="me", service=None):
	"""Get Messages from Inbox"""

	global Service

	if service == None:
		service = Service

	messages = None

	try:
		messages = list()

		response = service.users().messages().list(userId=user_id).execute()

		if 'messages' in response:
			messages.extend(response['messages'])

		while 'nextPageToken' in response:
			page_token = response['nextPageToken']

			response = service.users().messages().list(userId=user_id, pageToken=page_token).execute()

			messages.extend(response['messages'])

	except Exception as err:
		ErrMsg(err,"An error occurred trying to get messages list")

	return messages

# Get All Labels in Account (current service)
def GetLabels(user_id="me",service=None):
	"""Get Labels in current account (service)"""

	global Service

	results = list()

	if service == None:
		service = Service

	results = service.users().labels().list(userId=user_id).execute()

	labels = results.get("labels",[])

	return labels

# Get Label IDs
def GetLabelIDs(labels,user_id='me',service=None):
	"""Get Label IDs or supplied labels"""

	global Service

	label_ids = list()

	if service == None:
		service = Service

	results = GetLabels(user_id,service)

	if len(results) > 0:
		if type(labels) == str:
			labels = [ labels ]

		for label in labels:
			for result_label in results:
				if result_label['name'] == label:
					label_ids.append(result_label['id'])

	return label_ids

# Change A Messages Label(s)
def ChangeLabels(msg_id,msg_labels,user_id="me",service=None):
	"""Add or remove a label (or labels) from a message"""

	global Service

	success = True

	if service == None:
		service = Service

	try:
		message = service.users().messages().modify(uerId=user_id, id=msg_id, body=msg_labels).execute()
	except Exception as err:
		ErrMsg(err,"An error occurred when adding a label to a message")
		success = False

	return success

# Build a label modifiction dictionary for ChangeLabels
def BuildLabelMod(labels, mod=None, add=True, user_id='me', service=None):
	"""Build a label modification dictionary"""

	if mod == None:
		mod = { 'removeLabelIds' : list(), 'addLabelIds' : list() }

	if add:
		ids = GetLabelIDs(labels, user_id, service)

		mod['addLabelIds'].extend(ids)
	else:
		ids = GetLabelIDs(labels, user_id, service)

		mod['removeLabelIds'].extend(ids)

	return mod

# Add A Label To A Mesage (convenience function)
def AddLabel(label, mod=None, user_id='me', service=None):
	"""Add a label to a message"""

	mod = BuildLabelMod(label,mod,True,user_id,service)

	return mod

# Remove Label From A Message (convenience function)
def RemoveLabel(label, mod=None, user_id='me', service=None):
	"""Remove a label from a message"""

	mod = BuildLabelMod(label, mod, False, user_id, service)

	return mod

# Save Attachments From Message
def SaveAttachments(msg_id, save_in, user_id='me', service=None):
	"""Get Attachments from message"""

	global Service

	if service == None:
		service = Service

	attachments = list()

	attachment_file = None

	try:
		message = service.users().messages().get(userId=user_id, id=msg_id).execute()

		for part in message['payload']['parts']:
			if part['filename']:
				DbgMsg("Attachment {}".format(part['filename']), prefix=">>>")

				if 'data' in part['body']:
					data = part['body']['data']
				else:
					att_id = part['body']['attachmentId']
					att = service.users().messages().attachments().get(userId=user_id, messageId=msg_id, id=att_id).execute()
					data = att['data']

				file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))

				attachment_file = os.path.join(save_in,part['filename'])

				attachment_file = ph.NoClobber(attachment_file)

				attachments.append(attachment_file)

				with open(attachment_file, 'wb') as f:
					f.write(file_data)

	except errors.HttpError as error:
		ErrMsg(error,"An error occurred trying to save an email attachment")

	return attachments

# Create An Email Message
def CreateMessage(sender,to,subject,message_text):
	"""Create a message for an email.

	Args:
		sender: Email address of the sender.
		to: Email address of the receiver.
		subject: The subject of the email message.
		message_text: The text of the email message.

	Returns:
		An object containing a base64url encoded email object.
	"""

	message=MIMEText(message_text)
	message['to'] = to
	message['from'] = sender
	message['subject'] = subject

	raw = base64.urlsafe_b64encode(message.as_bytes())

	return {'raw': raw.decode() }

# Create An Email Message With Attachment
def CreateMessageWithAttachment(sender, to, subject, message_text, file):
	"""Create a message for an email.

	Args:
		sender: Email address of the sender.
		to: Email address of the receiver.
		subject: The subject of the email message.
		message_text: The text of the email message.
		file: The path to the file to be attached.

	Returns:
		An object containing a base64url encoded email object.
	"""

	message = MIMEMultipart()
	message['to'] = to
	message['from'] = sender
	message['subject'] = subject

	msg = MIMEText(message_text)
	message.attach(msg)

	content_type, encoding = mimetypes.guess_type(file)

	if content_type is None or encoding is not None:
		content_type = 'application/octet-stream'

	main_type, sub_type = content_type.split('/', 1)

	if main_type == 'text':
		fp = open(file, 'rb')
		msg = MIMEText(fp.read(), _subtype=sub_type)
		fp.close()
	elif main_type == 'image':
		fp = open(file, 'rb')
		msg = MIMEImage(fp.read(), _subtype=sub_type)
		fp.close()
	elif main_type == 'audio':
		fp = open(file, 'rb')
		msg = MIMEAudio(fp.read(), _subtype=sub_type)
		fp.close()
	else:
		fp = open(file, 'rb')
		msg = MIMEBase(main_type, sub_type)
		msg.set_payload(fp.read())
		encoders.encode_base64(msg)
		fp.close()

	filename = os.path.basename(file)
	msg.add_header('Content-Disposition', 'attachment', filename=filename)
	message.attach(msg)

	raw = base64.urlsafe_b64encode(message.as_bytes())

	return {'raw': raw.decode() }

# Send A Message
def SendMessage(user_id, message, service=None):
	"""Send an email message.

	Args:
		service: Authorized Gmail API service instance.
		user_id: User's email address. The special value "me"
		can be used to indicate the authenticated user.
		message: Message to be sent.

	Returns:
		Sent Message.
	"""

	global Service

	if not service:
		service = Service

	try:
		message = (service.users().messages().send(userId=user_id, body=message).execute())
		print('Message Id: %s' % message['id'])
	except errors.HttpError as error:
		print('An error occurred: %s' % error)

	return message

# Send Message Convenience Wrapper
def SendEmail(user_id, message, service=None):
	SendMessage(user_id,message,service)

#
# Spreadsheet Specific Helpers
#

# GetSheetId:
def GetSheetId(sheets,targetlbl):
	sheetId = None

	for row in sheets:
		if row[0] == targetlbl:
			sheetId = row[1]
			break

	return sheetId

# Get Spreadsheet from Service
def GetSpreadSheet(spreadsheetid,service=None):
	"""
	GetSpreadSheet - Return Gapps service spreadsheet instance

	spreadsheetid = id of spreadsheet to get
	service = Optional Gapps Service Instance
	"""

	global Service

	if service == None:
		service = Service

	sheets = service.spreadsheets()

	sheet = None
	error = None

	try:
		sheet = sheets.get(spreadsheetId=spreadsheetid).execute()
	except Exception as err:
		DbgMsg(f"An error occurred trying to get a sheet {spreadsheetid}")
		error = err

	return sheet, error

# Get List of Worksheets in Spreadsheet
def ListWorksheets(spreadsheet):
	"""
	ListWorkSheets - Get list of worksheets in spreadsheet supplied
	"""

	worksheets = spreadsheet.get('sheets','')

	return worksheets

# Get A Range of Values From Supplied Sheet ID
def GetValues(range, sheetId, service=None):
	"""
	Get Values (Range) from Supplied SheetID

	range = values range
	sheetId = The sheet ro extract the values from
	service = Optional service instance, useful when dealing with multiple services, otherwise it is optional

	"""

	global Service

	if service == None:
		service = Service

	values = None

	sheets = service.spreadsheets()
	selectedRange = sheets.values().get(spreadsheetId=sheetId,range=range).execute()
	values = selectedRange.get('values', [])

	return values

# Determine If WorkSheet Name Appears In Work Sheet List
def WorksheetInSheet(wrksheetName,wrkSheetList):
	"""
	Determine if supplied worksheet name is in worksheet list
	"""

	result = False

	for wrksheet in wrkSheetList:
		title = wrksheet.get("properties",{}).get("title","Sheet1")
		if wrksheetName == title:
			result = True
			break

	return result

#
# Test Infrastructure
#

# Test Stub
def test():
	global ConfigFile, Config, GappsConfig, CredsFile, TokenFile
	global GappsConfigSection, CredsValue, GappsTokenValue

	if ConfigFile and os.path.exists(ConfigFile):
		Config = configparser.ConfigParser()

		try:
			Config.read(ConfigFile)
		except Exception as err:
			print("An error occurred trying to load the config file")
			Config = None

		if Config: print("Config loaded")

		if Config.has_section(GappsConfigSection):
			GappsConfig = Config[GappsConfigSection]

			if Config.has_option(GappsConfigSection,CredsValue):
				CredsFile = GappsConfig[CredsValue]

				if Config.has_option(GappsConfigSection,GappsTokenValue):
					TokenFile = GappsConfig[GappsTokenValue]

					if CredsFile and TokenFile: print("Creds/Token File Paths Loaded, good to go")
				else:
					print("Has no token option, bummer...")
			else:
				print("Has no Creds option, bummer...")
		else:
			print("Config had Gapps Section")

	else:
		print("Either ConfigFile was not defined or does not exist, either way, NOT Loaded")

# Test Creds on Spreadsheet
def sheets_test():
	global CredsFile, TokenFile

	test()

	scopes = BuildScopes("spreadsheets.readonly")

	service = GetService(scopes,CredsFile,TokenFile)

	sheet = "West Campus"

	# Providing service here is optional. If dealing with more then one service,
	# this is useful. But if one service, then there is no need.
	objWorkspace = GetSpreadSheet(sheet,service)
	wrksheetList = ListWorksheets(objWorkspace)

	sheet_range = "!A1:K"

	values = GetValues(sheet_range,service,sheet)

	for row in values:
		for cell in row:
			print(cell,newline='')

		print("")

# Test Creds on Gmail
def gmail_test():
	global CredsFile, TokenFile

	test()

	scopes = BuildScopes("gmail")

	service = GetService(scopes,CredsFile,TokenFile,svc_name=ServiceNames["gmail"],svc_version="v1")

	message = CreateMessage("eric.johnfelt@stonybrook.edu","ejohnfelt@hotmail.com","A test","Kewl!!!! Finally!!!!")

	SendMessage("me",message,service=service)

#
# Requisite Main Loop
#

if __name__ == "__main__":
	DebugMode(True)
	ModuleMode(True)

	parser = argparse.ArgumentParser(description="Gapps Module")

	parser.add_argument("-c","--creds",default="credentials.txt",required=False,help="Credentials file")
	parser.add_argument("-t","--token",default="token.txt",required=False,help="Access token file")
	parser.add_argument("cmd",choices=["test","reauth"],help="Command to execute")

	args = parser.parse_args()

	if args.creds is not None:
		CredsFile = args.creds

	if args.token is not None:
		TokenFile = args.token

	if args.cmd is not None:
		if args.cmd == "test":
			test()
		elif args.cmd == "reauth":
			scopes = BuildScopes("spreadsheets.readonly")
			creds = ReAuthToken(TokenFile,scopes)
