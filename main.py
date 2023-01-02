from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "Movie API"
app.version = "0.0.1"

movies = [
    {
        "id": 1,
        "title": "Avatar",
        "oveview": "Cillum exercitation ad irure quis aliquip cillum eu. Do dolore exercitation anim officia et tempor deserunt ut laborum sit magna. Elit officia sit sunt cupidatat aute laborum consequat do occaecat reprehenderit ad quis exercitation ex. Officia velit duis reprehenderit velit minim labore amet minim aliquip mollit nisi dolor ipsum.",
        "year": "2009",
        "rating": 7.8,
        "category": "Action",
    },
    {
        "id": 2,
        "title": "Avatar 2",
        "oveview": "Cillum exercitation ad irure quis aliquip cillum eu. Do dolore exercitation anim officia et tempor deserunt ut laborum sit magna. Elit officia sit sunt cupidatat aute laborum consequat do occaecat reprehenderit ad quis exercitation ex. Officia velit duis reprehenderit velit minim labore amet minim aliquip mollit nisi dolor ipsum.",
        "year": "2022",
        "rating": 8,
        "category": "Action",
    },
]


@app.get("/", tags=["home"])
def message():
    return HTMLResponse("<h1>Hello world!</h1>")


@app.get("/movies", tags=["movies"])
def get_movies():
    return movies


@app.get("/movies/{id}", tags=["movies"])
def get_movie(id: int):
    return list(filter(lambda movie: movie["id"] == id, movies))
