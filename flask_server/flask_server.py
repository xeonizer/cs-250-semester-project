# imports
from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin


# flask app & Api
app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# for handling searches
class Setup(Resource):
    @cross_origin()
    def get(self):
        return render_template('index.html')

class Search(Resource):
    # @cross_origin
    def get(self, search_query):
        a = []
        a.append({"title": search_query,"path":"dataset/xxx","description":"A movie featuring AL Pacino as Micheal."})
        a.append({"title": search_query,"path":"dataset/xxx","description":"A movie featuring AL Pacino as Micheal."})
        return a



api.add_resource(Setup, '/')
api.add_resource(Search, '/search/<string:search_query>')

if __name__ == '__main__':
    app.run(debug=True)
