# Setup
To set up this project on your own machine, perform these steps.

1. Fork this repository, then clone it. Fork it via the Github website, then clone it with either Github desktop or the command line (if you've got the ssh keys set up)
    $ git clone git@github.com:GirlsCodeMK/libraryapp-hackathon-python-starthere.git

2. Once you have a copy of the repository, open a terminal in that directory
    $ cd /path/to/libraryapp-hackathon-python-starthere/

3. Once there, create and activate a virtual environment for the project    
    $ python3 -m venv gcmk
    $ source gcmk/bin/activate

4. Install the required libraries, such as Django    
    $ pip install -r requirements.txt

5. Check you have the correct version
    $ python -m django --version
    2.1.4
