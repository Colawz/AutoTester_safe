"""
AutoTest controller routes for AutoTester.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Blueprint, jsonify, request

from core.tmux_manager import kill_tmux_session, list_autotester_tmux_sessions
from core.shell_detect import detect_shell

autotest_bp = Blueprint("autotest", __name__)

AUTOTEST_DIR = Path(__file__).resolve().parent.parent / "autotest"
STATE_PATH = AUTOTEST_DIR / "auto_stage_state.json"
LOG_PATH = AUTOTEST_DIR / "auto_stage_loop.log"
HISTORY_PATH = AUTOTEST_DIR / "auto_stage_history.jsonl"
CONFIG_PATH = AUTOTEST_DIR / "auto_stage_config.json"


@autotest_bp.route("/autotest/status", methods=["GET"])
def route_autotest_status():
    """GET /api/autotest/status — current controller status."""
    try:
        state = {}
        if STATE_PATH.exists():
            state = json.loads(STATE_PATH.read_text(encoding="utf-8"))

        log_tail = []
        if LOG_PATH.exists():
            lines = LOG_PATH.read_text(encoding="utf-8", errors="replace").splitlines()
            log_tail = lines[-80:]

        history_tail = []
        if HISTORY_PATH.exists():
            for line in HISTORY_PATH.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if line:
                    try:
                        history_tail.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass

        # Count active worker sessions
        sessions = list_autotester_tmux_sessions()
        worker_count = len([s for s in sessions if "controller" not in s.get("session_name", "")])

        return jsonify({
            "running": bool(state.get("cycle_id")),
            "state": state,
            "log_tail": log_tail,
            "history_tail": history_tail[-80:],
            "worker_count": worker_count,
        })
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@autotest_bp.route("/autotest/start", methods=["POST"])
def route_autotest_start():
    """POST /api/autotest/start — start the AutoTest controller."""
    shell = detect_shell()
    if shell.is_unix and not shell.supports_tmux:
        return jsonify({
            "success": False,
            "error": "AutoTest requires tmux on Unix. Install tmux first.",
        }), 400

    try:
        body = request.get_json(silent=True) or {}

        # Write config
        config = {
            "stage": body.get("stage", "exec"),
            "launch_mode": body.get("launch_mode", "once"),
            "once": body.get("once", True),
            "test_mode": body.get("test_mode", "full"),
            "candidate_mode": body.get("candidate_mode", "pending"),
            "skill_scope": body.get("scope", "stage_pending"),
            "skill_repo": body.get("repo", "__all__"),
            "runner_plan": body.get("runner_plan", ["opencode:10"]),
        }
        AUTOTEST_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")

        # Build command
        controller_script = Path(__file__).resolve().parent.parent / "autotest" / "controller.py"
        args = [
            sys.executable, str(controller_script),
            "--config", str(CONFIG_PATH),
            "--once",
        ]
        if body.get("stage"):
            args.extend(["--stage", str(body["stage"])])

        command = " ".join(f"'{a}'" if " " in a else a for a in args)

        # Launch in tmux
        session_name = "autotester__auto__controller"
        subprocess.run(
            ["tmux", "new-session", "-d", "-s", session_name, "-n", "auto_loop", command],
            capture_output=True, text=True, timeout=30,
        )

        return jsonify({
            "success": True,
            "message": f"AutoTest controller started. Attach: tmux attach -t {session_name}",
            "session": session_name,
            "command": command,
        })
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@autotest_bp.route("/autotest/stop", methods=["POST"])
def route_autotest_stop():
    """POST /api/autotest/stop — stop the controller."""
    killed = kill_tmux_session("autotester__auto__controller")
    return jsonify({
        "success": killed,
        "message": "Controller stopped" if killed else "No running controller found",
    })


@autotest_bp.route("/autotest/kill-sessions", methods=["POST"])
def route_autotest_kill_sessions():
    """POST /api/autotest/kill-sessions — kill all worker sessions."""
    sessions = list_autotester_tmux_sessions()
    killed = 0
    for s in sessions:
        name = s.get("session_name", "")
        if "controller" not in name:
            if kill_tmux_session(name):
                killed += 1
    return jsonify({"success": True, "killed": killed, "total_sessions": len(sessions)})


@autotest_bp.route("/autotest/kill-session/<session_name>", methods=["POST"])
def route_autotest_kill_session(session_name: str):
    """POST /api/autotest/kill-session/<session_name> — kill a specific session."""
    # Security: only allow killing autotester__ sessions
    if not session_name.startswith("autotester__"):
        return jsonify({"success": False, "error": "Can only kill autotester__ sessions"}), 400

    killed = kill_tmux_session(session_name)
    return jsonify({
        "success": killed,
        "session_name": session_name,
        "message": f"Session {session_name} killed" if killed else f"Session {session_name} not found",
    })


@autotest_bp.route("/autotest/auto-run", methods=["POST"])
def route_autotest_auto_run():
    """
    POST /api/autotest/auto-run — start Auto-Run controller for a target.

    Body: {"target": "source/target", "harness": "opencode"}
    The controller runs in a tmux session and automatically launches
    sample -> exec -> spec stages sequentially.
    """
    from core.shell_detect import detect_shell

    shell = detect_shell()
    # Auto-Run controller currently uses tmux for session management.
    # On Windows, use the manual stage buttons instead.
    if shell.is_unix and not shell.supports_tmux:
        return jsonify({
            "success": False,
            "error": "Auto-Run requires tmux. Install tmux first.",
        }), 400
    elif not shell.is_unix:
        return jsonify({
            "success": False,
            "error": "Auto-Run controller is not supported on Windows yet. Please use the Sample/Exec/Spec buttons manually.",
        }), 400

    try:
        body = request.get_json(silent=True) or {}
        target = body.get("target", "").strip()
        if not target:
            return jsonify({"success": False, "error": "target is required"}), 400

        harness = body.get("harness", "opencode")

        # Build controller command
        controller_script = Path(__file__).resolve().parent.parent / "autotest" / "auto_run_controller.py"
        args = [
            sys.executable, str(controller_script),
            "--target", target,
            "--harness", harness,
        ]
        command = " ".join(f"'{a}'" if " " in a else a for a in args)

        # Session name for the controller
        safe_target = target.replace("/", "-")
        session_name = f"autotester__autorun__{safe_target}"

        # Kill any existing session for this target
        from core.tmux_manager import list_autotester_tmux_sessions
        for s in list_autotester_tmux_sessions():
            if safe_target in s.get("session_name", ""):
                kill_tmux_session(s["session_name"])

        # Launch controller in tmux
        subprocess.run(
            ["tmux", "new-session", "-d", "-s", session_name, "-n", "controller", command],
            capture_output=True, text=True, timeout=30,
        )

        return jsonify({
            "success": True,
            "message": f"Auto-Run started for {target}. Controller will manage all stages.",
            "session": session_name,
            "target": target,
            "command": command,
        })
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@autotest_bp.route("/autotest/auto-run/status", methods=["GET"])
def route_autotest_auto_run_status():
    """GET /api/autotest/auto-run/status — get Auto-Run controller status."""
    try:
        from autotest.auto_run_controller import STATE_PATH, LOG_PATH

        state = {}
        if STATE_PATH.exists():
            try:
                state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
            except Exception:
                pass

        log_tail = []
        if LOG_PATH.exists():
            lines = LOG_PATH.read_text(encoding="utf-8", errors="replace").splitlines()
            log_tail = lines[-50:]

        return jsonify({
            "success": True,
            "state": state,
            "log_tail": log_tail,
        })
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@autotest_bp.route("/autotest/auto-run/stop", methods=["POST"])
def route_autotest_auto_run_stop():
    """POST /api/autotest/auto-run/stop — stop the Auto-Run controller."""
    try:
        from core.tmux_manager import list_autotester_tmux_sessions
        from autotest.auto_run_controller import STATE_PATH

        killed = 0
        sessions = list_autotester_tmux_sessions()
        for s in sessions:
            name = s.get("session_name", "")
            if "autorun__" in name:
                if kill_tmux_session(name):
                    killed += 1

        # Update state
        if STATE_PATH.exists():
            try:
                state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
                state["status"] = "stopped"
                state["stopped_at"] = __import__("datetime").datetime.now().astimezone().isoformat(timespec="seconds")
                STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
            except Exception:
                pass

        return jsonify({
            "success": True,
            "killed": killed,
            "message": f"Stopped {killed} auto-run session(s)",
        })
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500
