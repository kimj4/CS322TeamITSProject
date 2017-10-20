#this is an implementation to take a given email and scrape the from, to date, subject, and body of email from it.
import re
import json
#this is a placeholder for when we feed in the text#
contents = ""
addresser = ""
addressee = ""
subject = ""
sent = ""
with open("TestEmail1.txt") as file:
	data = file.readlines() #get data of email
	print ('file successfully opened!')
	#We're now going to parse the email. Our assumptions:
	#1. There is only one "To" entity
	#2. There is only one "From" entity
	#3. There is only one subject.

	#We will accomplish this by a cascading series of if statements.
	for line in data: #for every line of data in the thingamajig
		
		tempLine = line
		tempLine = tempLine.strip()

		
		toRegex = re.compile('To\:' )
		fromRegex = re.compile('From\:')
		subRegex = re.compile('Subject\:')
		sentRegex = re.compile('Sent\:')
		
		if toRegex.match(tempLine): #if there's a "to:" in there
			addressee = tempLine[(toRegex.match(tempLine).end() +1):] #slices substring from where the colon is to the end.
			print ('found an addressee') 			
		elif fromRegex.match(tempLine): #if there's a from
			addresser = tempLine[(fromRegex.match(tempLine).end() +1):]
			print ('found an addresser')
		elif subRegex.match(line):
			subject = tempLine[(subRegex.match(tempLine).end() +1):]
			print ('found a subject')
		elif sentRegex.match(line):
			sent =tempLine[(sentRegex.match(tempLine).end() +1):]
		else: #if no subject, to, or from,
			contents = contents + line #append line to contents.

#dumps the email file.

	datadump = {
	'From' : addresser,
	'to' : addressee,
	'subject' : subject,
	'sent' : sent,
	'body' : contents
	}

	with open ('emails.json', 'w+') as f:
		json.dump(datadump, f)