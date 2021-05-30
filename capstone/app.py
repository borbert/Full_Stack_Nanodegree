import os
import json
from flask import (
  Flask,
  request,
  abort,
  jsonify
  )
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import (
  setup_db,
  db_drop_and_create_all,
  setup_db,
  Actor,
  Movies
  )
from auth import requires_auth, AuthError
# from authlib.integrations.flask_client import OAuth


AUTH0_CALLBACK_URL = os.getenv('AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.getenv(
    'AUTH0_DOMAIN',
     default='fsnd-project3-borbert.us.auth0.com')
AUTH0_BASE_URL = os.getenv('AUTH0_BASE_URL')
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  # db_drop_and_create_all()
  CORS(app)  # ,resources={r"/*": {"origins": "*"}}

  #----------------------------------------------------------------------------#
  # CORS (API configuration)
  #----------------------------------------------------------------------------#
  @app.after_request
  def after_request(response):
    response.headers.add(
    'Access-Control-Allow-Headers',
     'Content-Type, Authorization')
    response.headers.add(
    'Access-Control-Allow-Methods',
     'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  # '''
  # 0auth info
  # '''
  # oauth = OAuth(app)

  # auth0 = oauth.register(
  #   'auth0',
  #   client_id=AUTH0_CLIENT_ID,
  #   client_secret=AUTH0_CLIENT_SECRET,
  #   api_base_url=AUTH0_BASE_URL,
  #   access_token_url='fsnd-project3-borbert.us.auth0.com' + '/oauth/token',
  #   authorize_url='fsnd-project3-borbert.us.auth0.com' + '/authorize',
  #   client_kwargs={
  #       'scope': 'openid profile email'
  #           }
  # )

  '''
  Routes
  '''
  #-------------------Generate a new auth token-----------------#
  @app.route("/authorization", methods=["GET"])
  def generate_auth_url():
    url = f'https://{AUTH0_DOMAIN}/authorize' \
        f'?audience={AUTH0_AUDIENCE}' \
        f'&response_type=token&client_id=' \
        f'{AUTH0_CLIENT_ID}&redirect_uri=' \
        f'{AUTH0_CALLBACK_URL}'
    return jsonify({
        'url': url
    })
  #--------------------------General Routes------------------------#
  '''
  GET / endpoint
      This is a public endpoint that represents the list model with the short() description method.
      This returns status code 200 and json {'health': 'Running!!'}.
  Returns:
      Status code 200 and list of lists.
  '''
  @app.route('/')
  def heath_check():
    return jsonify({"health": "Running!!"}), 200

  #--------------------------Actors Controllers------------------------#
  '''
  GET /actors endpoint
      This is an endpoint that requires the 'get:actors' permission.  Once the action is authorized
      the method with retrieve a list of actors, in their long description format, from the database.
  Requires:
      'get:actors' permission
  Returns:
      Status code 200 and json {"success": True, "actors": actors} where actors is the list of actors.
  Known errors:
      401 Unauthorized if user lacks permission
  '''
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(payload):

    actors_query = Actor.query.order_by(Actor.id).all()
    actors = [actor.short() for actor in actors_query]

    return jsonify({
        "success": True,
        "actors": actors
    }), 200

  '''
  GET /actors/<int:actor_id> endpoint
      This is an endpoint that requires the 'get:actors' permission.  Once the action is authorized
      the method with retrieve an actor, in their long description format, from the database.
  Requires:
      'get:actors' permission
  Returns:
      Status code 200 and json {"success": True, "actor": actor.full_info()} where actor is an actor.
  Known errors:
      401 Unauthorized if user lacks permission
  '''
  @app.route('/actors/<int:actor_id>', methods=['GET'])
  @requires_auth("get:actors")
  def get_actor_by_id(payload, actor_id):
    actor = Actor.query.get_or_404(actor_id)

    return jsonify({
      "success": True,
      "actor": actor.long()
    }), 200

  '''
  POST /actors endpoint
      This is an endpoint that requires the 'post:actors' permission.  Once the action is authorized
      the method insert a new actor in the database.
  Requires:
      'post:actors' permission
  Returns:
      Status code 201 and json {"success": True, "created": new_actor.id}.
  Known errors:
      401 Unauthorized if user lacks permission.
      422 Invalid if name or date of birth missing.
  '''
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor(payload):
    body = request.get_json()
    # print(body)

    if not body:
      abort(400, {'message': 'request does not contain a valid JSON body.'})
    # Extract name and age value from request body
    name = body.get('name', None)
    full_name = body.get('full_name', None)
    date_of_birth = body.get('date_of_birth', None)

    # Set gender to value or to 'Other' if not given
    # gender = body.get('gender', 'Other')
    # print(gender)

    # abort if one of these are missing with appropiate error message
    if not name:
      abort(422, {'message': 'no name provided.'})

    if not date_of_birth:
      abort(422, {'message': 'no date_of_birth provided.'})

    # Create new instance of Actor & insert it.
    new_actor = (Actor(
          name=name,
          full_name=full_name,
          date_of_birth=date_of_birth,
          ))
    new_actor.insert()

    return jsonify({
      'success': True,
      'created': new_actor.id
    }), 201

  '''
  PATCH /actors/<int:actor_id> endpoint
      This is an endpoint that requires the 'patch:actors' permission.  Once the action is authorized
      the method update an existing actor, from the database.
  Requires:
      'patch:actors' permission
  Returns:
      Status code 200 and json {"success": True, "actor": actor.full_info()} where actor is an actor.
  Known errors:
      401 Unauthorized if user lacks permission
      422 Value, type, or keyerror error based upon validation checks
      500 For internal server error
  '''
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth("patch:actors")
  def update_actor(payload, actor_id):
    actor = Actor.query.get_or_404(actor_id)

    try:
      request_body = request.get_json()
      if not bool(request_body):
        raise TypeError

      if "name" in request_body:
        if request_body["name"] == "":
          raise ValueError

        actor.name = request_body["name"]

      if "full_name" in request_body:
        if request_body["full_name"] == "":
          raise ValueError

        actor.full_name = request_body["full_name"]

      if 'date_of_birth' in request_body:
        if request_body["date_of_birth"] == "":
          raise ValueError

        actor.date_of_birth = request_body["date_of_birth"]

      actor.update()

      return jsonify({
        "success": True,
        "actor_info": actor.long()
      }), 200

    except (TypeError, ValueError, KeyError):
      abort(422)

    except Exception:
      print(sys.exc_info())
      abort(500)

  '''
  DELETE /actors/<int:actor_id> endpoint
      This is an endpoint that requires the 'delete:actors' permission.  Once the action is authorized
      the method an actor from the database.
  Requires:
      'delete:actors' permission
  Returns:
      Status code 200 and json {"success": True, "deleted_actor_id": actor.id} where actor.id is the actor.id
      of actor that was deleted.
  Known errors:
      401 Unauthorized if user lacks permission
      500 Internal server error
  '''
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth("delete:actors")
  def delete_actor(payload, actor_id):
    actor = Actor.query.get_or_404(actor_id)

    try:
      actor.delete()

      return jsonify({
          "success": True,
          "deleted_actor_id": actor.id
      }), 200

    except Exception:
      print(sys.exc_info())
      abort(500)

  #--------------------------Movie Controllers-------------------------#
  '''
  GET /movies endpoint
      This is an endpoint that requires the 'get:movies' permission.  Once the action is authorized
      the method with retrieve a list of movies, in their long description format, from the database.
  Requires:
      'get:movies' permission
  Returns:
      Status code 200 and json {"success": True, "movies": movies} where movies is the list of movies.
  Known errors:
      401 Unauthorized if user lacks permission
  '''
  @app.route('/movies', methods=['GET'])
  def get_movies():
    movies_query = Movies.query.order_by(Movies.id).all()
    movies = [movie.short() for movie in movies_query]

    return jsonify({
        "success": True,
        "movies": movies
    }), 200

  '''
  POST /movies endpoint
      This is an endpoint that requires the 'post:movies' permission.  Once the action is authorized
      the method insert a new movies in the database.
  Requires:
      'post:movies' permission
  Returns:
      Status code 201 and json {"success": True, "created": new_movies.id}.
  Known errors:
      400 Not valid JSON body provided.
      401 Unauthorized if user lacks permission.
      422 Invalid if release year or title missing.
  '''
  @app.route('/movies', methods=['POST'])
  @requires_auth("post:movies")
  def create_movie(payload):
    # return 'auth implemented'
    # print(payload)

    body = request.get_json()
    # print(body)

    if not body:
      abort(400, {'message': 'request does not contain a valid JSON body.'})

    # Extract title and release_date value from request body
    title = body.get('title', None)
    release_year = body.get('release_year', None)
    # print(title,release_year)

    # abort if one of these are missing with appropiate error message
    if not title:
      abort(422, {'message': 'no title provided.'})

    if not release_year:
      abort(422, {'message': 'no "release_year" provided.'})

    new_movie = Movies(
      body['title'],
      body['release_year'],
      body['duration'],
      body['imdb_rating']
      )

    new_movie.add()

    return jsonify({
        'success': True,
        'created': new_movie.id
      }), 201

  '''
  GET /movies/<int:movie_id> endpoint
      This is an endpoint that requires the 'get:movies' permission.  Once the action is authorized
      the method with retrieve an movies, in their long description format, from the database.
  Requires:
      'get:movies' permission
  Returns:
      Status code 200 and json {"success": True, "movies": movies.full_info()} where movies is an movies.
  Known errors:
      401 Unauthorized if user lacks permission
  '''
  @app.route('/movies/<int:movie_id>')
  @requires_auth("get:movies")
  def get_movie_by_id(payload, movie_id):
    movie = Movies.query.get_or_404(movie_id)

    return jsonify({
      "success": True,
      "movie": movie.long()
    }), 200

 '''
  PATCH /movies/<int:movie_id> endpoint
      This is an endpoint that requires the 'patch:movies' permission.  Once the action is authorized
      the method update an existing movies, from the database.
  Requires:
      'patch:movies' permission
  Returns:
      Status code 200 and json {"success": True, "movies": movies.full_info()} where movies is an movies.
  Known errors:
      401 Unauthorized if user lacks permission
      422 Value, type, or keyerror error based upon validation checks 
      500 For internal server error
  '''
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth("patch:movies")
  def update_movie(payload, movie_id):
    movie = Movies.query.get_or_404(movie_id)

    try:
      request_body = request.get_json()
      if not bool(request_body):
        raise TypeError

      if "title" in request_body:
        if request_body["title"] == "":
          raise ValueError

        movie.title = request_body["title"]

      if "release_year" in request_body:
        if request_body["release_year"] <= 0:
          raise ValueError

        movie.release_year = request_body["release_year"]

      if "duration" in request_body:
        if request_body["duration"] <= 0:
          raise ValueError

        movie.duration = request_body["duration"]

      if "imdb_rating" in request_body:
          if request_body["imdb_rating"] < 0 \
                  or request_body["imdb_rating"] > 10:
            raise ValueError

          movie.imdb_rating = request_body["imdb_rating"]

      if "cast" in request_body:
        if len(request_body["cast"]) == 0:
          raise ValueError

          actors = Actor.query.filter(
            Actor.name.in_(request_body["cast"])).all()

          if len(request_body["cast"]) == len(actors):
            movie.cast = actors
          else:
            raise ValueError

      movie.update()

      return jsonify({
        "success": True,
        "movie_info": movie.long()
      }), 200

    except (TypeError, ValueError, KeyError):
      abort(422)

    except Exception:
      print(sys.exc_info())
      abort(500)
  
  '''
  DELETE /movies/<int:movie_id> endpoint
      This is an endpoint that requires the 'delete:movies' permission.  Once the action is authorized
      the method an actor from the database.
  Requires:
      'delete:movies' permission
  Returns:
      Status code 200 and json {"success": True, "deleted_movies_id": movies.id} where movies.id is the movies.id 
      of movies that was deleted.
  Known errors:
      401 Unauthorized if user lacks permission
      500 Internal server error
  '''
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth("delete:movies")
  def delete_movie(payload, movie_id):
    movie = Movies.query.get_or_404(movie_id)
    print(movie)
    try:
      movie.delete()

      return jsonify({
        "success": True,
        "deleted_movie_id": movie.id
      }), 200

    except Exception:
      abort(500, {'message':'error while deleting movie'})

  #--------------------------Error Handling------------------------#
  @app.errorhandler(401)
  def not_authorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Authentication error."
    }), 401

  @app.errorhandler(403)
  def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden."
    }), 403

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Item not found."
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Request could not be processed."
    }), 422

  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error['description']
    }), error.status_code

  return app

app = create_app()



#--------------------------App Entry-----------------------------#
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
