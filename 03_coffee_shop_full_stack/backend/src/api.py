import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
Uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# CORS Headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

## ROUTES
'''
GET /drinks endpoint
    This is a public endpoint that represnets the drink model with the short() description method.
    This returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the
    list of drinks.

Returns:
    Status code 200 and list of drinks.

'''
@app.route('/drinks')
def get_drinks():
    drinks=Drink.query.all()

    formatted_drinks = [drink.short() for drink in drinks]

    # print('Formatted drinks: {}'.format(formatted_drinks))

    return jsonify({
        'success': True,
        'drinks':formatted_drinks
    }), 200


'''
GET /drinks-detail endpoint
    This is an endpoint that requires the 'get:drinks-detail' permission.  Once the action is authorized
    the method with retrieve a list of drinks, in their long description format, from the database.
Requires:
    'get:drinks-detail' permission
Returns:
    Status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks.
Known errors:
    401 Unauthorized if user lacks permission
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinks=Drink.query.all()

    formatted_drinks = [drink.long() for drink in drinks]

    return jsonify({
        'success':True,
        'drinks':formatted_drinks
    }), 200


'''
POST /drinks endpoint
    This endpoint creates a new drink in the drink table with appropriate permissions.
Requires:
    The 'post:drinks' permission.
Returns:
    Status code 200 and json {"success": True, "drinks": drink} where drink an array containing 
    only the newly created drink in the long description format.
Known errors:
    401 Unauthorized if user lacks permission to add drinks.
    422 status code:  title and recipe are not in the new recipe or payload used to create the new
    recipe.
'''
@app.route('/drinks',methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    print(payload)
    body=request.get_json(payload)

    if 'title' and 'recipe' not in body:
        abort(422)

    try:
        title=body['title']
        recipe=body['recipe']

        # if type(recipe)!=list:
        #     recipe=[recipe]

        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()

        return jsonify({
            'success':True,
            'drinks':[drink.long()]
        }), 200

    except Exception as e:
        print(e)
        abort(422)

'''
PATCH /drinks/<id> endpoint
    This endpoint attempts to update an exisiting drink in the drink table.  Success indicates the
    record was updated in the drinks table.
Requires: 
    Drink_id <id> that is passed in the url. Also the <id> of the drinks model.
Returns:
    Status code 200 and json {"success": True, "drinks": drink} where drink an array
    containing only the updated drink.
Known errors:
    401 Unauthorized if user lacks permission to update/edit drinks.
    404 status code if drink_id is not given.
'''
@app.route('/drinks/<int:drink_id>', methods=["PATCH"])
@requires_auth('patch:drinks')
def update_drink(payload,drink_id):
    body = request.get_json(payload)
    new_title = body.get('title', None)
    new_recipe = body.get('recipe', None)

    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if not drink:
            abort(404)

        drink.title = new_title
        drink.recipe = json.dumps(new_recipe)

        # if type(recipe)!=list:
        #     recipe=[recipe]

        drink.update()

        return jsonify({
            'success':True,
            'drinks':[drink.long()]
        }), 200

    except Exception as e:
        print(e)
        abort(422)

'''
DELETE /drinks/<id> endpoint
    Attempts to delete a drink from the drinks table.  Success indicates the delete was successful.
Requires: 
    Drink_id <id> that is passed in the url. Also the <id> of the drinks model.
Returns:
    Status code 200 and json {"success": True, "delete": id} where the id is the drink <id> of the 
    deleted drink. 
Known errors:
    401 Unauthorized if user lacks permission to delete drinks.
    404 status code if drink_id is not given.
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload,drink_id):
    drink=Drink.query.filter(Drink.id==drink_id).one_or_none()

    if not drink:
        abort(404)
    
    try:
        drink.delete()

        return jsonify({
            'success':True,
            'delete': drink.id
        }), 200
    except Exception as e:
        print(e)
        abort(422)


'''
Error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
    }), 422

'''
Error handler for 404
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
    }), 404

'''
Error handler for AuthError
'''
@app.errorhandler(AuthError)
def not_authenticated(auth_error):
    return jsonify({
        "success": False,
        "error": auth_error.status_code,
        "message": auth_error.error
    }), 401