Overview

This code used for the SQLAlchemy.

Isolate the environement for the python 
	1 Install the virtualenv for the isolated environoment
		pip install virtualenv
	2 Create the virtual environment in the folder
		virtualenv <name of virtual environment>
		virtualenv venv
	3 Activate the virtual environment
		source venv/bin/activate

Step 1- Packages installation
Flask - Python framework
Flask:	pip install flask

Flask-SQLAlchemy is an extension for Flask that adds support for SQLAlchemy to your application.
SQLAlchemy:	pip install Flask-SQLAlchemy

PyMySQL is an interface for connecting to a MySQL database server from Python.
PyMySQL: pip install pymysql

Resource
Flask Resource - http://flask-sqlalchemy.pocoo.org/2.1/
SQLAlchamy - http://docs.sqlalchemy.org/en/latest/orm/tutorial.html


1. Create the database Table
   Base.metadata.create_all(engine)

2. Retrive Records
   
   Query.all()
   Return the results represented by this query as a list. This results in an execution of the underlying query. Ex- Category.query.all()

   order_by(*criterion) Apply one or more ORDER BY criterion to the query and return the newly resulting query.

   limit(limit) Apply a LIMIT to the query and return the newly resulting query.

   offset(offset) Apply an OFFSET to the query and return the newly resulting query.

   first() Return the first result of this query or None if the result doesn’t contain any rows. This results in an execution of the underlying query. Ex- Category.query.first()
    
   Fiter the record by the properties
   query.filter_by(username='missing').first()
