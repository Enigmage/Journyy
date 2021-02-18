import requests
from app import app 


def get_google_endpoints():
    return requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()
