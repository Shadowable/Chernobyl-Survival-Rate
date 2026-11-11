import math
import os
from typing import Any

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException, InternalServerError


def calculate_demo_index(
    age: int,
    distance_km: float,
    physical_ability: int,
    dose_rate_usv_h: float,
) -> float:
    normalized_values = (
        age / 120 * 100,
        distance_km / 1000 * 100,
        physical_ability / 10 * 100,
        dose_rate_usv_h / 1_000_000 * 100,
    )
    return round(sum(normalized_values) / len(normalized_values), 1)


def create_app() -> Flask:
    app = Flask(__name__)

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException):
        return jsonify(error=error.description), error.code

    @app.errorhandler(InternalServerError)
    def handle_internal_error(_error: InternalServerError):
        return jsonify(error="Internal server error"), 500

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.post("/predict")
    def predict():
        if not request.is_json:
            return jsonify(error="Content-Type must be application/json"), 415

        payload: Any = request.get_json()
        if not isinstance(payload, dict):
            return jsonify(error="Request body must be a JSON object"), 400

        expected_fields = {
            "age",
            "distance_km",
            "physical_ability",
            "dose_rate_usv_h",
        }
        if set(payload) != expected_fields:
            return jsonify(
                error="Provide exactly age, distance_km, physical_ability, "
                "and dose_rate_usv_h"
            ), 400

        age = payload["age"]
        physical_ability = payload["physical_ability"]
        distance_km = payload["distance_km"]
        dose_rate_usv_h = payload["dose_rate_usv_h"]

        if isinstance(age, bool) or not isinstance(age, int) or not 0 <= age <= 120:
            return jsonify(error="'age' must be a whole number from 0 to 120"), 400
        if (
            isinstance(physical_ability, bool)
            or not isinstance(physical_ability, int)
            or not 1 <= physical_ability <= 10
        ):
            return jsonify(
                error="'physical_ability' must be a whole number from 1 to 10"
            ), 400

        for field, value, maximum in (
            ("distance_km", distance_km, 1000),
            ("dose_rate_usv_h", dose_rate_usv_h, 1_000_000),
        ):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return jsonify(error=f"'{field}' must be a finite number"), 400
            try:
                is_finite = math.isfinite(float(value))
            except OverflowError:
                is_finite = False
            if not is_finite or not 0 <= value <= maximum:
                return jsonify(
                    error=f"'{field}' must be between 0 and {maximum}"
                ), 400

        return jsonify(
            demo_index=calculate_demo_index(
                age=age,
                distance_km=distance_km,
                physical_ability=physical_ability,
                dose_rate_usv_h=dose_rate_usv_h,
            ),
            notice=(
                "Fictional demo only. This index is not a survival probability, "
                "risk assessment, or safety guidance."
            ),
        )

    return app


if __name__ == "__main__":
    create_app().run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "5002")),
        debug=False,
    )
