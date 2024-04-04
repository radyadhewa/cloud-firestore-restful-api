from config import SECRET_KEY
from flask import Flask
from firebase_admin import credentials, initialize_app

cred = credentials.Certificate("api\key.json")
default_app = initialize_app(cred)

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = SECRET_KEY
  
  from .ticketAPI import ticketAPI
  
  app.register_blueprint(ticketAPI, url_prefix='/ticket')
  
  return app