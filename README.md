# Item Catalog Udacity Project 

##Project requirements:
* Python 2.7

## Overview
It implements a web application that provides a list of items within a variety of categories 
and integrates third-party user registration and authentication.


# To run the application:
Please ensure you have Python, Vagrant and VirtualBox installed.
Install the dependency libraries (Flask, sqlalchemy, requests and oauth2client) by running `pip install -r requirements.txt`
open terminal app
Go to directory oauth by running `cd oauth`
Launch the Vagrant VM from inside the folder with:
`vagrant up`
`vagrant ssh`
`cd /vagrant/`
Load the database by running : `python database_setup.py` 
Run python lotsofmenus.py (Sample items and categories can be added there)
Run `python project.py` to test the app
The item catalog Project can then be accessed at `localhost:5000`.  So Open the web browser and go the the url localhost:5000


####Additional Requirements
A **vidi.json** is need for oath with google, which is to be downloaded from the google developers console. 