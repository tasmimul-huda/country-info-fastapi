# app/crud/countries.py
from sqlalchemy.orm import Session
from app.db.models.country import Country
from app.schemas.country import CountryCreate, CountryUpdate
from sqlalchemy import func, or_

def get_country(db: Session, country_id: int):
    return db.query(Country).filter(Country.id == country_id).first()

def get_country_by_cca2(db: Session, cca2: str):
    return db.query(Country).filter(Country.cca2 == cca2).first()

def get_countries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Country).offset(skip).limit(limit).all()

def create_country(db: Session, country: CountryCreate):
    db_country = Country(**country.dict())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

def get_countries_by_region(db: Session, region: str):
    return db.query(Country).filter(Country.region == region).all()

def get_countries_by_language(db: Session, language_code: str):
    if len(language_code) <= 3:
        # Search by key (language code)
        return db.query(Country).filter(
            func.json_extract(Country.languages, f"$.{language_code.lower()}").isnot(None)
        ).all()
    else:
        # Search by value (language name)
        # This creates a pattern like: %"French"% to match the value in JSON
        pattern = f'%"{language_code}"%'
        return db.query(Country).filter(
            Country.languages.like(pattern)
        ).all()

def search_countries(db: Session, name: str):
    return db.query(Country).filter(Country.name_common.ilike(f"%{name}%")).all()


def get_country_stats(db: Session):
    from sqlalchemy import func, distinct
    
    total_countries = db.query(func.count(Country.id)).scalar()
    total_regions = db.query(func.count(distinct(Country.region))).scalar()
    
    total_languages = db.query(func.count(distinct(Country.languages))).scalar()
    
    return {
        "total_countries": total_countries,
        "total_regions": total_regions,
        "total_languages": total_languages
    }

def update_country(db: Session, cca2: str, country: CountryUpdate):
    db_country = get_country_by_cca2(db, cca2=cca2)
    if not db_country:
        return None
    
    update_data = country.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_country, field, value)
    
    db.commit()
    db.refresh(db_country)
    return db_country

def delete_country(db: Session, cca2: str):
    db_country = get_country_by_cca2(db, cca2=cca2)
    if not db_country:
        return False
    
    db.delete(db_country)
    db.commit()
    return True
