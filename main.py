from typing import Optional, List

from fastapi import FastAPI, Path, Body, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from pydantic import BaseModel
from pydantic import Field

from jwt_manger import create_token


app = FastAPI()
app.title = "Movie API"
app.version = "0.0.1"


class User(BaseModel):
    email: str
    password: str


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


@app.post("/login", tags=["auth"], status_code=200)
def login(user: User = Body(...)) -> dict:
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(
            status_code=200,
            content={
                "message": "Login successful",
                "token": token,
            },
        )
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)


@app.get("/movies/{id}", tags=["movies"], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    retrieved_movies = list(filter(lambda movie: movie["id"] == id, movies))
    return JSONResponse(content=retrieved_movies[0])


@app.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movies_by_category(
    category: str = Query(min_length=5, max_length=15),
    year: int = Query(ge=1900, le=2021),
) -> List[Movie]:
    retrieved_movies = list(
        filter(
            lambda movie: movie["category"] == category and movie["year"] == year,
            movies,
        )
    )

    if len(retrieved_movies) == 0:
        raise HTTPException(status_code=404, detail="Movie not found")

    return JSONResponse(status_code=200, content=retrieved_movies)


@app.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def add_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(
        status_code=201,
        content={
            "message": "Movie added successfully!",
            "movie": movies[-1],
        },
    )


@app.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(
    id: int = Path(ge=0, le=2000),
    updated_movie: Movie = Body(...),
) -> dict:
    global movies
    movies = list(
        map(
            lambda movie: movie if movie["id"] != id else updated_movie,
            movies,
        )
    )

    return JSONResponse(
        status_code=200,
        content={
            "message": "Movie updated successfully!",
            "movie": updated_movie,
        },
    )


@app.delete("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(id: int = Path(ge=0, le=2000)) -> dict:
    global movies
    movies = list(filter(lambda movie: movie["id"] != id, movies))
    return JSONResponse(
        status_code=200,
        content={
            "message": "Movie deleted successfully!",
            "id": id,
        },
    )
