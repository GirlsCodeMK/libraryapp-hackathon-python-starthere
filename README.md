# Setup
To set up this project on your own machine, perform these steps.

1. Fork this repository, then clone it. Fork it via the Github website, then clone it with either Github desktop or the command line (if you've got the ssh keys set up)
```
$ git clone git@github.com:mygithubusernae/libraryapp-hackathon-python-starthere.git
```
(Use the address of your fork of this repo: you'll need to change `mygithubusername` in the line above.)

2. Once you have a copy of the repository, open a terminal in that directory
```    
$ cd /path/to/libraryapp-hackathon-python-starthere/
```

3. Once there, create and activate a virtual environment for the project    
```    
$ python3 -m venv gcmk
$ source gcmk/bin/activate
```

(If you're on Windows using the `cmd` terminal, the command is
```
$ ./gcmk/Scripts/activate
```
If you're on Windwos using the _Git Bash_ terminal, the command is
```
$ source gcmk/Scripts/activate
```
)

4. Install the required libraries, such as Django    
```    
(gcmk) $ pip install -r requirements.txt
```
5. Check you have the correct version
```    
(gcmk) $ python -m django --version
2.1.5
```
6. Run a migration to create the database
```
(gcmk) $ python manage.py migrate
```
These migrations creates the `Librarian` and `Library user` groups and assigns the correct permissions to them. They also set up the `Configuration` database table with sensible starting values.

## Create users and records

There are two options here: either use the pre-populated sample data, or create users and data yourseelf.

### Using sample data (recommended)

After running `migrate`, pick _one_  of the datasets to include in the database.

1. Sample users
```
(gcmk) $ python manage.py loaddata library-user.json
```
2. Sample users, and sample books & loans
```
(gcmk) $ python manage.py loaddata library-user-library.json
```

Then run the server:
```
(gcmk) $ python manage.py runserver
```

and visit the library site (`127.0.0.1:8000/library`) in a web browser. The admin site is at `127.0.0.1:8000/admin` should you need it.

### Creating users and data by hand (not recommended)
If you elect _not_ to use any of the sample datasets, you'll have to create the users by hand. 

1. Create a superuser
```
(gcmk) $ python manage.py createsuperuser
```
2. Run the server, and open the admin site (`127.0.0.1:8000/admin`) in a web browser
```
(gcmk) $ python manage.py runserver
```
3. In the admin site, create some users, books, copies, and loans. Create at least one librarian and one library-user.

# Use

## Logging
The development system is set up to [log some messages to the console](https://docs.djangoproject.com/en/2.1/topics/logging/) (the same terminal where the messages appear from `runserver`). At the moment, logging is only active for calls in the `views.py` file. 

To log a step of a function, include the line
```
logger.warning('copy delete args: ' + str(self.kwargs))
```
...and the message will appear when the function is used.

Note that the argument to `logger` must be a single `str`ing, so you need to convert non-`str`ing arguments for `logger`.

# Links

The [Django documentation](https://docs.djangoproject.com/en/2.1/) is essential reading, including the [Django "getting started" tutorial](https://docs.djangoproject.com/en/2.1/intro/).

This application is based on the [DjangoGirls tutorial system](https://tutorial.djangogirls.org/en/) and the [Mozilla Development tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Tutorial_local_library_website).
