# Land of 1000 Movies
## Description
A Web application allowing users to browse through a data set of Movies. Users can search for movies by title, director, starring actors, and genre. This application also allows users to register and login. Once they have done so they are able to leave reviews on movies and keep a personal watchlist.

## Installation
Installation via requirements.txt

```shell
$ cd CS235A2
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

##Execution


**Running the application**

From the CS235A2 directory, and within the command window running the activated virtual environment (see venve\Scripts\activate above):

````shell
$ flask run
```` 

##Configuration

The CS235A2/.env file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (set to`wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (set to `development`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.

##Testing

Testing requires that the file CS235A2/tests/conftest.py be edited to set the value of `TEST_DATA_PATH`. You should set this to the absolute path of the CS235A2/datafiles directory.

e.g.

`TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'mikem', 'Documents', 'CS235A2', 'datafiles')`

assigns TEST_DATA_PATH with the following value (the use of os.path.join and os.sep ensures use of the correct platform path separator):

`C:\Users\mikem\Documents\CS235A2\datafiles`

You can then run tests from the command window within the virtual environment using:

````shell
$ python -m pytest
```` 
