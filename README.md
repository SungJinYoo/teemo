teemo(group_calendar)
==============

web project group calendar

1. clone repo
2. move to repo's root
3. $./setup.sh
4. $source `which virtualenvwrapper.sh`
5. $workon teemo"
6. $echo CREATE DATABASE teemo DEFAULT CHARACTER SET utf8 | mysql -u $your_username -p
7. $./setup_db.sh
8. $python manage.py runserver

now you can see the teemo service in your browser at locahost:8000

you can login with ID: teemo PW: teemo as a professor teaching course no 22152

you can login with ID: 2008037280 PW: 2008037280 as a student attending course 22152

