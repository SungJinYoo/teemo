halt_when_fail() {
    if [ $? != 0 ]; then
        echo -e "\033[31m [FAIL] \033[0m"$@ 1>&2;
        exit $?
    fi
}

halt_when_not_exists(){
    if [ $? != 0 ]; then
	echo -e "\033[31m [FAIL] \033[0mPLEASE INSTALL "$1
        exit $?
    fi
}

halt_when_not_exists "pip" `which pip`

pip install virtualenv
pip install virtualenvwrapper

source `which virtualenvwrapper.sh`
halt_when_fail "importing virtualenvwrapper"

rmvirtualenv teemo # ignore failure

mkvirtualenv -p `which python2.7` teemo
halt_when_fail "creating virtualenv"

cd initial_data/wadofstuff-django-serializers-1.1.0
python setup.py install
cd ../../

pip install -r initial_data/requirements.txt
halt_when_fail "installing dependency"

halt_when_not_exists "mysqladmin" `which mysqladmin`

echo -e "\033[32m [SUCCESS] \033[0m Setup done! Follow the remaining steps."
