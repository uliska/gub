#!/usr/bin/python
import re

import smtplib
import os
import time
import email.MIMEText
import email.Message
import email.MIMEMultipart
import optparse
import md5
import dbhash
import sys
import xml.dom.minidom

## TODO: should incorporate checksum of lilypond checkout too.
def try_checked_before (hash, canonicalized_target):
	if not os.path.isdir ('test'):
		os.makedirs ('test')

	db_file = 'test/gub-done-%s.db' % canonicalized_target
	print 'using database ', db_file
	
	db = dbhash.open (db_file, 'c')
	was_checked = db.has_key (hash)
	db[hash] = '1'
	db.close ()
	return was_checked

def read_last_patch ():
	"""Return a dict with info about the last patch"""
	
	last_change = os.popen ('darcs changes --xml --last=1').read ()
	dom = xml.dom.minidom.parseString(last_change)
	patch_node = dom.childNodes[0].childNodes[1]
	name_node = patch_node.childNodes[1]

	d = dict (patch_node.attributes.items())
	d['name'] = patch_node.childNodes[1].childNodes[0].data
	return d

def system (cmd):
	print cmd
	stat = os.system (cmd)
	if stat:
		raise 'Command failed', stat

def result_message (options, subject, parts) :
	"""Concatenate PARTS to a Message object."""
	
	if not parts:
		parts.append ('(empty)')
	
	parts = [email.MIMEText.MIMEText (p) for p in parts if p]

	msg = parts[0]
	if len (parts) > 1:
		msg = email.MIMEMultipart.MIMEMultipart()
		for p in parts:
			msg.attach (p)
	
	msg['Subject'] = 'GUB Autobuild: %s' % subject

	msg.epilogue = ''

	return msg

def opt_parser ():
	p = optparse.OptionParser()
	p.add_option ('-t', '--to',
		      action ='append',
		      dest = 'address',
		      default = [],
		      help = 'where to send error report')
	p.add_option ('-f', '--from',
		      action ='store',
		      dest = 'sender',
		      default = os.environ['EMAIL'],
		      help = 'whom to list as sender')
	p.add_option ('-s', '--smtp',
		      action ='store',
		      dest = 'smtp',
		      default = 'localhost',
		      help = 'SMTP server to use.')

	return p

def read_tail (file, amount=10240):
	f = open (file)
	f.seek (0, 2)
	length = f.tell()
	f.seek (- min (length, amount), 1)
	return f.read ()

################################################################
# main
def xml_patch_name (patch):
	name_elts =  patch.getElementsByTagName ('name')
	try:
		return name_elts[0].childNodes[0].data
	except IndexError:
		return ''
	
def get_release_hash (name):
	xml_string = os.popen ('darcs changes --xml').read()
	dom = xml.dom.minidom.parseString(xml_string)
	patches = dom.documentElement.getElementsByTagName('patch')
	patches = [p for p in patches if not re.match ('^TAG', xml_patch_name (p))]

	release_hash = md5.new ()
	for p in patches:
		release_hash.update (p.toxml ())
		
	release_hash = release_hash.hexdigest()
	print 'release hash is ', release_hash
	
	return release_hash

def test_target (options, target):
	canonicalize = re.sub('[ \t\n]', '_', target)
	canonicalize = re.sub ('[^a-zA-Z]', '_', canonicalize)

	release_hash = get_release_hash (canonicalize)

	if try_checked_before (release_hash, canonicalize):
		print 'release has already been checked: ', release_hash 
		sys.exit (0)

	last_patch = read_last_patch()
	last_patch['release_hash'] = release_hash


	logfile = 'test/test-%(canonicalize)s.log' %  locals()
	stat = os.system ("nice %(target)s >& %(logfile)s" %  locals())
	base_tag = 'success-%(canonicalize)s-' % locals ()
	release_id = '''
Last patch of this release:

%(local_date)s - %(author)s

	* %(name)s\n\n

MD5 of inventory: %(release_hash)s

''' % last_patch

	release_id += '\n\nTesting command: %s\n\n' %  target
	msg = None
	if stat: 
		body = read_tail (logfile)
		diff = os.popen ('darcs diff -u --from-tag %s' % base_tag).read ()
		
		msg = result_message (options, '%s FAIL' % target , [release_id,
							body, diff])
	else:
		tag = base_tag + last_patch['date']
		system ('darcs tag %s' % tag)
		system ('darcs push -a -t %s ' % tag)
		
		msg = result_message (options, '%s SUCCESS' % target,
				      [release_id,
				       "Tagging with %s\n\n" % tag])


	COMMASPACE = ', '
	msg['From'] = options.sender
	msg['To'] = COMMASPACE.join (options.address)
	connection = smtplib.SMTP (options.smtp)
	connection.sendmail (options.sender, options.address, msg.as_string ())


	
def main ():
	(options, args) = opt_parser().parse_args ()

	for a in args:
		test_target (options, a)

main()
