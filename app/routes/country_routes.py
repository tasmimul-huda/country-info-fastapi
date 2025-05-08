from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, Request, Depends, HTTPException, Form

# ================================================
from app.schemas.country import CountryCreate, CountryUpdate
from app.db.database import get_db
from app.db.models.country import Country
from app.crud import users
from app.crud.countries import (get_country,get_countries,get_country_by_cca2,create_country,get_countries_by_region,
                                get_countries_by_language,search_countries,update_country,delete_country
                                )
from app.core.security import verify_password
from app.core.security import get_current_user_session


country_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@country_router.get("/", response_class=HTMLResponse)
async def list_countries(
    request: Request,
    q: str = None,
    region: str = None,
    language: str = None,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user_session)
):
    # Get all distinct regions for dropdown
    all_regions = db.query(Country.region).distinct().all()
    all_regions = [r[0] for r in all_regions if r[0]]  # Flatten and remove None
    
    # Get all unique languages for dropdown
    # This is simplified - you might need a more sophisticated approach
    all_languages = set()
    countries = db.query(Country.languages).all()
    for c in countries:
        if c.languages:
            all_languages.update(c.languages.values())
    all_languages = sorted(all_languages)
    
    # Apply filters
    if q:
        countries = search_countries(db, name=q)
    elif region:
        countries = get_countries_by_region(db, region=region)
    elif language:
        countries = get_countries_by_language(db, language_code=language)
    else:
        countries = get_countries(db)
    
    return templates.TemplateResponse(
        "countries.html",
        {
            "request": request,
            "countries": countries,
            "query": q,
            "all_regions": all_regions,
            "all_languages": all_languages,
            "selected_region": region,
            "selected_language": language,
            "current_user": user
        }
    )



@country_router.get("/countries/{cca2}", response_class=HTMLResponse)
async def country_detail(
    request: Request,
    cca2: str,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user_session)
):
    country = get_country_by_cca2(db, cca2=cca2)
    if not country:
        raise HTTPException(status_code=404)
    
    same_region = get_countries_by_region(db, region=country.region)
    return templates.TemplateResponse(
        "country_detail.html",
        {"request": request, "country": country, "same_region": same_region,
         "current_user": user}
    )


# Add new country routes
@country_router.get("/new_country", response_class=HTMLResponse)
async def show_new_country_form(request: Request, user: str = Depends(get_current_user_session)):
    return templates.TemplateResponse(
        "country_new.html",
        {"request": request,
         "current_user": user}
    )


@country_router.post("/new_country" ,response_class=HTMLResponse)
async def create_country_from_form(
    request: Request,
    name_common: str = Form(...),
    name_official: str = Form(...),
    cca2: str = Form(...),
    capital: str = Form(None),
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user_session)
):
    country_data = {
        "name_common": name_common,
        "name_official": name_official,
        "cca2": cca2,
        "capital": capital,
        # Default values for required fields
        "population": 0,
        "flag_url": f"https://flagcdn.com/{cca2.lower()}.svg" or None
    }
    create_country(db, CountryCreate(**country_data))
    return RedirectResponse("/", status_code=303)

# Edit country routes
@country_router.get("/countries/{cca2}/edit", response_class=HTMLResponse)
async def edit_country_page(request: Request,
                             cca2: str, 
                            db: Session = Depends(get_db),
                            user: str = Depends(get_current_user_session)):
    country = get_country_by_cca2(db, cca2)
    if not country:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("country_edit.html",
                                       {"request": request,
                                        "country": country,
                                        "current_user": user})

@country_router.post("/countries/{cca2}/edit")
async def update_country_web(
    request: Request,
    cca2: str,
    name_common: str = Form(...),
    name_official: str = Form(...),
    capital: str = Form(None),
    population: int = Form(0),
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user_session)
):
    update_data = {
        "name_common": name_common,
        "name_official": name_official,
        "capital": capital,
        "population": population
    }
    update_country(db, cca2, CountryUpdate(**update_data))
    return RedirectResponse(f"/countries/{cca2}", status_code=status.HTTP_303_SEE_OTHER)

# Delete country route
@country_router.post("/countries/{cca2}/delete")
async def delete_country_web(
    request: Request,
    cca2: str,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user_session)
):
    delete_country(db, cca2)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

