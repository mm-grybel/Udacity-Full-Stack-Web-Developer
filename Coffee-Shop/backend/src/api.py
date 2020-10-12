import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth


def validate_recipe(recipe):
    recipes = []

    if not isinstance(recipe, list) and not isinstance(recipe, dict):
        return None

    if isinstance(recipe, dict):
        try:
            name = recipe['name']
            parts = recipe['parts']
            color = recipe['color']

            if not isinstance(name, str):
                return None

            if not isinstance(parts, (str, int, float)):
                return None

            if not isinstance(color, str):
                return None

            recipes = [{
                'name': name,
                'parts': int(parts),
                'color': color
            }]

        except Exception as e:
            print(e)
            return None

    else:
        for i in recipe:
            name = recipe['name']
            parts = recipe['parts']
            color = recipe['color']

            if not isinstance(name, str):
                return None

            if not isinstance(parts, (str, int, float)):
                return None

            if not isinstance(color, str):
                return None

            recipes.append({'name': name, 'parts': int(parts), 'color': color})

    return recipes


app = Flask(__name__)
setup_db(app)
CORS(app)


'''
uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# ROUTES

'''
GET /drinks
    it is a public endpoint
    it contains only the drink.short() data representation
returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks or appropriate status code
    indicating reason for failure
'''
@app.route('/drinks')
def retrieve_drinks():
    drinks = Drink.query.order_by(Drink.id).all()
    drinks = [drink.short() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': drinks
    })


'''
GET /drinks-detail
    it requires the 'get:drinks-detail' permission
    it contains the drink.long() data representation
returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks or appropriate status code
    indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def retrieve_drink_details(payload):
    drinks = Drink.query.order_by(Drink.id).all()
    drinks = [drink.long() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': drinks
    })


'''
POST /drinks
    it creates a new row in the drinks table
    it requires the 'post:drinks' permission
    it contains the drink.long() data representation
returns status code 200 and json {"success": True, "drinks": drink}
    where drink is an array containing only the newly created drink
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    body = request.get_json()
    title = body.get('title', None)
    recipe = body.get('recipe', None)

    if recipe is None or title is None:
        abort(422)

    drink_recipe = validate_recipe(recipe)

    if drink_recipe is None:
        abort(422)

    try:
        new_drink = Drink(title=title, recipe=json.dumps(drink_recipe))
        new_drink.insert()

        return jsonify({
            'success': True,
            'drinks': [new_drink.long()]
        })

    except Exception as e:
        print(e)
        abort(422)


'''
PATCH /drinks/<id>
    where <id> is the existing model id
    it responds with a 404 error if <id> is not found
    it updates the corresponding row for <id>
    it requires the 'patch:drinks' permission
    it contains the drink.long() data representation
returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the updated drink
    or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    body = request.get_json()
    drink = Drink.query.get(id)

    if drink is None:
        abort(404)

    try:
        title = body.get('title')
        recipe = body.get('recipe')

        if title is not None:
            drink.title = title

        if recipe is not None:
            drink_recipe = validate_recipe(recipe)
            if drink_recipe is not None:
                drink.recipe = json.dumps(drink_recipe)

        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })

    except Exception as e:
        print(e)
        abort(400)


'''
DELETE /drinks/<id>
    where <id> is the existing model id
    it responds with a 404 error if <id> is not found
    it deletes the corresponding row for <id>
    it requires the 'delete:drinks' permission
returns status code 200 and json {"success": True, "delete": id} where id
    is the id of the deleted record or appropriate status code
    indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()

        if drink is None:
            abort(404)

        drink.delete()

        return jsonify({
            'status': True,
            'delete': id
        })
    except Exception as e:
        print(e)
        abort(422)


# Error Handling

'''
Error handlers for all expected errors including 404 and 422
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@app.errorhandler(422)
def unprocessable_request(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable request'
    }), 422


'''
Error handler for AuthError
'''
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error
    }), error.status_code
