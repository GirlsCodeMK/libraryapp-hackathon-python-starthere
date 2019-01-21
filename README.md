# Setup
To set up this project on your own machine, perform these steps.

1. Fork this repository, then clone it. Fork it via the Github website, then clone it with either Github desktop or the command line (if you've got the ssh keys set up)
```
$ git clone git@github.com:GirlsCodeMK/libraryapp-hackathon-python-starthere.git
```
2. Once you have a copy of the repository, open a terminal in that directory
```    
$ cd /path/to/libraryapp-hackathon-python-starthere/
```
3. Once there, create and activate a virtual environment for the project    
```    
$ python3 -m venv gcmk
$ source gcmk/bin/activate
```

(If you're on Windows, the command is
```
$ ./gcmk/Scripts/activate
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

### Creating users and data by hand
1. Create a superuser
```
(gcmk) $ python manage.py createsuperuser
```
2. Run the server, and open the admin site (`127.0.0.1:8000/admin`) in a web browser
```
(gcmk) $ python manage.py runserver
```
3. In the admin site, create some users, books, copies, and loans. Create at least one librarian and one library-user.

# Links

The [Django documentation](https://docs.djangoproject.com/en/2.1/) is essential reading, including the [Django "getting started" tutorial](https://docs.djangoproject.com/en/2.1/intro/).

This application is based on the [DjangoGirls tutorial systemm](https://tutorial.djangogirls.org/en/) and the [Mozilla Development tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Tutorial_local_library_website).
