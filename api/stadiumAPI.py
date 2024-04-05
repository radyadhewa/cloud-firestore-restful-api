import datetime
from flask import Blueprint,request,jsonify
from firebase_admin import firestore

db = firestore.client()
stadium_Ref = db.collection('Stadium')
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

stadiumAPI = Blueprint('stadiumAPI', __name__)

@stadiumAPI.route('/')
def root():
    return '''
    <h3>API database stadium yang berisikan data:</h3>
    <ul>
      <li>id_stadium</li>
      <li>stadium</li>
      <li>country</li>
    </ul>
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

# ENDPOINT-2 delete stadium data
@stadiumAPI.route('/deletestadium/<string:document_id>', methods=['DELETE'])
def deletestadium(document_id):
    try:
        document_ref = stadium_Ref.document(document_id)

        if document_ref.get().exists:
            document_ref.delete()
            return jsonify({"success": True, "deleted_time": current_datetime, "message": f"Document {document_id} deleted"}), 200
        else:
            return jsonify({"success": False, "message": f"Document {document_id} not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {e}"}), 500