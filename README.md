# Setup
To set up this project on your own machine, perform these steps.

1. Fork this repository, then clone it. Fork it via the GitHub website, then clone it with either GitHub desktop or the command line (if you've got the ssh keys set up)
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
If you're on Windows using the _Git Bash_ terminal, the command is
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

There are two options here: either use the pre-populated sample data, or create users and data yourself.

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

# Making changes

Let's say you want to make a change/enhancement/extension to the app.

## Setup
You only need do this once.

Create a new `remote` link, called `upstream`, that points to the original repository. This will allow you to keep up to date with ongoing changes that others have made. (You have to do this on the command line: GitHub desktop doesn't support this.)
```
(gcmk) $ git remote add upstream https://github.com/GirlsCodeMK/libraryapp-hackathon-python-starthere.git
```

## Starting work
Before you start work, ask around to make sure no-one else is working on that feature!

1. Make sure your local copy of your repository is up-to-date by `pull`ing any changes.
```
(gcmk) $ git checkout master
(gcmk) $ git fetch upstream
(gcmk) $ git merge --ff-only upstream/master
```

2. Create and checkout a new branch for your feature. Call the branch anything you want, but you may want to include your name and/or the issue number (if you're addressing [an open issue on the project](https://github.com/GirlsCodeMK/libraryapp-hackathon-python-starthere/issues)).
```
(gcmk) $ git branch cool-feature
(gcmk) $ git checkout cool-feature
```
(You can do both of these steps as one with `git checkout -b cool-feature`)

3. Do some work on this feature. Make commits often, as is good Git practice.

4. Sooner or later (and preferably sooner), you'll want to `push` these commits to your own repository. The _first_ time you do this, you need to tell Git to create a new branch in your remote `origin` repository on GitHub.
```
(gcmk) $ git push --set-upstream origin cool-feature
```

5. As you continue to work, make more commits and push them.
```
(gcmk) $ git push origin cool-feature
```

## Getting your changes accepted
Once you've finished your cool feature, it's time to get it accepted into the main project.

1. Check that the main `master` hasn't changed while you've been working.
```
(gcmk) $ git checkout master
(gcmk) $ git fetch upstream
(gcmk) $ git merge --ff-only upstream/master
```
As you've not changed our local copy of `master`, there should be no conflicts here.

2. Merge the newly-updated `master` into your feature branch
```
(gcmk) % git checkout cool-feature
(gcmk) % git merge master
```
(If you're feeling confident about what you're doing, you can `rebase` your changes instead of `merge`ing them.)

3. Fix any conflicts between your changes and the updates in `master`. Once you're done, commit the changes back to your feature branch. (Git is helpful here in guiding you through the process.)

4. Push your changes back up to your repository
```
(gcmk) $ git push origin cool-feature
```

5. On the GitHub website, find the big green "New pull request" button to ask for your changes to be included into main repository.

6. That's all you need do: someone else will look at your changes and advise you on what happens next. Your changes could be accepted as-is, or the review could suggest some improvements to make to your feature. 


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
