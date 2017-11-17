#this is an implementation to take a given email and scrape the from, to date, subject, and body of email from it.
import os
import re
import json
from pprint import pprint
import multiprocessing

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
		isDisclaimer = False # in an effort to get rid of the FL information law disclaimer
		for line in data:

			# if '’' in line:
			# 	print(line)
			line = line.replace('’', '\'')

			line = line.replace('> ', '')
			line = line.replace('>', '')
			# if 'Original Message' in line:
			# 	print(line)

			tempLine = line
			tempLine = tempLine.strip()

			toRegex = re.compile('To\:' )
			fromRegex = re.compile('From\:')
			subRegex = re.compile('Subject\:')
			sentRegex = re.compile('[ \t]*Sent\:')
			starsRegex = re.compile('[*]+')
			ccRegex = re.compile('[cC][cC] *:')
			rangleRegex = re.compile('>')
			omRegex = re.compile('.*[- ]*Original Message[ -]*')


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
					contents = contents.replace('\n', ' ')
					contents = contents.replace('\t', ' ')

					contents = contents.replace('  ', ' ')

					# TODO: look into replacing the unicode apostrophe into a single quote or something
					cur_email['body'] = contents
					emails_list.append(cur_email)
					cur_email = {}
					contents = ''

				addresser = tempLine[(fromRegex.match(tempLine).end() +1):]
				cur_email['from'] = addresser
				# if you've found another 'from' then, the disclaimer is probably over
				isDisclaimer = False
			elif subRegex.match(line):
				subject = tempLine[(subRegex.match(tempLine).end() +1):]
				cur_email['subject'] = subject
			elif sentRegex.match(line):
				sent =tempLine[(sentRegex.match(tempLine).end() +1):]
				cur_email['sent'] = sent
			elif starsRegex.match(line):
				# the line of stars marks the beginning of the disclaimer
				isDisclaimer = True
				contents = contents + ''
			elif ccRegex.match(line):
				# probably won't need carbon copy information
				continue
			elif omRegex.match(line):
				continue

			else: #if no subject, to, or from,
				if not isDisclaimer:
					# only add the line if it is not a part of the disclaimer
					contents = contents + line #append line to contents.

		with open(output_file_name, 'w+') as f:
			json.dump(emails_list, f, indent=4)

def scrape(thread_name, thread_number, total_thread_count):
	count_limit = 400
	num_to_process = count_limit // total_thread_count

	start = num_to_process * (thread_number - 1)

	directory_name = 'JebBushEmails'
	out_directory_name = 'output'
	directory = os.fsencode(directory_name)
	count = 0
	count_to_start = 0;
	for file in os.listdir(directory):
		if count_to_start < start:
			count_to_start += 1
		else:
			filename = os.fsdecode(file)
			if filename.endswith(".txt"):
				input_file_name = directory_name + '/' + filename
				# output_file_name = out_directory_name + '/' + filename.split('.')[0] + '.json'
				output_file_name = out_directory_name + '/' + str(count_to_start) + '.json'
				jsonify_file(input_file_name, output_file_name)
				if count == num_to_process:
					break;
				else:
					count += 1
					count_to_start += 1
					continue
	return

def main():
	cpu_count = multiprocessing.cpu_count()
	pool = multiprocessing.Pool( cpu_count )
	tasks = []
	tNum = 0
	max_t = 4
	while tNum < max_t:
		tNum += 1
		tasks.append( (str(tNum), tNum, cpu_count) )
	results = []
	for t in tasks:
		results.append( pool.apply_async( scrape, t ) )

	r = []
	for result in results:
		r.append(result.get())

	# input_file_name = 'sampleDataset/01+January+2003+Public+2.txt'
	# output_file_name = 'emails.json'
	# jsonify_file(input_file_name, output_file_name)

if __name__ == '__main__':
	main()
