from typing import Optional

from fastapi import FastAPI, Path, Query
from fastapi.responses import HTMLResponse

# from fastapi import Body

from pydantic import BaseModel
from pydantic import Field


app = FastAPI()
app.title = "Movie API"
app.version = "0.0.1"


class Movie(BaseModel):
    id: int
    title: str = Field(min_length=5, max_length=15)
    overview: Optional[str] = Field(min_length=15, max_length=50)
    year: int = Field(ge=1900, le=2021)
    rating: float = Field(ge=0.0, le=10.0)
    category: str = Field(min_length=3, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Avatar",
                "oveview": "Cillum exercitation ad irure quis aliquip cillum eu. Do dolore exercitation anim officia et tempor deserunt ut laborum sit magna. Elit officia sit sunt cupidatat aute laborum consequat do occaecat reprehenderit ad quis exercitation ex. Officia velit duis reprehenderit velit minim labore amet minim aliquip mollit nisi dolor ipsum.",
                "year": 2009,
                "rating": 7.8,
                "category": "Action",
            },
        }


movies = [
    {
        "id": 1,
        "title": "Avatar",
        "oveview": "Cillum exercitation ad irure quis aliquip cillum eu. Do dolore exercitation anim officia et tempor deserunt ut laborum sit magna. Elit officia sit sunt cupidatat aute laborum consequat do occaecat reprehenderit ad quis exercitation ex. Officia velit duis reprehenderit velit minim labore amet minim aliquip mollit nisi dolor ipsum.",
        "year": 2009,
        "rating": 7.8,
        "category": "Action",
    },
    {
        "id": 2,
        "title": "Avatar 2",
        "oveview": "Cillum exercitation ad irure quis aliquip cillum eu. Do dolore exercitation anim officia et tempor deserunt ut laborum sit magna. Elit officia sit sunt cupidatat aute laborum consequat do occaecat reprehenderit ad quis exercitation ex. Officia velit duis reprehenderit velit minim labore amet minim aliquip mollit nisi dolor ipsum.",
        "year": 2022,
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
def get_movie(id: int = Path(ge=1, le=2000)):
    return list(filter(lambda movie: movie["id"] == id, movies))


@app.get("/movies/", tags=["movies"])
def get_movies_by_category(
    category: str = Query(min_length=5, max_length=15),
    year: int = Query(ge=1900, le=2021),
):
    return list(
        filter(
            lambda movie: movie["category"] == category and movie["year"] == year,
            movies,
        )
    )


@app.post("/movies", tags=["movies"])
def add_movie(movie: Movie):
    movies.append(movie)
    return movies[-1]


@app.put("/movies/{id}", tags=["movies"])
def update_movie(id: int, updated_movie: Movie):
    global movies
    movies = list(
        map(
            lambda movie: movie if movie["id"] != id else updated_movie,
            movies,
        )
    )

    return updated_movie


@app.delete("/movies/{id}", tags=["movies"])
def delete_movie(id: int):
    global movies
    movies = list(filter(lambda movie: movie["id"] != id, movies))
    return {"message": "Movie deleted successfully!"}
