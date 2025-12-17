from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.Review import Review
from schemas.review import ReviewCreate, Review as ReviewSchema

router = APIRouter(prefix="/reviews", tags=["reviews"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ReviewSchema)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/", response_model=list[ReviewSchema])
def read_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()
