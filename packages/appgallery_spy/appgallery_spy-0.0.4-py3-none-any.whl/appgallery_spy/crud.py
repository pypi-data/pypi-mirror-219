import pymongo
from pymongo import MongoClient

from appgallery_spy.models import Review


def get_db():
    client = MongoClient("mongodb://db:27017")
    db = client["AppGallery"]
    return db


def get_recent_reviews(reviews_collection, count: int):
    recent_reviews = reviews_collection.find().sort("date", pymongo.DESCENDING).limit(count)
    reviews = [
        Review(
            username=review["username"], date=review["date"], review_text=review["review_text"], rating=review["rating"]
        )
        for review in recent_reviews
    ]

    return reviews


def insert_data(data: list[dict], reviews_collection=None) -> None:
    if not reviews_collection:
        db = get_db()
        reviews_collection = db["reviews"]
    print("Saving data...")
    reviews_collection.insert_many(data)
    print("Data is saved.")
