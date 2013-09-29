py_feedme
=========
If you have problems regarding missing modules.

### Install Django

    $ wget https://www.djangoproject.com/download/1.5.4/tarball/
    $ tar xzvf index.html
    $ cd Django-1.5.4
    $ sudo python setup.py install
    
    OR 
    
    $ pip install django

### Install some python dev stuff (to install psycopg2)

    For Ubuntu:
    $ sudo apt-get install libpq-dev python-dev

### Install psycopg2

    $ wget http://initd.org/psycopg/tarballs/PSYCOPG-2-5/psycopg2-2.5.1.tar.gz
    $ tar xzvf psycopg2-2.5.1.tar.gz
    $ cd psycopg2-2.5.1
    $ sudo python setup.py install
    
    OR
    
    $ pip install psycopg2

### To Run

Run `python manage.py runserver` and navigate to `localhost:8000`.

### Install Feedparser

    $ wget https://feedparser.googlecode.com/files/feedparser-5.1.3.tar.gz
    $ tar xzvf feedparser-5.1.3.tar.gz
    $ cd feedparser-5.1.3.tar.gz
    $ sudo python setup.py install
    
    OR
    
    $ pip install feedparser

If you encounter errors, you might need to install this first (setupTools)

    $ wget http://python-distribute.org/distribute_setup.py
    $ python distribute_setup.py
