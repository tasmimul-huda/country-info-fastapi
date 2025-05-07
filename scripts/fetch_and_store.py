# scripts/fetch_and_store.py
import sys
import requests
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import select

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.db.database import SessionLocal, Base, engine
from app.db.models.country import Country
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.crud.users import create_user

def init_db():
    Base.metadata.create_all(bind=engine)

def fetch_countries():
    response = requests.get('https://restcountries.com/v3.1/all')
    return response.json()

def store_countries(db: Session, countries_data):
    for country_data in countries_data:
        country = Country(
            name_common=country_data.get('name', {}).get('common', ''),
            name_official=country_data.get('name', {}).get('official', ''),
            cca2=country_data.get('cca2', ''),
            cca3=country_data.get('cca3', ''),
            independent=country_data.get('independent', None),
            un_member=country_data.get('unMember', False),
            region=country_data.get('region', ''),
            subregion=country_data.get('subregion', None),
            area=country_data.get('area', None),
            population=country_data.get('population', 0),
            flag_url=country_data.get('flags', {}).get('png', ''),
            capital=country_data.get('capital', [None])[0],
            timezones=country_data.get('timezones', []),
            languages=country_data.get('languages', {})
        )
        db.add(country)
    db.commit()

def create_demo_user_if_needed(db: Session):
    # Check if users table is empty
    if db.scalar(select(User).limit(1)) is None:
        print("No users found in database. Creating a demo user.")
        username = input("Enter username for demo user: ")
        email = input("Enter email for demo user: ")
        password = input("Enter password for demo user: ")
        
        user_data = UserCreate(
            username=username,
            email=email,
            password=password
        )
        user = create_user(db, user_data)
        print(f"Demo user created: {user.username}")
    else:
        print("Users already exist in database. Skipping demo user creation.")

def main():
    # Initialize database first
    init_db()
    
    db = SessionLocal()
    try:
        # Create demo user if needed
        create_demo_user_if_needed(db)
        
        # Fetch and store countries
        countries_data = fetch_countries()
        store_countries(db, countries_data)
        print(f"Successfully stored {len(countries_data)} countries")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()