from flask import request, jsonify
from datetime import datetime
from flask_apispec import MethodResource

from models.database.databasemodel import Logs, db

class ApiEndpoint(MethodResource):
    def post(self):
        try:
            # Récupérer les données envoyées en JSON
            data = request.get_json()

            uptime = data['Uptime']
            try:
                uptime_dt = datetime.strptime(uptime, "%Y-%m-%dT%H:%M:%S.%f")
            except ValueError:
                uptime_dt = uptime

            data["Computer"] = data["Computer"].upper()
            if data["User"][:9] == "MAGELLAN\\":
                data["User"] = data[9:].lower()

            new_logs = Logs(user=data['User'], computer=data['Computer'], date=datetime.now())

            db.session.add(new_logs)
            db.session.flush()
            db.session.refresh(new_logs)
            db.session.commit()

            return jsonify({"message": "Data received successfully", "data": "", "statusCode": 200})

        except Exception as e:
            return jsonify({"error": str(e), "statusCode": 500})
