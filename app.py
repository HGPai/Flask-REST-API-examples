from flask import Flask
from datetime import datetime
from flask_restful import reqparse, Resource, Api

app = Flask(__name__)
api = Api(app=app)


names = {'Hari': {'Unique ID': 12070, 'email': 'hgpai94@gmail.com', 'current user': True},
         'Sam': {'Unique ID': 12125, 'email': 'sam122@gmail.com', 'current user': True},
         'Brad': {'Unique ID': 14052, 'email': 'brad455@gmail.com', 'current user': True}
         }


class Hello(Resource):

    def get(self, name):
        if name in names.keys():
            return names[name]
        else:
            return 'Invalid User! Please try different name.'

    def post(self):
        return {'data': 'Posted'}


api.add_resource(Hello, '/HelloWorld/<string:name>')

if __name__ == '__main__':
    # Use debug=True only in development environment
    app.run(debug=True)
