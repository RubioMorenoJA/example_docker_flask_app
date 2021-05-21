from flask import Flask
import config
from flasgger import Swagger
from blueprints.api_endpoints.api_v1 import blueprint as blueprint_v1
from blueprints.jinja_endpoints.hello import blueprint as blueprint_hello
# from blueprints.documented_endpoints import blueprint as blueprint_doc_api_v1
from blueprints.documented_endpoints.doc_flasgger.doc_api_v1 import template, swagger_app_conf


app = Flask(__name__)
app.register_blueprint(blueprint_v1)
app.register_blueprint(blueprint_hello)
# app.register_blueprint(blueprint_doc_api_v1)

app.config['SWAGGER'] = swagger_app_conf

swagger = Swagger(app, template=template)
app.config.from_object(config.Config)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
