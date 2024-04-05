import uuid
import datetime
import pandas as pd
from .stadiumAPI import stadium_Ref
from flask import Blueprint,request,jsonify
from firebase_admin import firestore

db = firestore.client()
ticket_Ref = db.collection('Tiket')
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

ticketAPI = Blueprint('ticketAPI', __name__)

@ticketAPI.route('/')
def root():
    return '''
    <h3>Halaman awal API ticket yang berisikan data:</h3>
    <ul>
      <li>id_ticket</li>
      <li>stadium</li>
      <li>class</li>
      <li>home-team</li>
      <li>away-team</li>
      <li>price</li>
      <li>stock</li>
    </ul>
  '''

# ENDPOINT-1 add new ticket data
@ticketAPI.route('/add', methods=['POST'])
def create():
    try:
      id = uuid.uuid4()
      ticket_Ref.document(id.hex).set({**request.json, "time_created":pd.Timestamp(current_datetime)})
      ticket_Ref.document(id.hex).set({**request.json, "time_created":pd.Timestamp(current_datetime)})
      return jsonify({"success": True, "feedback":"Data added to Tiket database", "time_created":current_datetime}), 201
    except Exception as e:
      return f"An error occured: {e}", 400
    
# ENDPOINT-2 retrieve all ticket data and join country data from stadium database
@ticketAPI.route('/retrieve', methods =['GET'])
def read():
    try:
        ticket_id = request.args.get('id')
        if ticket_id:
            ticket = ticket_Ref.document(ticket_id).get()
            ticket_data = ticket.to_dict()
            
            stadium_name = ticket_data.get('stadium')
            if stadium_name:
                stadium_query = stadium_Ref.where('stadium', '==', stadium_name).limit(1).get()
                if stadium_query:
                    stadium_data = stadium_query[0].to_dict()
                    country = stadium_data.get('country')
                    if country:
                        ticket_data['country'] = country
            return jsonify(ticket_data), 200
        else:
            all_tickets = [doc.to_dict() for doc in ticket_Ref.stream()]
            for ticket_data in all_tickets:
                stadium_name = ticket_data.get('stadium')
                if stadium_name:
                    stadium_query = stadium_Ref.where('stadium', '==', stadium_name).limit(1).get()
                    if stadium_query:
                        stadium_data = stadium_query[0].to_dict()
                        country = stadium_data.get('country')
                        if country:
                            ticket_data['country'] = country
            return jsonify({"access_time": current_datetime, "data": all_tickets}), 200
    except Exception as e:
        return jsonify({"Error": f"An error occurred: {e}"}), 400

# ENDPOINT-3 update a ticket data
@ticketAPI.route('/update/<id>', methods=['POST', 'PUT'])
def update(id):
    try:
        if id is None:
            return jsonify({"Error": "Missing 'id' in the request"}), 400
        
        id = str(id)
        ticket_doc_ref = ticket_Ref.document(id)
        ticket_data = ticket_doc_ref.get().to_dict()
        
        new_stock = request.json.get('stock')
        if new_stock == 0:
            # Delete the document if stock is 0
            ticket_doc_ref.delete()
            return jsonify({"success": True, "updated_time": current_datetime, "feedback": f"Data with id {id} deleted due to stock reaching 0"}), 201
        else:
            # Update the stock
            ticket_doc_ref.update({**request.json, "time_updated":pd.Timestamp(current_datetime)})
            return jsonify({"success": True, "feedback": f"Data with id {id} updated"}), 201
    except Exception as e:
        return jsonify({"Error": f"An error occurred: {e}"}), 400
    
# ENDPOINT-4 delete ticket data
@ticketAPI.route('/deletetiket/<string:document_id>', methods=['DELETE'])
def deletetiket(document_id):
    try:
        document_ref = ticket_Ref.document(document_id)

        if document_ref.get().exists:
            document_ref.delete()
            return jsonify({"success": True, "deleted_time": current_datetime,"message": f"Document {document_id} deleted"}), 200
        else:
            return jsonify({"success": False, "message": f"Document {document_id} not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {e}"}), 500

# ENDPOINT-5 get only club teams data
@ticketAPI.route('/uniqueteams', methods=['GET'])
def get_unique_teams():
    try:
        all_tickets = ticket_Ref.stream()
        unique_teams = set()
        for ticket in all_tickets:
            ticket_data = ticket.to_dict()
            home_team = ticket_data.get('home_team')
            away_team = ticket_data.get('away_team')
            if home_team:
                unique_teams.add(home_team)
            if away_team:
                unique_teams.add(away_team)
        
        return jsonify({"access_time":current_datetime,"teams_list": list(unique_teams)}), 200
    except Exception as e:
        return jsonify({"Error": f"An error occurred: {e}"}), 400

# ENDPOINT-6 join stadium + tiket
@ticketAPI.route('/join', methods=['GET'])
def join():
    tikets = ticket_Ref.get()
    stadiums = stadium_Ref.get()

    joined_data = []
    for Tiket in tikets:
        id_stadium = Tiket.get('stadium')
        stadium = next((stadium for stadium in stadiums if stadium.get('stadium') == id_stadium), None)
        if stadium:
            joined_data.append({
                'Tiket': Tiket.to_dict(),
                'stadium': stadium.to_dict()
            })
    

    return jsonify({"access_time": current_datetime,'data': joined_data})