from firebase_admin import credentials
from firebase_admin import db
import firebase_admin
from decrypt import *
from datetime import datetime
from pathlib import Path

#fetch the credentials from the JSON
login = credentials.Certificate(f'{Path.cwd()}/firebase_credentials.json')

if not firebase_admin._apps:
    #initialize the database
    firebase_admin.initialize_app(login, {
        'databaseURL': '' #REPLACE WITH YOUR OWN FIREBASE URL
    })

def log(username):
    # Get current date and time 
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    time = now.strftime("%I:%M %p")

    ref = db.reference(f'/raspberry pi/Logs')
    value = ({
        f"{username}" : 
        {
            'Date': f'{date}',
            'Time': f'{time}',
            'User': f'{username}'
        }
    })
    ref.push().set(value)