# app/db/models/country.py
from sqlalchemy import Column, Integer, String, Float, Boolean, JSON
from app.db.database import Base

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name_common = Column(String(100))
    name_official = Column(String(200))
    cca2 = Column(String(2), unique=True)
    cca3 = Column(String(3), unique=True, nullable=True)
    independent = Column(Boolean, nullable=True)
    un_member = Column(Boolean, default=False)
    region = Column(String(100), nullable=True)
    subregion = Column(String(100), nullable=True)
    area = Column(Float, nullable=True)
    population = Column(Integer, nullable=True)
    flag_url = Column(String, nullable=True)
    capital = Column(String(100), nullable=True)
    timezones = Column(JSON, nullable=True)
    languages = Column(JSON, nullable=True)