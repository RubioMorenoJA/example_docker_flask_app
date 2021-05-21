from flask import Blueprint
from flask_restplus import Api
from blueprints.documented_endpoints.doc_flask_restplus.doc_api_v1 import namespace as ns_api_v1


blueprint = Blueprint('documented_api', __name__, url_prefix='/api/v1/documented_api')


api_extension = Api(
    blueprint,
    title='Flask App API',
    version='1.0',
    description='Flask App API documentation for using externally',
    doc='/doc'
)

api_extension.add_namespace(ns_api_v1)
