"""Endpoints for the researched geopolitical/economic events dataset."""
from flask import Blueprint, jsonify

from app.services import get_events

events_bp = Blueprint("events", __name__)


@events_bp.route("", methods=["GET"])
def list_events():
    """
    GET /api/events
    Returns the full list of researched events used for change point
    association (date, name, category, description).
    """
    try:
        events = get_events()
    except Exception as error:
        return jsonify({"error": str(error)}), 500

    return jsonify({"count": len(events), "events": events})
