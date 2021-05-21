
swagger_app_conf = {
    'title': 'My API',
    'uiversion': 3,
    "specs_route": "/swagger/",
    'doc_dir': './swagger/'
}

template = {
  "swagger": "2.0",
  "info": {
    "title": "Flask Restful Swagger Demo",
    "description": "A Demo for the Flask-Restful Swagger Demo",
    "version": "0.1.1",
    "contact": {
      "name": "Pope",
      "url": "https://github.com/RubioMorenoJA",
    }
  },
  "host": "localhost:8080",  # overrides localhost:500
  # "basePath": "/api",  # base bash for blueprint registration
  "schemes": [
    "http",
    "https"
  ]
  # "operationId": "getmyData"
}
