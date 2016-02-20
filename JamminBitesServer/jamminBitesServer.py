import os, os.path
import random
import string
import cherrypy
#import mysql.connector
#import subprocess
#import tinys3
#import boto
#import boto.s3
#import sys
#from boto.s3.key import Key
from jinja2 import Environment, FileSystemLoader

# declare global variables
env = Environment(loader=FileSystemLoader('clientSideFiles'))
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
		return tmpl.render()

	@cherrypy.expose
	def bites(self):
		tmpl = env.get_template('bites.html')
		return tmpl.render()

	@cherrypy.expose
	def about(self):
		tmpl = env.get_template('about.html')
		return tmpl.render()

	@cherrypy.expose
	def contact(self):
		tmpl = env.get_template('contact.html')
		return tmpl.render()



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


