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
`localhost:8000/feeds` (Ryan your login page!).
`localhost:8000/feeds/addFeed` (Insert feeds here).
`localhost:8000/feeds/myFeeds` (Shows all our feeds).

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


Hi Guys!! I've took some time to change some settings and organize the folders(Based on Django tutorial style)
The html files are in the folder "templates" and the dependencies like bootstrap and javascrip is in the folder
"static". The directory structure may not be ideal(someone improve on this please) but its working, if you 
have a better please implement it and test it and make sure it works before pushing.

I've also added a new app called "feeds" (its kind of just a folder with models.py,views.py and other stuffs)

After running python manage.py runserver, navigate to 'http://localhost:8000/feeds/' instead 
It should look good(unless your using firefox)

******************************************************************************************************

Added more new stuff! 
Added a feedTest page (showing latest feed of kotaku, needs to display it cleaner)

Run `python manage.py runserver` and navigate to `localhost:8000/feeds/feedTest` (even more new stuff).



