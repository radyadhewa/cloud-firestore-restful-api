import datetime
from flask import Blueprint,request,jsonify
from firebase_admin import firestore

db = firestore.client()
stadium_Ref = db.collection('Stadium')
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

stadiumAPI = Blueprint('stadiumAPI', __name__)

@stadiumAPI.route('/')
def root():
    return '''API database stadium yang berisikan data
  1. id_stadium \n
  2. stadium \n
  3. country \n
  '''

# ENDPOINT-1 retrieve all stadium data
@stadiumAPI.route('/retrieve', methods =['GET'])
def read():
    try:
      stadium_id = request.args.get('id')
      if stadium_id:
        stadium = stadium_Ref.document(id).get()
        return jsonify(stadium.to_dict()), 200
      else:
        all_stadium = [doc.to_dict() for doc in stadium_Ref.stream()]
        return jsonify({"access_time":current_datetime, "data":all_stadium}), 200
    except Exception as e:
      return f"An error occured: {e}", 404