"""
Stage launcher — main orchestration for AutoTester pipeline stages.

Migrated from SkillTester's open_terminal_with_runner() and stage launchers.
Orchestrates the full launch flow: prompt building → tmux session creation → job execution.
"""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path
from typing import Any

from .cleaner import delete_exec_track_data, delete_target_stage_data
from .config import get_base_dir, get_database_root, get_runtime_root, get_stage_config
from .prompt_builder import (
    EXEC_TRACK_JOB_IDS,
    _get_stage_jobs,
    build_stage_prompt,
)
from .shell_detect import detect_shell
from .tmux_manager import (
    build_tmux_runner_command,
    build_tmux_session_name,
    build_tmux_window_name,
    open_tmux_window,
    tmux_exists,
    write_tmux_job_script,
)


# ── Track stagger ────────────────────────────────────────────────────────────

_EXEC_FULL_TRACK_STAGGER_SECONDS = float(
    os.environ.get("AUTOTEST_EXEC_TRACK_STAGGER_SECONDS", "30")
)


def _exec_track_stagger_seconds(
    stage: str,
    harness: str,
    job_count: int,
    only_job_id: str | None,
) -> float:
    """Delay between opening exec track windows. Only for opencode full track."""
    if stage != "exec":
        return 0.0
    if harness != "opencode":
        return 0.0
    if only_job_id is not None:
        return 0.0
    if job_count <= 1:
        return 0.0
    return _EXEC_FULL_TRACK_STAGGER_SECONDS


# ── Main launcher ────────────────────────────────────────────────────────────

def launch_stage(
    target_name: str,
    stage: str,
    harness_name: str = "opencode",
    *,
    only_job_id: str | None = None,
    api_key: str = "",
) -> dict[str, Any]:
    """
    Main launch orchestrator. Creates a tmux session, opens windows for each
    stage job, and starts harness processes.

    Args:
        target_name: 'source/target' identifier
        stage: 'sample', 'exec', or 'spec'
        harness_name: harness identifier ('opencode', 'claude', etc.)
        only_job_id: if set, only launch this specific job (for single-track exec)
        api_key: API key for harnesses that need one (kimi)

    Returns launch result with session info, attach command, and job list.
    """
    harness_name = harness_name.strip().lower()

    shell = detect_shell()
    is_windows = not shell.is_unix

    if not is_windows and not tmux_exists():
        return {
            "success": False,
            "error": (
                "tmux is not installed on this server. "
                "Install tmux first, e.g.: sudo yum install -y tmux"
            ),
        }

    jobs = _get_stage_jobs(stage)

    if only_job_id is not None:
        jobs = [j for j in jobs if j["job_id"] == only_job_id]
        if not jobs:
            raise ValueError(f"Unsupported job id for stage {stage}: {only_job_id}")

    from harnesses import get_harness
    adapter = get_harness(harness_name)

    stagger_seconds = _exec_track_stagger_seconds(
        stage=stage,
        harness=harness_name,
        job_count=len(jobs),
        only_job_id=only_job_id,
    )

    database_dir = get_database_root()
    runtime_root = get_runtime_root()
    base_dir = get_base_dir()

    try:
        launched_jobs = []
        session_name = build_tmux_session_name(target_name, stage, harness_name)
        run_root = runtime_root / session_name

        for index, job in enumerate(jobs):
            prompt_result = build_stage_prompt(
                target_name, stage, harness_name, job,
                database_dir=database_dir,
            )
            prompt_text = str(prompt_result["prompt_text"])
            launch_cwd = Path(prompt_result["launch_cwd"])
            mkdir_paths = [
                Path(p) for p in prompt_result.get("mkdir_paths", [])
                if str(p or "").strip()
            ]
            env_exports = {
                "AUTOTEST_HARNESS": harness_name,
                **{k: str(v) for k, v in prompt_result.get("env_exports", {}).items()},
            }

            # Window title
            if job["output_kind"] == "exec_baseline":
                window_title = f"{adapter.display_name} {job['window_prefix']}"
            else:
                window_title = f"{adapter.display_name} {job['window_prefix']}: {target_name}"

            window_name = build_tmux_window_name(str(job["job_id"]), index)
            job_dir = run_root / window_name
            prompt_path = job_dir / "prompt.txt"
            log_path = job_dir / "pane.log"

            prompt_path.parent.mkdir(parents=True, exist_ok=True)
            prompt_path.write_text(prompt_text, encoding="utf-8")

            runner_command = build_tmux_runner_command(
                harness_name=harness_name,
                prompt_file=prompt_path,
                workspace_root=launch_cwd,
                base_dir=base_dir,
                prompt_dir=str(job_dir),
                api_key=api_key,
            )

            if is_windows:
                # Windows: write .ps1 and launch via subprocess.Popen
                script_path = job_dir / "run.ps1"
                _write_windows_job_script(
                    script_path=script_path,
                    launch_cwd=launch_cwd,
                    mkdir_paths=mkdir_paths,
                    env_exports=env_exports,
                    runner_command=runner_command,
                    title=window_title,
                )

                result = _open_windows_terminal(
                    window_title=window_title,
                    script_path=script_path,
                    launch_cwd=launch_cwd,
                )
                launched_jobs.append(result)

            else:
                # Unix: write .sh and launch via tmux
                script_path = job_dir / "run.sh"
                write_tmux_job_script(
                    script_path=script_path,
                    launch_cwd=launch_cwd,
                    mkdir_paths=mkdir_paths,
                    env_exports=env_exports,
                    runner_command=runner_command,
                    title=window_title,
                    shell=shell,
                )

                launched_jobs.append(
                    open_tmux_window(
                        session_name=session_name,
                        window_name=window_name,
                        title=window_title,
                        script_path=script_path,
                        log_path=log_path,
                        prompt_path=prompt_path,
                        create_session=(index == 0),
                    )
                )

            # Stagger between windows
            if index < len(jobs) - 1:
                delay = stagger_seconds if stagger_seconds > 0 else 1
                time.sleep(delay)

        stage_config = get_stage_config(stage)
        launch_label = jobs[0]["label"] if len(jobs) == 1 else stage_config.get("label", stage)

        if is_windows:
            return {
                "success": True,
                "message": (
                    f"{adapter.display_name} launched for {target_name} "
                    f"({launch_label}, {len(launched_jobs)} terminal window(s)). "
                ),
                "harness": harness_name,
                "stage": stage,
                "job_scope": only_job_id or "all",
                "database_root": str(database_dir),
                "session_name": session_name,
                "run_root": str(run_root),
                "launched_jobs": launched_jobs,
            }
        else:
            return {
                "success": True,
                "message": (
                    f"{adapter.display_name} launched for {target_name} "
                    f"({launch_label}, {len(launched_jobs)} tmux window(s)). "
                    f"Attach with: tmux attach -t {session_name}"
                ),
                "harness": harness_name,
                "stage": stage,
                "job_scope": only_job_id or "all",
                "database_root": str(database_dir),
                "tmux_session": session_name,
                "attach_command": f"tmux attach -t {session_name}",
                "run_root": str(run_root),
                "launched_jobs": launched_jobs,
            }

    except NotImplementedError as exc:
        return {"success": False, "error": str(exc)}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


# ── Convenience launchers ────────────────────────────────────────────────────

def launch_sample_stage(
    target_name: str,
    harness_name: str = "opencode",
    *,
    api_key: str = "",
) -> dict[str, Any]:
    """Launch SampleAgent for a target. Cleans old sample+exec+specs data first."""
    cleanup = delete_target_stage_data(target_name, "sample", harness=harness_name)
    result = launch_stage(target_name, "sample", harness_name, api_key=api_key)
    result["database_cleanup"] = cleanup
    return result


def launch_exec_stage(
    target_name: str,
    harness_name: str = "opencode",
    *,
    api_key: str = "",
    mode: str = "single",  # "single" = with_target only, "dual" = baseline + with_target
) -> dict[str, Any]:
    """Launch ExecAgent for a target. mode='single' runs only with_target track (default)."""
    from .scanner import check_database
    db_status = check_database(target_name)
    if not db_status.get("sample_done"):
        raise ValueError(
            f"Sample stage is not complete for {target_name}. "
            "Run sample stage first."
        )

    if mode == "single":
        # Only launch with_target track
        cleanup = delete_exec_track_data(target_name, "with_target", harness=harness_name)
        result = launch_stage(
            target_name, "exec", harness_name,
            only_job_id="exec_withtarget",
            api_key=api_key,
        )
    else:
        # Launch both tracks
        cleanup = delete_target_stage_data(target_name, "exec", harness=harness_name)
        result = launch_stage(target_name, "exec", harness_name, api_key=api_key)

    result["database_cleanup"] = cleanup
    result["exec_mode"] = mode
    return result


def launch_exec_track_stage(
    target_name: str,
    harness_name: str = "opencode",
    track: str = "baseline",
    *,
    api_key: str = "",
) -> dict[str, Any]:
    """Launch a single exec track (baseline or with_target). Requires sample_done."""
    if track not in EXEC_TRACK_JOB_IDS:
        raise ValueError(f"Unsupported exec track: {track}. Use 'baseline' or 'with_target'.")

    from .scanner import check_database
    db_status = check_database(target_name)
    if not db_status.get("sample_done"):
        raise ValueError(
            f"Sample stage is not complete for {target_name}. "
            "Run sample stage first."
        )

    cleanup = delete_exec_track_data(target_name, track, harness=harness_name)
    result = launch_stage(
        target_name, "exec", harness_name,
        only_job_id=EXEC_TRACK_JOB_IDS[track],
        api_key=api_key,
    )
    result["database_cleanup"] = cleanup
    result["exec_track"] = track
    return result


def launch_spec_stage(
    target_name: str,
    harness_name: str = "opencode",
    *,
    api_key: str = "",
) -> dict[str, Any]:
    """Launch SpecAgent for a target. Requires sample_done."""
    from .scanner import check_database
    db_status = check_database(target_name)
    if not db_status.get("sample_done"):
        raise ValueError(
            f"Sample stage is not complete for {target_name}. "
            "Run sample stage first."
        )

    cleanup = delete_target_stage_data(target_name, "spec", harness=harness_name)
    result = launch_stage(target_name, "spec", harness_name, api_key=api_key)
    result["database_cleanup"] = cleanup
    return result


# ── Windows helpers ────────────────────────────────────────────────────────

def _write_windows_job_script(
    *,
    script_path: Path,
    launch_cwd: Path,
    mkdir_paths: list[Path],
    env_exports: dict[str, str],
    runner_command: str,
    title: str,
) -> None:
    """Write a PowerShell script for Windows terminal launch."""
    script_path.parent.mkdir(parents=True, exist_ok=True)

    mkdir_lines = "\n".join(
        f'New-Item -ItemType Directory -Force -Path "{p}" | Out-Null'
        for p in mkdir_paths
    )

    export_lines = "\n".join(
        f'$env:{key} = "{value}"'
        for key, value in env_exports.items()
        if str(value or "").strip()
    )

    script = f"""# AutoTester Job Script
# Title: {title}

Write-Host "========================================"
Write-Host "  AutoTester - {title}"
Write-Host "========================================"
Write-Host "Started at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"

{mkdir_lines}

Set-Location "{launch_cwd}"
{export_lines}

Write-Host "Working directory: $(Get-Location)"
Write-Host "========================================"

{runner_command}

Write-Host "========================================"
Write-Host "Finished at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
Write-Host "Exit status: $LASTEXITCODE"
Write-Host "Press any key to close this window..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
"""

    script_path.write_text(script, encoding="utf-8")


def _open_windows_terminal(
    *,
    window_title: str,
    script_path: Path,
    launch_cwd: Path,
) -> dict[str, Any]:
    """Open a new PowerShell window on Windows."""
    import platform as _plat

    powershell = "powershell.exe"
    system_root = os.environ.get("SystemRoot", "C:\\Windows")
    candidate = Path(system_root) / "System32" / "WindowsPowerShell" / "v1.0" / "powershell.exe"
    if candidate.exists():
        powershell = str(candidate)
    elif shutil.which("pwsh.exe"):
        powershell = "pwsh.exe"

    cmd = [
        powershell,
        "-NoLogo",
        "-NoExit",
        "-ExecutionPolicy", "Bypass",
        "-File", str(script_path),
    ]

    try:
        process = subprocess.Popen(
            cmd,
            cwd=str(launch_cwd),
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )
    except (AttributeError, OSError):
        process = subprocess.Popen(cmd, cwd=str(launch_cwd))

    return {
        "success": True,
        "title": window_title,
        "pid": process.pid,
        "script_path": str(script_path),
        "terminal": "powershell",
    }
