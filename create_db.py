from movie_manager import MovieManager
import json

database_path = "data/database.db"
if __name__ == "__main__":
    mm = MovieManager(database_path);
    with open("data/movies.json","r") as f:
        movies = json.load(f)
        movie_count = len(movies)
        for i,m in enumerate(movies):
            print(i,"/",movie_count,end="\r")
            try:
                mm.add_movie(m)
            except Exception as e:
                # print("fail: ",e)
                # input()
                pass
