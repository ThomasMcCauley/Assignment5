import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import models, schemas

logger = logging.getLogger(__name__)

def create(db: Session, sandwich: schemas.SandwichCreate):
    logger.info("Function create in sandwiches controller called")
    db_sandwich = models.Sandwich(
        sandwich_name=sandwich.sandwich_name,
        price=sandwich.price
    )
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

def read_all(db: Session):
    logger.info("Function read_all in sandwiches controller called")
    return db.query(models.Sandwich).all()

def read_one(db: Session, sandwich_id: int):
    logger.info(f"Function read_one in sandwiches controller called with id {sandwich_id}")
    sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    if sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwich

def update(db: Session, sandwich_id: int, sandwich: schemas.SandwichUpdate):
    logger.info(f"Function update in sandwiches controller called with id {sandwich_id}")
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    if not db_sandwich:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    for key, value in sandwich.dict(exclude_unset=True).items():
        setattr(db_sandwich, key, value)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

def delete(db: Session, sandwich_id: int):
    logger.info(f"Function delete in sandwiches controller called with id {sandwich_id}")
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    if not db_sandwich:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    db.delete(db_sandwich)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
