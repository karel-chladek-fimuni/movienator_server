from yipy.api import Yipy
from math import ceil
import json

def fetch_movies():
    api = Yipy()
    movie_list = api.list(limit=1)
    genres = set()
    page_count = ceil(movie_list["data"]["movie_count"]/50)
    # page_count = 2
    movies = []
    for page in range(1, 1+page_count):
        print(page,"/",page_count," "*10,end="\r")
        movie_list = api.list(limit=50, page=page)
        for m in movie_list["data"]["movies"]:
            movies.append(m)
            if("genres" in m):
                for g in m["genres"]:
                    genres.add(g)
                # print(m["imdb_code"])
    with open("data/movies.json","w") as f:
        json.dump(movies,f)
    with open("data/genres.json","w") as f:
        json.dump(list(genres),f)

# with open("movies.json","r") as f:
#     movies = json.load(f)
#     movies_short = []
#     for i,m in enumerate(movies):
#         print(i,"/",len(movies),end="\r")
#         if("genres" in m):
#             movies_short.append({"id":m["id"], "genres":m["genres"]})
#         else:
#             movies_short.append({"id":m["id"], "genres":[]})
#     with open("movies_short.json","w") as f:
#         json.dump(movies_short,f)
if __name__ == '__main__':
    fetch_movies()
    