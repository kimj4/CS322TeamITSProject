#this is an implementation to take a given email and scrape the from, to date, subject, and body of email from it.
import re
import json
#this is a placeholder for when we feed in the text#
contents = ""
with open("email.txt") as file:
	data = file.read() #get data of email

	#We're now going to parse the email. Our assumptions:
	#1. There is only one "To" entity
	#2. There is only one "From" entity
	#3. There is only one subject.

	#We will accomplish this by a cascading series of if statements.
	for line in data: #for every line of data in the thingamajig
		toRegex = re.compile('To\:' )
		fromRegex = re.compile('From\:')
		subRegex = re.compile('Subject\:')
		if toRegex.match(): #if there's a "to:" in there
			addressee = line[(toRegex.match().end() + 1):] #slices substring from where the colon is to the end. 			
		elif fromRegex.match(): #if there's a from
			addresser = line[(fromRegex.match().end() + 1):]
		elif subRegex.match():
			subject = line[(subRegex.match().end() + 1):]
		else: #if no subject, to, or from,
		contents = contents + line #append line to contents.


	data = {
	'From' : addresser
	'to' : addressee
	'subject' : subject
	'body' : contents
	}

	with open ('emails.json')