#Movienator Search Server

## Api call
GET /movies
```json
{
    "genre_filter":{
        "needed": [
            "Horror"
        ],
        "forbiden": [
            "Action"
        ]

    },
    "rating_filter":{
        "min":3.5,
        "max":5
    },
    "year_filter":{
        "min":0,
        "max":2021
    },
    "language_filter":{
        "possible":[
            "en"
        ]
    }

}
```
##Available Genres
```json
[
    "Sport",
    "Reality-TV",
    "Fantasy",
    "Thriller",
    "Mystery",
    "Action",
    "Documentary",
    "Family",
    "Adventure",
    "Crime",
    "War",
    "Drama",
    "Animation",
    "Game-Show",
    "Comedy",
    "Music",
    "Talk-Show",
    "Western",
    "Horror",
    "Musical",
    "History",
    "Film-Noir",
    "Biography",
    "Sci-Fi",
    "Romance",
    "News"
]
```