import os
import json
import firebase_admin

from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

firebase_creds = os.getenv("FIREBASE_CREDENTIALS")

cred_dict = json.loads(firebase_creds)
cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred)

db = firestore.client()
