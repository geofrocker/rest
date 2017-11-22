# Yummy-Recipes Restful API
[![Build Status](https://travis-ci.org/geofrocker/rest.svg?branch=master)](https://travis-ci.org/geofrocker/rest)
[![Coverage Status](https://coveralls.io/repos/github/geofrocker/rest/badge.svg?branch=master)](https://coveralls.io/github/geofrocker/rest?branch=master)
[![Requirements Status](https://requires.io/github/geofrocker/rest/requirements.svg?branch=master)](https://requires.io/github/geofrocker/rest/requirements/?branch=master)
# Description
Yummy recipies API is an api built using restframework
  * A user can see the available recipes
  * A user can register for membership
  * A user can login using his/her credentials
  * A user can add, edit and delete recipes
# Installation guide
  * This application has been tested with [Python 3.4](https://www.python.org/) and [Flask 0.11](http://flask.pocoo.org/)
  * Make sure the above requirements are satisfied
  * Navigate to the project root directory and run `pip install -r requirements.txt` from command line. [Learn more a pip](https://pypi.python.org/pypi/pip) if you don't have it already installed
  * Run `python app.py` from command line or terminal
  * You should be able to see something similar to this
  ![A screen shot of flask running in cmd](/github.com/geofrocker/Yummy-Recipes/raw/master/A%20screen%20shot%20of%20flask%20running%20in%20cmd.png)
  * Visit your browser and enter `127.0.0.1/5000`
  * :boom::boom: You will be good to go
# Create a .env file and add the following variables
`DEBUG = True`
`DATABASE_URL = 'postgresql://localhost/rest_api'`
`TEST_DB = 'postgresql://localhost/ApiTests'`
`SQLALCHEMY_TRACK_MODIFICATIONS = False`
`SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'`

# How run test
  * Make sure all the requirements are installed by running `pip install -r requirements.txt`
  * Make sure you are in the projects root directory
  * Open your terminal and run `py.test test.py`
  * Or `PYTHON_PATH=. pytest test/tests.py -r Pf --cov=.`
  * To install nose use:`sudo pip install nose`
  * Then just use:`nosetests --with -coverage`

  *
  * You will be good to go :boom::boom:

# For Testing purposes
  * I recommend that you install Postman from [here](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en)
  * This will help you to test the api efficiently. click [here](https://www.getpostman.com/postman) to get started

EndPoint | Functionality
------------ | -------------
POST /auth/login | Logs a user in and generates a unique token
POST /auth/register | Register a user
POST /  | Create a new recipe
GET / | Get all the public recipes
GET /<recipe_id> | Get single recipe
PUT /<recipe_id> | Update a specific recipe
DELETE /<recipe_id> | Delete a specific recipe
GET /users | Get all users
GET /users/<user_id> | Get user by id
DELETE /users/<user_id> | Delete a user by id
