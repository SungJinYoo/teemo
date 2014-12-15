source `which virtualenvwrapper.sh`
workon teemo

python manage.py migrate
python manage.py loaddata initial_data/*.json
python manage.py update_courses 2014 20
python manage.py add_test_datas
