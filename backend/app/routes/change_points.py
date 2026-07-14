"""Endpoints for the Bayesian change point model results."""
from flask import Blueprint, jsonify

from app.services import get_change_point_results

change_points_bp = Blueprint("change_points", __name__)


@change_points_bp.route("", methods=["GET"])
def get_results():
    """
    GET /api/change-points
    Returns the detected change point date, its credible interval, the
    mean log return before/after, and the nearest researched events.
    """
    try:
        results = get_change_point_results()
    except FileNotFoundError:
        return jsonify({"error": "Change point results have not been generated yet"}), 404
    except Exception as error:
        return jsonify({"error": str(error)}), 500

    return jsonify(results)
