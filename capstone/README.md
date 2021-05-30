# Intro

The Casting Agency API supports the agency by allowing users to query the database for movies and actors. There are three different user roles (and related permissions), which are:
- Casting assistant: Can view actors and movies.
- Casting director: Can view, add, modify, or delete actors; can view and modify movies.
- Executive producer: Can view, add, modify, or delete actors and movies. 

## Motivations & Covered Topics

This is the last project of the Udacity-Full-Stack-Nanodegree Course. It is a fictitional backend api for a casting agency who needs to keep track of movies and actors.  As stated above there are three levels of authorization with different permissions for each level.  

This project covers following technical topics in this final project:
1. Database modeling with `postgres` & `sqlalchemy` (see `models.py`)
2. API to performance CRUD Operations on database with `Flask` (see `app.py`)
3. Automated testing with `Unittest` (see `test_app`)
4. Authorization & Role based Authentification with `Auth0` (see `auth.py`)
5. Deployment on `Heroku`

## Getting Started

### Technologies
- Python 3.9
- Postgres
- Flask and sqlalchemy
- Unittest
- Auth0
- Heroku

### Technology Stack

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is used to handle the requests and responses from the backend server.

- [SQLAlchemy](https://www.sqlalchemy.org/) is a Python SQL toolkit. The ORM allows for the database modeling to be abstracted away allowing the developer to focus on building the objects (models).

- [Postgres](https://www.postgresql.org) was the chosen database technology for this project becuase of its ease of use and relational structure.

- [Auth0](https://auth0.com) was chosen for the authorization and authentication of the api.  It allows for these processes to be handled by a third party and even allows authentication from other services, i.e. Github, Google, etc. This takes the complexities of user management out of the hands of the developer.

### Installing Dependencies

#### Python 3.9

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Postrgres
Make sure you have postgres installed locally if you wish to test the code locally.

#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).  I used the venv process for this project.
```
python3 -m venv <name of your environment>
```

#### Project Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

#### Heroku
1. The api can be pushed to heroku to host and run live.  In order to complete this you will need the heroku cli.
```
brew tap heroku/brew && brew install heroku
```
Additional instructions can be found here:  https://devcenter.heroku.com/categories/command-line.
2. Once the heroku CLI is installed follow these steps to setup your app:
```
heroku create <name_of_your_app>
```
3. Once the app is created you will get a git url and a url to access the app.  Use the git url to hook your repository to heroku.
```
git remote add heroku <heroku_git_url>
```
4. Add a postgres database to the project in heroku.
```
heroku addons:create heroku-postgresql:hobby-dev --app <name_of_your_application>
```
5. Then push your code to heroku
```
git push heroku master
```
6. Run database migrations on heroku and models/tables will be built in the background.
```
heroku run python manage.py db upgrade --app <name_of_your_application>
```

#### Setting up the environment 
Run the code below to setup the environemental variables.
```
source setup.sh
```
Then identifiy the entry script for flask.
```
export FLASK_APP=app.py 
export FLASK_ENV=development # enables debug mode  
```

#### Running the development server
You can run the development server by running:
```
python app.py
```
OR
```
flask run --reload
```

# Running the API

API endpoints can be accessed via  https://borbertcastingagency.herokuapp.com/

Auth0 information for endpoints that require authentication can be found in `setup.sh`.  Tokens provided should allow testing of the API endpoints.

# Running tests

To run the unittests, first CD into the FSND-Capstone folder (testing locally) and run the following command:
```
python test_app.py
```

If running tests against the heroku deployment use the provided postman collection. 
```
capstone testing collection.postman_collection.json
```

# API Documentation

Errors
`401`
`403`
`404`
`422`

Note: all error handlers return a JSON object with the request status and error message.

401
- 401 error handler is returned when there is an issue with the authentication necessary for the action being requested. 
```
{
	"error": 401,
	"message": "Authentication error.",
	"success": false
}
```
403
- 403 error handler occurs when the requested action is not allowed, i.e. incorrect permissions.
```
{
	"error": 403,
	"message": "Forbidden.",
	"success": false
}
```
404
- 404 error handler occurs when a request resource cannot be found in the database, i.e. an actor with a nonexistent ID is requested.
```
{
	"error": 404,
	"message": "Item not found.",
	"success": false
}
```
422
- 422 error handler is returned when the request contains invalid arguments, i.e. a difficulty level that does not exist.
```
{
	"error": 422,
	"message": "Request could not be processed.",
	"success": false
}
```

Endpoints
`GET '/actors'`
`GET '/movies'`
`POST '/actors'`
`POST '/movies'`
`PATCH '/actors/<int:actor_id>'`
`PATCH '/movies/<int:movie_id>'`
`DELETE '/actors/<int:actor_id>'`
`DELETE '/movies/<int:movie_id>'`

GET '/actors'
- Fetches a JSON object with a list of actors in the database.
- Request Arguments: None
- Returns: A list of actors, that contains multiple objects with a series of string key pairs.
```
{
    "actors": [
        {
            "age": "45",
            "gender": "male",
            "id": 1,
            "name": "Leonardo DiCaprio"
        },
        {
            "age": "37",
            "gender": "female",
            "id": 4,
            "name": "Anne Hathaway"
        }
    ],
    "success": true
}
```
GET '/movies'
- Fetches a JSON object with a list of movies in the database.
- Request Arguments: None
- Returns: A list of movies, that contains multiple objects with a series of string key pairs.
```
{
    "movies": [
        {
            "id": 1,
            "release_year": "December 19, 1997",
            "title": "Titatic"
        },
        {
            "id": 3,
            "release_year": "January 16, 2009",
            "title": "My Bloody Valentine"
        }
    ],
    "success": true
}
```
POST '/actor'
- Posts a new actor to the database, including the name, age, gender, and actor ID, which is automatically assigned upon insertion.
- Request Arguments: Requires three string arguments: name, age, gender.
- Returns: An actor object with the date of birth, gender, and name.

```
{
    {
    "name":"BillyBob",
    "full_name":"George W",
    "date_of_birth":"09-29-1975",
    "gender":"M"
    },
    "success": true
}
```
POST '/movie'
- Posts a new movie to the database, including the title, release, and movie ID, which is automatically assigned upon insertion.
- Request Arguments: Requires two string arguments: title, release.
- Returns: A movie object with the duration, imdb_rating, release_year, and title.

```
{
    {
    "title": "Full Metal Freedom",
    "release_year": 1978,
    "duration": 120,
    "imdb_rating": 8.7
    },
    "success": true
}
```
PATCH '/actors/<int:actor_id>'
- Patches an existing actor in the database.
- Request arguments: Actor ID, included as a parameter following a forward slash (/), and the key to be updated passed into the body as a JSON object. For example, to update the age for '/actors/1'
```
{
	"gender": "Other"
}
```
- Returns: An actor object with the full body of the specified actor ID.
```
{
    {
    "name":"BillyBob",
    "full_name":"George W",
    "date_of_birth":"09-29-1975",
    "gender":"M"
    },
    "success": true
}
```
PATCH '/movies/<int:movie_id>'
- Patches an existing movie in the database.
- Request arguments: Movie ID, included as a parameter following a forward slash (/), and the key to be updated, passed into the body as a JSON object. For example, to update the age for '/movies/5'
```
{
    "duration": 122
}
```
- Returns: A movie object with the full body of the specified movie ID.
```
{
    {
        "id": 5,
        "release_year": 1999,
        "title": "Thor",
        "duration": 122
    },
    "success": true
}
```
DELETE '/actors/<int:actor_id>'
- Deletes an actor in the database via the DELETE method and using the actor id.
- Request argument: Actor id, included as a parameter following a forward slash (/).
- Returns: ID for the deleted question and status code of the request.
```
{
    "success": True,
    "deleted_actor_id": actor.id
}
```
DELETE '/movies/<int:movie_id>'
- Deletes a movie in the database via the DELETE method and using the movie id.
- Request argument: Movie id, included as a parameter following a forward slash (/).
- Returns: ID for the deleted question and status code of the request.
```
{
    "success": True,
    "deleted_movie_id": movie.id
}
```
