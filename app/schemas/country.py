# # app/schemas/country.py
from pydantic import BaseModel
from typing import Optional, List, Dict

class CountryBase(BaseModel):
    name_common: str
    name_official: str
    cca2: str
    cca3: str

class CountryCreate(CountryBase):
    cca3: Optional[str] = None
    independent: Optional[bool] = None
    un_member: bool = False
    region: Optional[str] = "" 
    subregion: Optional[str] = None
    area: Optional[float] = None
    population: int
    flag_url: Optional[str] = None
    capital: Optional[str] = None
    timezones: Optional[List[str]] = ["UTC"]
    languages: Optional[Dict[str, str]] = {"eng": "English"}

class Country(CountryBase):
    id: int
    independent: Optional[bool]
    un_member: Optional[bool]
    region: str
    subregion: Optional[str]
    area: Optional[float]
    population: int
    flag_url: Optional[str]
    capital: Optional[str]
    timezones: Optional[List[str]] = ["UTC"]
    languages: Optional[Dict[str, str]] 

    class Config:
        from_attributes = True

class CountryUpdate(BaseModel):
    name_common: Optional[str] = None
    name_official: Optional[str] = None
    independent: Optional[bool] = None
    un_member: Optional[bool] = None
    region: Optional[str] = None
    subregion: Optional[str] = None
    area: Optional[float] = None
    population: Optional[int] = None
    flag_url: Optional[str] = None
    capital: Optional[str] = None
    timezones: Optional[List[str]] = None
    languages: Optional[dict] = None

