from flask import Blueprint, request, jsonify
from flasgger import swag_from
from DDBB.database import User


blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')


@blueprint.route('/users', methods=['GET', 'POST'])
@swag_from('/usr/src/app/swagger/users_doc_v1.yaml')
def users():
    if request.method == 'GET':
        db_user = User()
        users = db_user.get_users()
        db_user.close()
        return jsonify(users), 200
    elif request.method == 'POST':
        db_user = User()
        response, message = db_user.set_user(request.json)
        db_user.close()
        response_code = 201 if response else 400
        return jsonify(message), response_code
