from flask import Flask, request, json, jsonify
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

from movie_manager import MovieManager

database_path = "data/database.db"
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
CORS(app)

# app.config["JWT_SECRET_KEY"] = "secret"

api.add_resource(MovieManager, "/movies",
                 resource_class_args=[database_path])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7777)
