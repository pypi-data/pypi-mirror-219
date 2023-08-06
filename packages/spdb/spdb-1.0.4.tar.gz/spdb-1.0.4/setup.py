from setuptools import setup

setup(name='spdb',
	  version='1.0.4',
	  description='Sassy Python Databases utils',
	  packages=['spdb'],
	  author_email='mrybs2@gmail.com',
	  zip_safe=False,
	  readme='README.md',
	  install_requires=[
	  	'qrcode',
	  	'pyotp'
	  ])