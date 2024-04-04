import uuid
from config import DB_NAME
from flask import Blueprint,request,jsonify
from firebase_admin import firestore

db = firestore.client()
ticket_Ref = db.collection('Tiket')

ticketAPI = Blueprint('ticketAPI', __name__)

@ticketAPI.route('/add', methods=['POST'])
def create():
    try:
      id = uuid.uuid4()
      ticket_Ref.document(id.hex).set(request.json)
      return jsonify({"success": True}), 200
    except Exception as e:
      return f"An error occured: {e}", 400