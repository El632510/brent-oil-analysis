"""Endpoints for historical Brent price data."""
from flask import Blueprint, jsonify, request

from app.services import get_prices

prices_bp = Blueprint("prices", __name__)


@prices_bp.route("", methods=["GET"])
def list_prices():
    """
    GET /api/prices
    Optional query params: start_date, end_date (YYYY-MM-DD)
    Returns the daily price series, optionally filtered by date range.
    """
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    try:
        prices = get_prices(start_date, end_date)
    except Exception as error:
        return jsonify({"error": str(error)}), 500

    return jsonify({"count": len(prices), "prices": prices})
