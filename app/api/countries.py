# app/api/countries.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.countries import (
    get_countries,
    get_country_by_cca2,
    create_country,
    update_country,
    delete_country,
    get_countries_by_region,
    get_countries_by_language,
    search_countries
)
from app.db.database import get_db
from app.schemas.country import Country, CountryCreate, CountryUpdate
# from app.core.security import get_current_user

router = APIRouter()

# 1. List all countries
@router.get("/", response_model=List[Country])
def list_countries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all countries with pagination support.
    """
    return get_countries(db, skip=skip, limit=limit)

# 2. Retrieve details of a specific country
@router.get("/{cca2}", response_model=Country)
def get_country_details(cca2: str, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific country by its 2-letter code (cca2).
    """
    country = get_country_by_cca2(db, cca2=cca2)
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

# 3. Create a new country entry
@router.post("/", response_model=Country)
def add_new_country(country: CountryCreate,db: Session = Depends(get_db)): # ,current_user: str = Depends(get_current_user)
    """
    Create a new country entry (requires authentication).
    """
    return create_country(db, country=country)

# 4. Update an existing country's details
@router.put("/{cca2}", response_model=Country)
def update_country_details(cca2: str,country: CountryUpdate,db: Session = Depends(get_db)): # ,current_user: str = Depends(get_current_user)
    """
    Update details of an existing country (requires authentication).
    """
    db_country = update_country(db, cca2=cca2, country=country)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country

# 5. Delete an existing country
@router.delete("/{cca2}", status_code=204)
def remove_country(cca2: str,db: Session = Depends(get_db)): # ,current_user: str = Depends(get_current_user)
    """
    Delete a country (requires authentication).
    """
    if not delete_country(db, cca2=cca2):
        raise HTTPException(status_code=404, detail="Country not found")
    return {"detail": "Country deleted successfully"}

# 6. List same regional countries of a specific country
@router.get("/{cca2}/region", response_model=List[Country])
def get_same_region_countries(cca2: str, db: Session = Depends(get_db)):
    """
    Get all countries in the same region as the specified country.
    """
    country = get_country_by_cca2(db, cca2=cca2)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return get_countries_by_region(db, region=country.region)

# 7. List countries that speak the same language
@router.get("/language/{language}", response_model=List[Country])
def get_countries_by_language_endpoint(
    language: str,
    db: Session = Depends(get_db)
):
    """
    Get countries by language code or name.
    Examples:
    - /api/v1/countries/language/fra
    - /api/v1/countries/language/French
    """
    countries = get_countries_by_language(db, language)
    if not countries:
        raise HTTPException(
            status_code=404,
            detail=f"No countries found for language '{language}'"
        )
    return countries

# 8. Search for a country by name (partial match)
@router.get("/search/", response_model=List[Country])
def search_countries_by_name(name: str, db: Session = Depends(get_db)):
    """
    Search for countries by name (supports partial matching).
    """
    countries = search_countries(db, name=name)
    if not countries:
        raise HTTPException(
            status_code=404,
            detail=f"No countries found matching '{name}'"
        )
    return countries