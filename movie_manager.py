from database_manager import DatabaseManager
import flask
from flask_restful import Resource
from functools import reduce
from random import shuffle

def get_genre_filter_command(json_data):
    def remove_dash(g):
        return g.replace("-","_").lower()

    def make_select(g,eq=True):
        equality = "==" if eq else "!="
        return f"SELECT movie_id FROM movie_genre where genre {equality} \"{g}\" GROUP BY movie_id"
    # select * from (SELECT DISTINCT movie_id as horror_movie_id FROM movie_genre where genre == "Horror" GROUP BY movie_id) INNER JOIN (SELECT DISTINCT movie_id AS comedy_movie_id FROM movie_genre where genre == "Comedy" GROUP BY movie_id) on horror_movie_id = comedy_movie_id
    command = "select distinct id as genre_movie_id from movies"
    has_where = False
    genre_filter = json_data["genre_filter"]
    if("needed" in genre_filter and len(genre_filter["needed"]) > 0):
        for g in genre_filter["needed"]:
            if not has_where:
                command += " where "
                has_where = True
            else:
                command += " and "
            command += f"id in ({make_select(g,True)})"

    if("forbiden" in genre_filter and len(genre_filter["forbiden"]) > 0):
        for g in genre_filter["forbiden"]:
            if not has_where:
                command += " where "
                has_where = True
            else:
                command += " and "
            command += f"id not in ({make_select(g,True)})"
    return command

def range_filter_command(table,value_name,min,max):
    return f"SELECT id from {table} where {value_name} >= {min} and {value_name} <= {max}"

def make_language_filter_command(possibilities):
    cmd = "SELECT id FROM movies"
    if len(possibilities)!=0:
        filters = " OR ".join([f"language == \"{g}\"" for g in possibilities])
        cmd += f" where {filters} GROUP BY id"
    return cmd

    
class MovieManager(Resource):
    def __init__(self, database):
        self.database = DatabaseManager(database)

    # def get_by_or(self, json_data):
    #     filters = " OR ".join(
    #         [f"genre == \"{g}\"" for g in json_data["genres"]])
    #     command = f"SELECT movie_id FROM movie_genre where {filters} GROUP BY movie_id"
    #     out = self.database.execute_get(command)
    #     return list(map(lambda x: x[0], out)), 200

    # def get_all_movies(self):
    #     command = f"SELECT movie_id FROM movie_genre"
    #     out = self.database.execute_get(command)
    #     return list(map(lambda x: x[0], out)), 200

    # def get_by_and(self, json_data):
    #     if("genres" not in json_data or len(json_data["genres"])==0):
    #         return self.get_all_movies()
    #     command = get_genre_command(json_data)
    #     out = self.database.execute_get(command)
    #     return list(map(lambda x: x[0], out)), 200

    def _get(self):
        json_data = flask.request.json
        command = f"SELECT id from movies"
        has_where = [False]
        def _prepare(has_where):
            if not has_where[0]:
                has_where[0] = True
                return " where "
            else:
                return " and "
        prepare = lambda : _prepare(has_where)
        filters = []
        if("genre_filter" in json_data):
            genre_cmd = get_genre_filter_command(json_data)
            command += prepare()
            command += f"id in ({genre_cmd})"

        if("rating_filter" in json_data):
            rating_cmd = range_filter_command("movies","rating",json_data["rating_filter"]["min"],json_data["rating_filter"]["max"])
            command += prepare()
            command += f"id in ({rating_cmd})"

        if("year_filter" in json_data):
            year_cmd = range_filter_command("movies","year",json_data["year_filter"]["min"],json_data["year_filter"]["max"])
            command += prepare()
            command += f"id in ({year_cmd})"

        if("language_filter" in json_data):
            language_cmd = make_language_filter_command(json_data["language_filter"]["possible"])
            command += prepare()
            command += f"id in ({language_cmd})"
        
        print(command)
        out = self.database.execute_get(command)
        return list(map(lambda x: x[0], out)), 200
        
    def get(self):
        res,status = self._get()
        if(status == 200):
            shuffle(res)
        return res,status

    def add_movie(self, movie_json):
        movie_id = movie_json["id"]
        names = ("id",
                "title",
                "url",
                "imdb_code",
                "title_long",
                "slug",
                "year",
                "rating",
                "runtime",
                "summary",
                "yt_trailer_code",
                "language",
                "mpa_rating",
                "background_image",
                "background_image_original",
                "small_cover_image",
                "medium_cover_image",
                "large_cover_image",
                "date_uploaded",
                "date_uploaded_unix")
        values = []
        for n in names:
            values.append(movie_json[n])
        self.database.insert("movies", names, tuple(values))

        if("genres" in movie_json):
            for genre in movie_json["genres"]:
                self.database.insert(
                    "movie_genre", ("movie_id", "genre"), (movie_id, genre))
