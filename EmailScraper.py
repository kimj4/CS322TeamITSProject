#this is an implementation to take a given email and scrape the from, to date, subject, and body of email from it.
import os
import re
import json
from pprint import pprint
#this is a placeholder for when we feed in the text#
contents = ""
addresser = ""
addressee = ""
subject = ""
sent = ""
# input_file_name = 'testEmailMultiple.txt'


def jsonify_file(input_file_name, output_file_name):

	# parse file line by line until you find a line that starts with a 'from:'.
	#  From there, parse each line, looking for any special information, and storing
	#  them as such, and adding the rest to the body of the email.
	#  Repeat this until you hit the next line that starts with 'from:'.
	#   when you do, finalize the cur_email object and push it into the emails_list.
	#  	Reinitialize cur_email and content for the next email.
	#  Once you are done running through all lines, write the list out as a json
	with open(input_file_name, 'r', encoding=None, errors='backslashreplace') as file:
		data = file.readlines() #get data of email
		print ('file successfully opened!')
		#We're now going to parse the email. Our assumptions:
		#1. There is only one "To" entity
		#2. There is only one "From" entity
		#3. There is only one subject.

		emails_list = []
		cur_email_idx = -1
		cur_email = {}
		contents = ''
		for line in data:
			tempLine = line
			tempLine = tempLine.strip()

			toRegex = re.compile('To\:' )
			fromRegex = re.compile('From\:')
			subRegex = re.compile('Subject\:')
			sentRegex = re.compile('Sent\:')


			if toRegex.match(tempLine): #if there's a "to:" in there
				addressee = tempLine[(toRegex.match(tempLine).end() +1):] #slices substring from where the colon is to the end.
				cur_email['to'] = addressee
			elif fromRegex.match(tempLine): #if there's a from
				if ('from' in cur_email):
					# TODO: the following lines are for when/if we want to somehow change
					#  or filter the contents of the body. For example, we might
					#  want to make the body into a list of sentences rather than
					#  a single string. Also, there are a couple weird characters
					#  that need to be taken care of

					#  We may need to split sentences by newline characters since
					#   sometimes people use it instead of closing it with a period.
					# contents = contents.replace('\n', ' ')
					# contents = contents.replace('\t', ' ')
					# contents = contents.replace('-----Original Message-----', '')
					# contents = contents.replace('***********************************************************Please note: Florida has a very broad public records law.Most written communications to or from state officialsregarding state business are public records available to thepublic and media upon request. Your e-mail communicationsmay therefore be subject to public disclosure.', '')

					# TODO: look into replacing the unicode apostrophe into a single quote or something
					cur_email['body'] = contents
					emails_list.append(cur_email)
					cur_email = {}
					contents = ''

				addresser = tempLine[(fromRegex.match(tempLine).end() +1):]
				cur_email['from'] = addresser
			elif subRegex.match(line):
				subject = tempLine[(subRegex.match(tempLine).end() +1):]
				cur_email['subject'] = subject
			elif sentRegex.match(line):
				sent =tempLine[(sentRegex.match(tempLine).end() +1):]
				cur_email['sent'] = sent
			else: #if no subject, to, or from,
				contents = contents + line #append line to contents.

		with open(output_file_name, 'w+') as f:
			json.dump(emails_list, f, indent=4)

def main():
	directory_name = 'JebBushEmails'
	out_directory_name = 'output'
	directory = os.fsencode(directory_name)
	count = 0
	count_limit = 9999999999
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		if filename.endswith(".txt"):
			input_file_name = directory_name + '/' + filename
			output_file_name = out_directory_name + '/' + filename.split('.')[0] + '.json'
			jsonify_file(input_file_name, output_file_name)
			if count == count_limit:
				break;
			count += 1
			# continue
		else:
			continue
	#
	# input_file_name = 'sampleDataset/01+January+2003+Public+2.txt'
	# output_file_name = 'emails.json'
	# jsonify_file(input_file_name, output_file_name)

if __name__ == '__main__':
	main()
