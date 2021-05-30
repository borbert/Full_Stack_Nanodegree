import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movies, Actor, db_drop_and_create_all
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# tokens for testing
casting_assistant_token = config["bearer_tokens"]['casting_assistant']
casting_director_token = config["bearer_tokens"]['casting_director']
executive_producer_token = config["bearer_tokens"]['executive_producer']

database_name = os.getenv('DATABASE_NAME', default='test_agency_db')
db_user = os.getenv('DB_USER', default='postgres')
db_pass = os.getenv('DB_PASS', default=None)
db_host = os.getenv('DB_HOST', default='localhost')
port = os.getenv('PORT', default=5432)
database_path = os.getenv(
    'DATABASE_URL', default="postgres://{}:{}@{}:{}/{}".format(
        db_user, db_pass, db_host, port, database_name))


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.casting_assistant_token = config["bearer_tokens"]['casting_assistant']
        self.casting_director_token = config["bearer_tokens"]['casting_director']
        self.executive_producer_token = config["bearer_tokens"]['executive_producer']
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.VALID_NEW_ACTOR = {
            "name": "Ana de Armas",
            "full_name": "Ana Celia de Armas Caso",
            "date_of_birth": "April 30, 1988"
        }

        self.INVALID_NEW_ACTOR = {
            "name": "Ana de Armas"
        }

        self.VALID_UPDATE_ACTOR = {
            "full_name": "Anne Hathaway"
        }

        self.INVALID_UPDATE_ACTOR = {}

        self.VALID_NEW_MOVIE = {
            "title": "Suicide Squad",
            "duration": 137,
            "release_year": 2016,
            "imdb_rating": 6
        }

        self.INVALID_NEW_MOVIE = {
            "title": "Knives Out",
            "imdb_rating": 7.9,
            "cast": ["Ana de Armas"]
        }

        self.VALID_UPDATE_MOVIE = {
            "imdb_rating": 6.5
        }

        self.INVALID_UPDATE_MOVIE = {}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_health(self):
        """Test for GET / (health endpoint)"""
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('health', data)
        self.assertEqual(data['health'], 'Running!!')

    def test_api_call_without_token(self):
        """Failing Test trying to make a call without token"""
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authentication error.")

    def test_get_actors(self):
        """Passing Test for GET /actors"""
        # need to insert an actor record to pass the assertion of len(data)
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        }, json=self.VALID_NEW_ACTOR)
        # get all actors
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.casting_assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('actors', data)
        self.assertTrue(len(data['actors']))

    def test_get_actors_by_id(self):
        """Passing Test for GET /actors/<actor_id>"""
        # need to insert an actor record in order to find it
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        }, json=self.VALID_NEW_ACTOR)
        # find actor by id
        res = self.client().get('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('actor', data)
        self.assertIn('full_name', data['actor'])

    def test_404_get_actors_by_id(self):
        """Failing Test for GET /actors/<actor_id>"""
        # this should fail because the actor is not in the db
        res = self.client().get('/actors/1', headers={
            'Authorization': "Bearer {}".format(casting_director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_create_actor_with_casting_assistant_token(self):
        """Failing Test for POST /actors"""
        # create a new actor with incorrect permissions
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.casting_assistant_token)
        }, json=self.VALID_NEW_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_create_actor(self):
        """Passing Test for POST /actors"""
        # create a new actor with proper credentials
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        }, json=self.VALID_NEW_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])
        self.assertIn('created', data)

    def test_422_create_actor(self):
        """Failing Test for POST /actors"""
        # failing test due to inserting invalid data --testing 422
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        }, json=self.INVALID_NEW_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_update_actor_info(self):
        """Passing Test for PATCH /actors/<actor_id>"""
        # insert a record before updating the record
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        }, json=self.VALID_NEW_ACTOR)
        # patch method on the actor recrod just inserted
        res = self.client().patch('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        }, json=self.VALID_UPDATE_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('actor_info', data)
        self.assertEqual(data["actor_info"]["full_name"],
                         self.VALID_UPDATE_ACTOR["full_name"])

    def test_422_update_actor_info(self):
        """Failing Test for PATCH /actors/<actor_id>"""
        # insert a record before updating the record
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        }, json=self.VALID_NEW_ACTOR)

        res = self.client().patch('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        }, json=self.INVALID_UPDATE_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_delete_actor_with_casting_assistant_token(self):
        """Failing Test for DELETE /actors/<actor_id>"""
        # insert a record before deleting the record
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        }, json=self.VALID_NEW_ACTOR)
        # this should fail -- assistant doesnt have these credentials
        res = self.client().delete('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.casting_assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_delete_actor(self):
        """Passing Test for DELETE /actors/<actor_id>"""
        # insert a record before deleting the record
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        }, json=self.VALID_NEW_ACTOR)
        # this should pass
        res = self.client().delete('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('deleted_actor_id', data)

    def test_404_delete_actor(self):
        """Failing Test for DELETE /actors/<actor_id>"""
        # this actor does not exist in db this should produce a 404 status code
        res = self.client().delete('/actors/100', headers={
            'Authorization': "Bearer {}".format(self.executive_producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_get_movies(self):
        """Passing Test for GET /movies"""
        # insert a movie so there is one to be found -- need executive producer
        # token
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.executive_producer_token)
        }, json=self.VALID_NEW_MOVIE)
        # find all movies with the casting assistant token
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('movies', data)
        self.assertTrue(len(data["movies"]))

    def test_get_movie_by_id(self):
        """Passing Test for GET /movies/<movie_id>"""
        # insert a movie so there is one to be found -- need executive producer
        # token
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.executive_producer_token)
        }, json=self.VALID_NEW_MOVIE)
        # find movie inserted above with id
        res = self.client().get('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.casting_assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('movie', data)
        self.assertIn('imdb_rating', data['movie'])
        self.assertIn('duration', data['movie'])

    def test_404_get_movie_by_id(self):
        """Failing Test for GET /movies/<movie_id>"""
        # movie with id of 100 does not exist
        res = self.client().get('/movies/100', headers={
            'Authorization': "Bearer {}".format(self.casting_assistant_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_create_movie_with_user_token(self):
        """Failing Test for POST /movies"""
        # this functionality requires the executive producer token
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.casting_assistant_token)
        }, json=self.VALID_NEW_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_create_movie(self):
        """Passing Test for POST /movies"""
        # this functionality requires the executive producer token
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.executive_producer_token)
        }, json=self.VALID_NEW_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])
        self.assertIn('created', data)

    def test_422_create_movie(self):
        """Failing Test for POST /movies"""
        # this test should fail becuase the record to insert is invalid
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.executive_producer_token)
        }, json=self.INVALID_NEW_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_update_movie_info(self):
        """Passing Test for PATCH /movies/<movie_id>"""
        # add movie to update -- this functionality requires the executive
        # producer token
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.executive_producer_token)
        }, json=self.VALID_NEW_MOVIE)
        # update with casting director token
        res = self.client().patch('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        }, json=self.VALID_UPDATE_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('movie_info', data)
        self.assertEqual(data["movie_info"]["imdb_rating"],
                         self.VALID_UPDATE_MOVIE["imdb_rating"])

    def test_422_update_movie_info(self):
        """Failing Test for PATCH /movies/<movie_id>"""
        # add movie to update -- this functionality requires the executive
        # producer token
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.executive_producer_token)
        }, json=self.VALID_NEW_MOVIE)

        # this fails because the update is invalid
        res = self.client().patch('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        }, json=self.INVALID_UPDATE_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_delete_movie_with_casting_director_token(self):
        """Failing Test for DELETE /movies/<movie_id>"""
        # this should fail with 401 because the executive producer only has
        # this priviledge
        res = self.client().delete('/movies/3', headers={
            'Authorization': "Bearer {}".format(self.casting_director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_delete_movie(self):
        """Passing Test for DELETE /movies/<movie_id>"""
        # add movie to update -- this functionality requires the executive
        # producer token
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.executive_producer_token)
        }, json=self.VALID_NEW_MOVIE)
        # this also requires the executive director token
        res = self.client().delete('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.executive_producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('deleted_movie_id', data)

    def test_404_delete_movie(self):
        """Passing Test for DELETE /movies/<movie_id>"""
        # this should pass but 404 is what we are looking for
        # this movie does not exist in the db
        res = self.client().delete('/movies/100', headers={
            'Authorization': "Bearer {}".format(self.executive_producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
