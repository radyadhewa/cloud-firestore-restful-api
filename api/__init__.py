import firebase_admin
from flask import Flask
from firebase_admin import credentials
from config import SECRET_KEY

# authentication key
cred = credentials.Certificate("api/key.json")
firebase_admin.initialize_app(cred)
app = Flask(__name__)

# create flask app
def create_app():
  app.config['SECRET_KEY'] = SECRET_KEY
  
  @app.route('/')
  def root():
      return '''
    Selamat datang di API Pemesanan ticket sepakbola dunia, silahkan baca dokumentasi pada <a href="https://github.com/radyadhewa/cloud-firestore-restful-api" target="_blank">repository ini</a> untuk mengakses endpoints
    '''
  
  from .ticketAPI import ticketAPI
  from .stadiumAPI import stadiumAPI
  
  app.register_blueprint(ticketAPI, url_prefix='/ticket')
  app.register_blueprint(stadiumAPI, url_prefix='/stadium')
  
  return app