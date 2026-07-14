"""Endpoints for high-level summary statistics used in dashboard cards."""
from flask import Blueprint, jsonify

from app.services import get_summary_stats

summary_bp = Blueprint("summary", __name__)


@summary_bp.route("", methods=["GET"])
def get_summary():
    """
    GET /api/summary
    Returns headline numbers for the dashboard summary cards: date range,
    min/max/avg price, and average daily volatility.
    """
    try:
        stats = get_summary_stats()
    except Exception as error:
        return jsonify({"error": str(error)}), 500

    return jsonify(stats)
