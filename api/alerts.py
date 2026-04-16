from flask import Blueprint, jsonify
from storage.alerts import get_alerts

alerts_bp = Blueprint("alerts", __name__)

@alerts_bp.route("/alerts")
def alerts():
    return jsonify(get_alerts())