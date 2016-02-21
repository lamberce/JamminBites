import os, os.path
import random
import string
import cherrypy
#import mysql.connector
import subprocess
#import tinys3
#import boto
#import boto.s3
#import sys
#from boto.s3.key import Key
from jinja2 import Environment, FileSystemLoader
import smtplib
from email.mime.text import MIMEText

# declare global variables
env = Environment(loader=FileSystemLoader('clientSideFiles'))
commentEmail = 'lamberce@rose-hulman.edu'
# S3_ACCESS_KEY = 'AKIAI2L42BGVQS5V57QA'
# S3_SECRET_KEY = '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'

# config = {
#         'user': 'Floptical',
#         'password': 'Password1',
#         'host': 'floptical-relational-database.cxrbiaxhps5f.us-west-2.rds.amazonaws.com',
#         'database': 'flopticalDatabase'
# }


class ServeSite(object):
	@cherrypy.expose
	def index(self):
		tmpl = env.get_template('index.html')
		params = {}
		params['homeSelected'] = "class='selected'"
		return tmpl.render(params)

	@cherrypy.expose
	def bites(self):
		tmpl = env.get_template('bites.html')
		params = {}
		params['ourBitesSelected'] = "class='selected'"
		return tmpl.render(params)

	@cherrypy.expose
	def about(self):
		tmpl = env.get_template('about.html')
		params = {}
		params['aboutSelected'] = "class='selected'"
		return tmpl.render(params)

	@cherrypy.expose
	def contact(self, message=""):
		tmpl = env.get_template('contact.html')
		params = {}
		params['contactSelected'] = "class='selected'"
		params['commentSubmittedMessage'] = message
		return tmpl.render(params)

	@cherrypy.expose
	def checkout(self):
		tmpl = env.get_template('checkout.html')
		params = {}
		params['checkoutSelected'] = "class='selected'"
		return tmpl.render(params)

	@cherrypy.expose
	def sendComment(self,name="",email="",subject="",message=""):
		if name != "Name" and email != "Email" and subject != "Subject":
			subject = email + ": " + subject
			os.system("""echo '%s' | mail -s '%s' '%s'"""%(message, subject, commentEmail))

			raise cherrypy.HTTPRedirect("""/contact?message='Your comments have been sent!'""")
		else:
			raise cherrypy.HTTPRedirect("""/contact""")

	@cherrypy.expose
	def addToCart(self, itemId=""):
		print itemID=""
		return "Added to cart"


if __name__ == '__main__':
	conf = {
		'global': {
		'server.max_request_body_size': 0
		},
		'/': {
			'tools.sessions.on' : True,
			'tools.staticdir.root' : os.path.abspath(os.getcwd())
		},
		'/css': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './clientSideFiles/css'
		},
		'/js': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './clientSideFiles/js'
		},
		'/fonts': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './clientSideFiles/fonts'
		},
		'/images': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './clientSideFiles/images'
		}
	}

cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(ServeSite(), '/',conf)


