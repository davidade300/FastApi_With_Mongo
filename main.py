"""
This is the main file for the lesson
"""
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from mongo_string import MONGODB_URI

client = AsyncIOMotorClient(MONGODB_URI)
app = FastAPI()


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
