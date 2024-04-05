from config import SECRET_KEY
from flask import Flask
from firebase_admin import credentials, initialize_app

cred = credentials.Certificate("api\key.json")
default_app = initialize_app(cred)

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = SECRET_KEY
  
  @app.route('/')
  def root():
      return '''
    Selamat datang di API Pemesanan ticket sepakbola dunia, berikut beberapa cara untuk akses layanan CRUD
    '''
  
  from .ticketAPI import ticketAPI
  from .stadiumAPI import stadiumAPI
  
  app.register_blueprint(ticketAPI, url_prefix='/ticket')
  app.register_blueprint(stadiumAPI, url_prefix='/stadium')
  
  return app