teemo(group_calendar)
==============

web project group calendar

Clone project;

IF use OS X
	
	sudo pip install virtualenv
	sudo pip install virtualenvwrapper

Check your virtualenvwapper.sh
	
	which virtualenvwrapper.sh

Add this script on your SHELL( See which virtualenvwrapper.sh)
	
	source /usr/local/bin/vitrualenvwrapper.sh

Make virtualenv

	mkvirtualenv teemo

install mysql

	sudo apt-get install mysqlclient-dev
	
	brew install mysql

Additional package Install

	pip install -r requirements.txt

ADD mysql database,connect your mysql

	create databases teemo default character set "UTF8";

Run server

	python manage.py runserver

IF you have to get permission to manage database
	
	python mamage.py createsuperuser

Add initial_data into your application
	
	python manage.py loaddata initial_data/course_times.json
