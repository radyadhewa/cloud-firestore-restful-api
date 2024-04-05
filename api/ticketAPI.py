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
    return '''Halaman awal API ticket yang berisikan data
  1. id_ticket \n
  2. stadium \n
  3. class \n
  4. home-team \n
  5. away-team \n
  6. price \n
  7. stock'''

# ENDPOINT-1 add new ticket data
@ticketAPI.route('/add', methods=['POST'])
def create():
    try:
      id = uuid.uuid4()
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
            return jsonify({"success": True, "feedback": f"Data with id {id} deleted due to stock reaching 0"}), 201
        else:
            # Update the stock
            ticket_doc_ref.update({**request.json, "time_updated":pd.Timestamp(current_datetime)})
            return jsonify({"success": True, "feedback": f"Data with id {id} updated"}), 201
    except Exception as e:
        return jsonify({"Error": f"An error occurred: {e}"}), 400

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