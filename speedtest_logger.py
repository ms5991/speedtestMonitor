#!/usr/bin/python
import time, getopt, sys, os.path, re, datetime, smtplib, json

def write_log(ping, download, upload, verbose, logFile):
	
	pLog = re.findall('[\d]{1,4}\.[\d]{1,3}', ping)[0]
	dLog = re.findall('[\d]{1,4}\.[\d]{1,3}', download)[0]
	uLog = re.findall('[\d]{1,4}\.[\d]{1,3}', upload)[0]

	timestamp = str(datetime.datetime.now())
	toLog = '{0},{1},{2},{3}\n'.format(timestamp, pLog, dLog, uLog)
		
	if verbose: print 'Printing to log: [{0}]'.format(toLog)
		
	if os.path.isfile(logFile):
		with open(logFile, "a") as csvFile:
			csvFile.write(toLog)
	else:
		with open(logFile,"w+") as csvFile:
			csvFile.write('Timestamp,Ping (ms),Download (Mbit/s),Upload (Mbit/s)\n')
			csvFile.write(toLog)

def send_email(output, sendToAddress, emailConfigFile, verbose):

	if verbose: print 'Sending email to {0}'.format(sendToAddress)

	# load config data	
	with open(emailConfigFile) as conf:
		if verbose: print 'Loading json email data...'
		emailData = json.load(conf)
		if verbose: print 'Got username: [{0}] and password: [{1}]'.format(emailData["username"], emailData["password"])
	
	# send via gmail (the email address has to be a gmail
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()

	# this is way easier than I expected
	server.login(emailData["username"], emailData["password"])

	if verbose: print 'Successfully logged in using credentials'

	# use message headers -- you need a blank line between the subject and the message body
	timestamp = str(datetime.datetime.now())
	message = "\r\n".join(["From: {0}".format(emailData["username"]), "To: {0}".format(sendToAddress), "Subject: Speedtest Results", "\nResults: {0}\nAt time: [{1}]".format(output, timestamp)])

	if verbose: print 'Sending: \n[{0}]\n'.format(message)

	# actually sends it
	server.sendmail(emailData["username"], sendToAddress, message)
	server.quit()

	if verbose: print 'Successfully sent email to {0}'.format(sendToAddress)

def main(argv):

	try:
		opts, args = getopt.getopt(sys.argv[1:], "tvl", ["testing","verbose", "log=","email="])
	except getopt.GetoptError, e:
		print 'speedtest_display.py: {0}'.format(str(e))
		sys.exit(2)
	
	# default to normal operations
	testing = False

	# default verbose off
	verbose = False

	# log variables
	log = False
	logFile = '/home/pi/log_speedtest.csv'

	# default no email
	sendToAddress = None
	emailConfigFile = 'email_config.json'

	# OPTIONS EXPLAINATION
	# -t or --testing	: uses dummy data rather than querying speedtest.net
	# -v or --verbose	: prints more information than otherwise
	# -l			: prints data to the CSV file with default log file name "/home/pi/log_speedtest.csv
	# --log			: prints data to the CSV file with the provided file name
	# --email		: sends an email to the provided address after every speedtest
	#
	for opt, arg in opts:
		if opt in ['-t', '--testing']:
			testing = True
			print 'Set to testing mode!'
		elif opt in ['-v','--verbose']:
			verbose = True
		elif opt == '-l':
			log = True
		elif opt == '--log':
			log = True
			logFile = arg
		elif opt == '--email':
			sendToAddress = arg

	# if in testing mode, use fake data
	if not testing:
		print 'Aquiring data from speedtest.net....'
		from subprocess import Popen, PIPE
		process = Popen(["/usr/local/bin/speedtest-cli","--simple"], stdout = PIPE)
		(output, err) = process.communicate()
		exit_code = process.wait()
		if err is not None:
			print str(err)
			print 'Terminating program. Try \'sudo apt-get install speedtest-cli\''
			sys.exit(2)
	else:
		output = 'Ping: 32.000 ms\nDownload: 111.000 MBit/s\nUpload: 6.000 MBit/s'
	
	
	output = output.split('\n')

	# send email	
	if sendToAddress is not None:
		send_email(output, sendToAddress, emailConfigFile, verbose)

	# if this fails, it means speedtest query didn't work.  Happens very rarely
	try:
		ping = output[0]
		download = output[1]
		upload = output[2]
	except:
		ping = 0
		download = 0
		upload = 0

	print 'Result from speedtest: \n\t{0}\n\t{1}\n\t{2}\n'.format(ping, download, upload)

	if log: write_log(ping, download, upload, verbose, logFile)

if __name__ == "__main__":
	main(sys.argv[1:])
