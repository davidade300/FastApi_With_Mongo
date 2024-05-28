"""
This is the main file for the lesson
"""
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pymongo import ReturnDocument
from mongo_string import MONGODB_URI
from serializer import convert_doc, convert_doc_list

client = AsyncIOMotorClient(MONGODB_URI)
app = FastAPI()

database = client.get_database("sample_mflix")
collection = database.get_collection("movies")


class Movie(BaseModel):
    """
    this class is using the same names as the on the cluster
    """
    title: str
    release_date: str
    genre: str


@app.get("/")
async def root():
    """
    method/function docstring goes here
    """
    collections = await client.list_database_names()
    return {
        "message": "Connected to MongoDB Atlas!",
        "Collections": collections
    }


@app.post("/items/")
async def create_movie(movie: Movie):
    """
    Route to create movies

    Args:
        movie (Movie): class of type Movie

    Returns a json containing the succes message and the movie created
    """
    await collection.insert_one(movie.model_dump())
    return {"message": "item created", "item": movie}


@app.get("/read_movies/")
async def read_movies():
    """
    it returns the first 10 movies

    Returns: a dict with the first 10 movies

    """
    movies = await collection.find().to_list(length=10)
    return {"items": convert_doc_list(movies)}


@app.put("/movies/{title}")
async def update_movie(title: str, movie: Movie):
    """_summary_

    Args:
        genre (str): genre of the movie
        movie (Movie): movie with updated data

    Raises:
        HTTPException: yep, we got error handling now!!!

    Returns: it returns the things that it should return(a JSON !!!!)
    """
    updated_movie = await collection.find_one_and_update(
        {"title": title},
        {"$set": movie.model_dump()},
        return_document=ReturnDocument.AFTER
    )
    if updated_movie:
        return {"message": "Movie updated", "movie": convert_doc(updated_movie)}
    raise HTTPException(status_code=404,
                        detail=f"Movie with title {title} not found!")


@app.delete("/movies/{tile}")
async def delete_movie(title: str):
    """_summary_

    Args:
        title (str): title of the movie

    Raises:
        HTTPException: exception handling is not something new anymore :/

    Returns:
        _type_: message
    """
    result = await collection.delete_one({"title": title})
    if result.deleted_count:
        return {"message": f"Movie with title{title} deleted"}
    raise HTTPException(status_code=404,
                        detail=f"Movie with title {title} not found")
