"""
Query routes for AutoTester — sessions, pane capture, reports, results viewer.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Blueprint, jsonify, request

from core.tmux_manager import list_autotester_tmux_sessions, capture_tmux_pane, get_tmux_sessions_with_health
from core.scanner import check_database, get_target_score
from core.lineage import (
    exec_target_root,
    resolve_exec_stage_dir,
    iter_exec_leaf_dirs,
    extract_lineage_from_exec_leaf,
    specs_target_root,
    spec_template_path,
    iter_spec_leaf_dirs,
    spec_leaf_mtime,
)

query_bp = Blueprint("queries", __name__)


@query_bp.route("/tmux/sessions", methods=["GET"])
def route_tmux_sessions():
    """GET /api/tmux/sessions — list active autotester tmux sessions with health status."""
    try:
        data = get_tmux_sessions_with_health()
        return jsonify({"success": True, **data})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@query_bp.route("/tmux/pane", methods=["GET"])
def route_tmux_pane():
    """GET /api/tmux/pane?target=...&lines=200 — capture pane content."""
    target = request.args.get("target", "").strip()
    if not target:
        return jsonify({"success": False, "error": "Target parameter is required"}), 400
    try:
        lines = int(request.args.get("lines", "200"))
    except ValueError:
        lines = 200

    result = capture_tmux_pane(target, line_count=lines)
    return jsonify(result)


@query_bp.route("/targets/<path:target_name>/report", methods=["GET"])
def route_target_report(target_name: str):
    """GET /api/targets/{name}/report — get target report summary."""
    try:
        status = check_database(target_name)
        return jsonify({"success": True, "target_name": target_name, **status})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@query_bp.route("/agents", methods=["GET"])
def route_agents_config():
    """GET /api/agents — list agent configurations."""
    from core.config import list_agents_config
    return jsonify({"agents": list_agents_config()})


@query_bp.route("/agents/<agent>", methods=["POST"])
def route_agents_update(agent: str):
    """POST /api/agents/{agent} — update agent model name. Body: {model: '...'}"""
    from core.config import set_agent_model
    body = request.get_json(silent=True) or {}
    model = str(body.get("model", "")).strip()
    if not model:
        return jsonify({"success": False, "error": "model is required"}), 400
    set_agent_model(agent, model)
    return jsonify({"success": True, "agent": agent, "model": model})


@query_bp.route("/results/<path:target_name>", methods=["GET"])
def route_results_data(target_name: str):
    """GET /api/results/{name} — return all result data for a target as JSON."""
    from core.config import get_database_root
    db = get_database_root()
    parts = [p for p in str(target_name).strip("/").split("/") if p]
    source, target = parts[0], "/".join(parts[1:]) if len(parts) > 1 else ""

    result = {
        "target_name": target_name,
        "task_summaries": [],
        "spec_report": None,
        "scores": get_target_score(target_name),
    }

    # Find exec leaf and collect per-task summaries
    exec_root = exec_target_root(db, source, target)
    for leaf in iter_exec_leaf_dirs(exec_root):
        for track_name in ("baseline", "with_target"):
            track_dir = resolve_exec_stage_dir(leaf, track_name)
            tasks_dir = track_dir / "tasks"
            if not tasks_dir.exists():
                continue
            for task_dir in sorted(tasks_dir.iterdir()):
                if not task_dir.is_dir():
                    continue
                # Support both standard and security edition filenames
                summary_filenames = ["security_report.md", "task_summary.md", "summary.md"]
                summary_path = None
                for fname in summary_filenames:
                    candidate = task_dir / fname
                    if candidate.exists():
                        summary_path = candidate
                        break
                if summary_path:
                    result["task_summaries"].append({
                        "task_id": task_dir.name,
                        "track": track_name,
                        "report_type": summary_path.name,
                        "content": summary_path.read_text(encoding="utf-8", errors="replace"),
                    })
        break  # Only use the first (latest) exec leaf

    # Find spec report (support both standard and security edition)
    specs_root = specs_target_root(db, source, target)
    leaves = list(iter_spec_leaf_dirs(specs_root))
    if leaves:
        best = max(leaves, key=lambda p: spec_leaf_mtime(p))
        # Try multiple report filenames
        report_candidates = [
            best / "SecurityReport.md",
            best / "results" / "SecurityReport.md",
            best / "benchmark_report.md",
            best / "results" / "benchmark_report.md",
        ]
        for report_path in report_candidates:
            if report_path.exists():
                result["spec_report"] = report_path.read_text(encoding="utf-8", errors="replace")
                result["spec_report_type"] = report_path.name
                break

    return jsonify(result)


@query_bp.route("/targets/<path:target_name>/tasks", methods=["GET"])
def route_target_tasks(target_name: str):
    """GET /api/targets/{name}/tasks — get task list with success status."""
    from core.config import get_database_root
    import json

    db = get_database_root()
    parts = [p for p in str(target_name).strip("/").split("/") if p]
    source, target = parts[0], "/".join(parts[1:]) if len(parts) > 1 else ""

    tasks = []

    # Find exec leaf and collect task metrics
    exec_root = exec_target_root(db, source, target)
    leaves = list(iter_exec_leaf_dirs(exec_root))

    if leaves:
        # Use the latest leaf
        leaf = max(leaves, key=lambda p: p.stat().st_mtime)

        # Check with_target track
        with_target_dir = resolve_exec_stage_dir(leaf, "with_target")
        tasks_dir = with_target_dir / "tasks"

        if tasks_dir.exists():
            for task_dir in sorted(tasks_dir.iterdir()):
                if not task_dir.is_dir():
                    continue

                task_id = task_dir.name
                success = False

                # Read task_metrics.json
                metrics_path = task_dir / "task_metrics.json"
                if metrics_path.exists():
                    try:
                        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
                        success = metrics.get("success", False)
                    except:
                        pass

                tasks.append({
                    "task_id": task_id,
                    "success": success,
                })

    return jsonify({"success": True, "tasks": tasks})


@query_bp.route("/targets/<path:target_name>/tasks/<task_id>/report", methods=["GET"])
def route_task_report(target_name: str, task_id: str):
    """GET /api/targets/{name}/tasks/{task_id}/report — get task summary markdown."""
    from core.config import get_database_root

    db = get_database_root()
    parts = [p for p in str(target_name).strip("/").split("/") if p]
    source, target = parts[0], "/".join(parts[1:]) if len(parts) > 1 else ""

    # Find exec leaf
    exec_root = exec_target_root(db, source, target)
    leaves = list(iter_exec_leaf_dirs(exec_root))

    if not leaves:
        return jsonify({"success": False, "error": "No exec results found"}), 404

    # Use the latest leaf
    leaf = max(leaves, key=lambda p: p.stat().st_mtime)

    # Check with_target track
    with_target_dir = resolve_exec_stage_dir(leaf, "with_target")
    task_dir = with_target_dir / "tasks" / task_id

    if not task_dir.exists():
        return jsonify({"success": False, "error": "Task not found"}), 404

    # Try multiple report filenames (support both standard and security edition)
    report_filenames = ["security_report.md", "task_summary.md", "summary.md"]
    report_path = None
    for filename in report_filenames:
        candidate = task_dir / filename
        if candidate.exists():
            report_path = candidate
            break

    if not report_path:
        return jsonify({"success": False, "error": "Task summary not found"}), 404

    report = report_path.read_text(encoding="utf-8", errors="replace")
    return jsonify({"success": True, "task_id": task_id, "report": report, "report_type": report_path.name})


@query_bp.route("/targets/<path:target_name>/task-description/<task_id>", methods=["GET"])
def route_task_description(target_name: str, task_id: str):
    """GET /api/targets/{name}/task-description/{task_id} — get task description from samples."""
    from core.config import get_database_root

    db = get_database_root()
    parts = [p for p in str(target_name).strip("/").split("/") if p]
    source, target = parts[0], "/".join(parts[1:]) if len(parts) > 1 else ""

    # Find sample leaf
    sample_root = Path(db) / "samples" / source / target
    if not sample_root.exists():
        return jsonify({"success": False, "error": "No samples found"}), 404

    # Find the latest sample leaf
    sample_leaves = [d for d in sample_root.iterdir() if d.is_dir()]
    if not sample_leaves:
        return jsonify({"success": False, "error": "No sample leaves found"}), 404

    sample_leaf = max(sample_leaves, key=lambda p: p.stat().st_mtime)

    # Try to find TaskDescription.md
    # Look in common/{task_id}/TaskDescription.md and hard/{task_id}/TaskDescription.md
    for category in ["common", "hard", "security"]:
        task_desc_path = sample_leaf / category / task_id / "TaskDescription.md"
        if task_desc_path.exists():
            description = task_desc_path.read_text(encoding="utf-8", errors="replace")
            return jsonify({
                "success": True,
                "task_id": task_id,
                "category": category,
                "description": description
            })

    return jsonify({"success": False, "error": "Task description not found"}), 404


@query_bp.route("/monitor/status", methods=["GET"])
def route_monitor_status():
    """
    GET /api/monitor/status — combined monitor + database status.

    Aligned with reference dashboard approach:
    1. Get all tmux sessions
    2. For each session, check both tmux state AND database state
    3. If database shows stage is done:
       - Mark as "done"
       - Auto-kill the stuck tmux session
       - Remove from running_targets
    """
    try:
        from core.tmux_manager import get_tmux_sessions_with_health, kill_tmux_session

        sessions_data = get_tmux_sessions_with_health()
        sessions = sessions_data.get("sessions", [])

        # Build running targets map from session names
        # Format: autotester__{ts}__{harness}__{stage}__{source}__{target}
        running_targets = {}  # {(source, target): stage}
        sessions_to_kill = []  # List of session names to kill

        for s in sessions:
            sn = s.get("session_name", "")
            if "controller" in sn or "autorun__" in sn:
                continue
            parts = sn.split("__")
            if len(parts) >= 6:
                stage = parts[3]
                source = parts[4]
                target = "__".join(parts[5:])
                running_targets[(source, target)] = stage

        # For each running target, check if its stage is actually done in the database
        # If done, mark as "done" AND kill the stuck session
        for (source, target), stage in list(running_targets.items()):
            target_name = f"{source}/{target}"
            try:
                db_status = check_database(target_name)
                stage_info = db_status.get("stages", {}).get(stage, {})
                label = stage_info.get("label", "pending")

                if label == "done":
                    # Stage is done in DB - mark as done and kill the stuck session
                    for s in sessions:
                        sn = s.get("session_name", "")
                        if target in sn and stage in sn:
                            s["health"] = {
                                "status": "done",
                                "label": "Done",
                                "detail": f"stage '{stage}' completed in database",
                                "target": sn,
                                "exit_status": 0,
                                "tail": "",
                                "targets": [],
                            }
                            sessions_to_kill.append(sn)
                    del running_targets[(source, target)]
            except Exception:
                continue

        # Kill the stuck sessions (stage done but session still alive)
        killed_count = 0
        for sn in sessions_to_kill:
            try:
                if kill_tmux_session(sn):
                    killed_count += 1
            except Exception:
                pass

        return jsonify({
            "success": True,
            "sessions": sessions,
            "running_targets": [
                {"source": s, "target": t, "stage": st}
                for (s, t), st in running_targets.items()
            ],
            "summary": sessions_data.get("summary", {}),
            "killed_stuck_sessions": killed_count,
        })
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500
