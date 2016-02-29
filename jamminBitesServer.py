import os, os.path
import random
import string
import cherrypy
import Cookie
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
ordersEmail = 'lamberce@rose-hulman.edu'
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
		if cherrypy.session.get('itemsInCart') == None:
			params['amountInCart'] = 0
		else:
			params['amountInCart'] = (cherrypy.session['itemsInCart'])['amountInCart']
		return tmpl.render(params)

	@cherrypy.expose
	def bites(self):
		tmpl = env.get_template('bites.html')
		params = {}
		params['ourBitesSelected'] = "class='selected'"

		if 'HTTP_COOKIE' in os.environ:
			cookie_string = os.environ.get('HTTP_COOKIE')
		if cherrypy.session.get('itemsInCart') == None:
			params['amountInCart'] = 0
		else:
			params['amountInCart'] = (cherrypy.session['itemsInCart'])['amountInCart']
		return tmpl.render(params)

	@cherrypy.expose
	def about(self):
		tmpl = env.get_template('about.html')
		params = {}
		params['aboutSelected'] = "class='selected'"
		if cherrypy.session.get('itemsInCart') == None:
			params['amountInCart'] = 0
		else:
			params['amountInCart'] = (cherrypy.session['itemsInCart'])['amountInCart']
		return tmpl.render(params)

	@cherrypy.expose
	def contact(self, message=""):
		tmpl = env.get_template('contact.html')
		params = {}
		params['contactSelected'] = "class='selected'"
		params['commentSubmittedMessage'] = message
		if cherrypy.session.get('itemsInCart') == None:
			params['amountInCart'] = 0
		else:
			params['amountInCart'] = (cherrypy.session['itemsInCart'])['amountInCart']
		return tmpl.render(params)

	@cherrypy.expose
	def checkout(self, stripeToken="", stripeEmail="", stripeTokenType=""):
		tmpl = env.get_template('checkout.html')
		params = {}
		params['checkoutSelected'] = "class='selected'"
		if cherrypy.session.get('cart') == None:
			params['shoppingCartItems'] = "Empty Cart"
		else:
			params['shoppingCartItems'] = cherrypy.session['cart']
		if cherrypy.session.get('itemsInCart') == None:
			params['amountInCart'] = 0
		else:
			params['amountInCart'] = (cherrypy.session['itemsInCart'])['amountInCart']
		return tmpl.render(params)

	@cherrypy.expose
	def sendComment(self,name="",email="",subject="",message=""):
		if name != "Name" and email != "Email" and subject != "Subject":
			subject = "Comment from " + email + ": " + subject
			os.system("""echo '%s' | mail -s '%s' '%s'"""%(message, subject, commentEmail))

			raise cherrypy.HTTPRedirect("""/contact?message='Your comments have been sent!'""")
		else:
			raise cherrypy.HTTPRedirect("""/contact""")

	@cherrypy.expose
	def addToCart(self, itemId=""):
		if itemId == "":
			return "No item specified"
		elif(cherrypy.session.get('cart') == None):
			cherrypy.session['cart'] = {itemId : 1}
			cherrypy.session['itemsInCart'] = {'amountInCart' : 1}
			return "Cart created"
		else:
			if itemId in cherrypy.session['cart']:
				(cherrypy.session['cart'])[itemId] = (cherrypy.session['cart'])[itemId] + 1
			else:
				(cherrypy.session['cart'])[itemId] = 1
			(cherrypy.session['itemsInCart'])['amountInCart'] = (cherrypy.session['itemsInCart'])['amountInCart'] + 1
			return "Added to cart"

	@cherrypy.expose
	def placeOrder(self):
		# Get cart here
		# Fill message with cart contenets and name, email, and address of user
		# should submit when stripe form is submitted
		message = ""
		# Probably add user email
		subject = "Order from"
		os.system("""echo '%s' | mail -s '%s' '%s'"""%(message, subject, ordersEmail))
		return "Order placed"


if __name__ == '__main__':
	conf = {
		'global': {
		'server.max_request_body_size': 0
		},
		'/': {
			'tools.sessions.on' : True,
			'tools.sessions.timeout' : 120,
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


