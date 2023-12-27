from sqlalchemy.orm import Session
import schemas
from db.models import User, School


def create_user(db: Session, schema: schemas.UserCreate):
    db_user = User(**schema.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, category_id: int):
    return db.query(User).filter_by(id=category_id).first()


def update_user(db: Session, category_id: int, category_data: schemas.UserUpdate | dict):
    db_user = db.query(User).filter_by(id=category_id).first()
    category_data = category_data if isinstance(category_data, dict) else category_data.model_dump()
    if db_user:
        for key, value in category_data.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter_by(id=user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


def create_school(db: Session, schema: schemas.SchoolCreate):
    db_school = School(**schema.model_dump())
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school


def get_schools(db: Session):
    return db.query(School).all()


def get_school(db: Session, item_id: int):
    return db.query(School).filter_by(id=item_id).first()


def update_school(db: Session, item_id: int, item_data: schemas.SchoolUpdate | dict):
    db_school = db.query(School).filter_by(id=item_id).first()

    item_data = item_data if isinstance(item_data, dict) else item_data.model_dump()

    if db_school:
        for key, value in item_data.items():
            if hasattr(db_school, key):
                setattr(db_school, key, value)

        db.commit()
        db.refresh(db_school)
        return db_school
    return None


def delete_school(db: Session, item_id: int):
    db_school = db.query(School).filter_by(id=item_id).first()
    if db_school:
        db.delete(db_school)
        db.commit()
        return True
    return False
