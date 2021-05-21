from flask import request
from flask_restplus import Namespace, Resource, fields
from http import HTTPStatus


namespace = Namespace('api_v1', 'API v1 endpoints')

users_model = namespace.model(
    'Users',
    {
        'id': fields.Integer(
            readonly=True,
            description='User identifier'
        ),
        'name': fields.String(
            required=True,
            description='User name'
        )
    }
)

users_example = {'id': 1, 'name': 'User name'}


@namespace.route('')
class Users(Resource):
    '''Create, modify and get users'''

    @namespace.response(500, 'Internal Server error')
    @namespace.marshal_with(users_model, code=HTTPStatus.CREATED)
    def get(self):
        '''Get users example information'''
        return users_example

    @namespace.response(400, 'User already exists')
    @namespace.response(500, 'Internal Server error')
    @namespace.expect(users_model)
    def post(self):
        '''Create a new user'''
        if request.json['name'] == 'User name':
            namespace.abort(400, 'User already exists')
        return users_example, 201
