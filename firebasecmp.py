from firebase_admin import credentials
from firebase_admin import db
import firebase_admin
from decrypt import *
from pathlib import Path


#fetch the credentials from the JSON
login = credentials.Certificate(f'{Path.cwd()}/firebase_credentials.json')

#initialize the database
firebase_admin.initialize_app(login, {
    'databaseURL': '' #REPLACE WITH YOUR OWN FIREBASE URL
})


def validate_password(password):
        #splitting the string containing password and username into a list
        nfc_card_data = list(password.split(":"))
        
        try:
            #reading from the database
            ref = db.reference(f'/app/{nfc_card_data[0]}')
            firebase_data = ref.get()
            
            #define variables for storing key,input password and original password fetched from firebase
            input_password = nfc_card_data[1]
            firebase_password = firebase_data['encNFCpass']
            key = firebase_data['aesKey']

            decrypted_firebase_password = decrypt_password(firebase_password, key)
            decrypted_input_password = decrypt_password(input_password, key)
            
            if decrypted_firebase_password == decrypted_input_password:
                return "match"
            else:
                return None
        except:
            return None