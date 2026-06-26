"""
Target management routes for AutoTester.
"""

from __future__ import annotations

import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Blueprint, jsonify, request

from core.scanner import scan_all_targets, check_database
from core.target_manager import create_target, delete_target, get_target_path, list_targets

target_bp = Blueprint("targets", __name__)


@target_bp.route("/targets", methods=["POST"])
def create_target_route():
    """POST /api/targets — create a new target with requirement.md + optional source zip."""
    body = request.get_json(silent=True) or {}

    name = str(body.get("name", "")).strip()
    description = str(body.get("description", "")).strip()

    if not name:
        return jsonify({"success": False, "error": "Target name is required"}), 400
    if "/" not in name:
        return jsonify({"success": False, "error": "Target name must be in 'source/target' format"}), 400
    if not description:
        return jsonify({"success": False, "error": "Description is required"}), 400

    # Handle source zip (base64-encoded)
    source_zip_raw = None
    if body.get("source_zip"):
        try:
            source_zip_raw = base64.b64decode(body["source_zip"])
        except Exception:
            return jsonify({"success": False, "error": "Invalid base64 encoding for source_zip"}), 400

    try:
        result = create_target(name, description, source_zip_raw)
        return jsonify(result), 201
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@target_bp.route("/targets", methods=["GET"])
def list_targets_route():
    """GET /api/targets — list all targets with scan status."""
    try:
        force_refresh = request.args.get("refresh", "").lower() in ("1", "true", "yes")
        data = scan_all_targets()
        return jsonify(data)
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@target_bp.route("/targets/<path:target_name>", methods=["GET"])
def get_target_route(target_name: str):
    """GET /api/targets/{name} — get single target detail."""
    try:
        status = check_database(target_name)
        return jsonify({"success": True, "target_name": target_name, **status})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@target_bp.route("/targets/<path:target_name>/requirement", methods=["GET"])
def get_target_requirement_route(target_name: str):
    """GET /api/targets/{name}/requirement — read requirement.md for a target."""
    try:
        target_path = get_target_path(target_name)
        requirement_path = target_path / "requirement.md"
        if not requirement_path.exists():
            return jsonify({
                "success": False,
                "error": "requirement.md not found",
                "target_name": target_name,
            }), 404

        return jsonify({
            "success": True,
            "target_name": target_name,
            "path": str(requirement_path),
            "content": requirement_path.read_text(encoding="utf-8", errors="replace"),
        })
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@target_bp.route("/targets/<path:target_name>", methods=["DELETE"])
def delete_target_route(target_name: str):
    """DELETE /api/targets/{name} — delete target and all associated data."""
    try:
        result = delete_target(target_name)
        return jsonify(result)
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500
