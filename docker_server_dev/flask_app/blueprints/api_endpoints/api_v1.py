"""
Users have to set headers with {Content-type: application/json} in order to work. A json is expected to get data.
"""
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from DDBB.database import User


blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')


@blueprint.route('/users', methods=['GET', 'POST'])
@swag_from('/usr/src/app/swagger/users_doc_v1.yaml')
def users():
    db_user = User()
    if request.method == 'GET':
        response_body, response_code = db_user.get_users()
    elif request.method == 'POST':
        response_body, response_code = db_user.set_user(request.json)
    else:
        response_body = 'Unable to process'
        response_code = 405
    db_user.close()
    return jsonify(response_body), response_code


@blueprint.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user(user_id):
    db_user = User()
    if request.method == 'GET':
        response_body, response_code = db_user.get_users(user_id)
    elif request.method == 'PUT':
        response_body, response_code = db_user.set_user_changes(user_id, request.json)
    elif request.method == 'DELETE':
        response_body, response_code = db_user.delete_user(user_id)
    else:
        response_body = 'Unable to process'
        response_code = 405
    db_user.close()
    return jsonify(response_body), response_code
