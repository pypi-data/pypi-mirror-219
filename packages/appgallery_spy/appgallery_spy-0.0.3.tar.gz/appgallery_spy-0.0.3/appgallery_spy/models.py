from datetime import datetime

from pydantic import BaseModel


class RecentReviewsRequest(BaseModel):
    count: int


class Review(BaseModel):
    username: str
    date: datetime
    review_text: str
    rating: int
