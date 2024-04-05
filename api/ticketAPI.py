import uuid
from flask import Blueprint,request,jsonify
from firebase_admin import firestore

db = firestore.client()
ticket_Ref = db.collection('Tiket')

ticketAPI = Blueprint('ticketAPI', __name__)

@ticketAPI.route('/')
def root():
    return '''Halaman awal API ticket yang berisikan data
  1. id_ticket \n
  2. stadium \n
  3. class \n
  4. home-team \n
  5. away-team \n
  6. price \n
  7. stock'''

@ticketAPI.route('/add', methods=['POST'])
def create():
    try:
      id = uuid.uuid4()
      ticket_Ref.document(id.hex).set(request.json)
      return jsonify({"success": True}), 200
    except Exception as e:
      return f"An error occured: {e}", 400
    
@ticketAPI.route('/retrieve', methods =['GET'])
def read():
    try:
      ticket_id = request.args.get('id')
      if ticket_id:
        ticket = ticket_Ref.document(id).get()
        return jsonify(ticket.to_dict()), 200
      else:
        all_ticket = [doc.to_dict() for doc in ticket_Ref.stream()]
        return jsonify(all_ticket), 200
    except Exception as e:
      return f"An error occured: {e}", 400
    
@ticketAPI.route('/update/<id>', methods=['POST', 'PUT'])
def update(id):
    try:
      data = request.json
      if id is None:
        return jsonify({"Error": "Missing 'id' in the request"}), 400
      
      id = str(id)
      ticket_Ref.document(id).update(request.json)
      return jsonify({"success": True}), 200
    except Exception as e:
      return f"An error occured: {e}", 400