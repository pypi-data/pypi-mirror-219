from fastapi import Depends, FastAPI
from pymongo.collection import Collection

from appgallery_spy import crud
from appgallery_spy.models import RecentReviewsRequest, Review

app = FastAPI()


@app.post("/reviews/recent")
async def get_recent_reviews(request: RecentReviewsRequest, db: Collection = Depends(crud.get_db)):
    count = request.count
    review_collection = db["review"]
    return crud.get_recent_reviews(review_collection, count)


@app.post("/reviews/insert")
def insert_reviews(data: list[Review], db: Collection = Depends(crud.get_db)) -> None:
    review_collection = db["review"]
    reviews_as_dict = [review.model_dump() for review in data]
    return crud.insert_data(reviews_as_dict, review_collection)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
