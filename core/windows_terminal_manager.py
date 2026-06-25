"""
Windows Terminal management for AutoTester.

Provides Windows-specific terminal launching using Windows Terminal,
PowerShell, or CMD as fallbacks.
"""

from __future__ import annotations

import ctypes
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Windows keep-awake constants
_ES_CONTINUOUS = 0x80000000
_ES_SYSTEM_REQUIRED = 0x00000001
_ES_DISPLAY_REQUIRED = 0x00000002


def _windows_keep_awake_start() -> None:
    """Prevent Windows from sleeping while the controller runs."""
    if not sys.platform.startswith("win"):
        return
    try:
        ctypes.windll.kernel32.SetThreadExecutionState(
            _ES_CONTINUOUS | _ES_SYSTEM_REQUIRED | _ES_DISPLAY_REQUIRED,
        )
    except Exception:
        pass


def _windows_keep_awake_stop() -> None:
    """Restore normal Windows sleep behaviour."""
    if not sys.platform.startswith("win"):
        return
    try:
        ctypes.windll.kernel32.SetThreadExecutionState(_ES_CONTINUOUS)
    except Exception:
        pass


def _safe_terminal_token(value: str, max_length: int = 48, *, add_hash: bool = False) -> str:
    """Sanitize a string for use in terminal/session names."""
    raw = str(value or "").strip()
    safe = re.sub(r"[^a-z0-9-]+", "-", raw.lower()).strip("-")
    if not safe:
        safe = "run"
    if len(safe) <= max_length:
        return safe
    if add_hash and max_length > 10:
        digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:8]
        prefix = safe[:max_length - 9].rstrip("-") or "run"
        return f"{prefix}-{digest}"
    return safe[:max_length].rstrip("-") or "run"


def build_terminal_profile_name(
    target_name: str,
    stage: str,
    harness: str,
    timestamp: str | None = None,
) -> str:
    """Build a unique terminal tab title: autotester__{ts}__{harness}__{stage}__{source}__{target}"""
    parts = [p for p in str(target_name or "").strip("/").split("/") if p]
    source = parts[0] if parts else "unknown"
    target = parts[1] if len(parts) > 1 else parts[0] if parts else "target"

    ts = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    components = [
        "autotester",
        ts,
        _safe_terminal_token(harness, 16),
        _safe_terminal_token(stage, 16),
        _safe_terminal_token(source, 24),
    ]
    prefix = "__".join(components) + "__"
    remaining = max(16, 100 - len(prefix))
    return prefix + _safe_terminal_token(target, remaining, add_hash=True)


def write_powershell_job_script(
    *,
    script_path: Path,
    launch_cwd: Path,
    mkdir_paths: list[Path],
    env_exports: dict[str, str],
    runner_command: str,
    title: str,
) -> None:
    """Write a PowerShell script that runs the harness command with logging."""
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
Write-Host "Running command:"
Write-Host @"
{runner_command}
"@
Write-Host "========================================"

$autotester_output_log = Join-Path $env:TEMP "autotester-output-$(Get-Date -Format 'yyyyMMddHHmmss').log"

try {{
    {runner_command} 2>&1 | Tee-Object -FilePath $autotester_output_log
    $status = $LASTEXITCODE
}} catch {{
    Write-Host "Error: $_"
    $status = 1
}}

# Check for fatal errors
if (Select-String -Path $autotester_output_log -Pattern "(Error|ERROR|Fatal|FATAL):\\s*(Insufficient Balance|Authentication failed|Unauthorized|Permission denied|Rate limit|API key)" -Quiet) {{
    Write-Host "[autotester] fatal runner output detected; overriding exit status to 1"
    $status = 1
}}

Remove-Item $autotester_output_log -ErrorAction SilentlyContinue

Write-Host "========================================"
Write-Host "Finished at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
Write-Host "Exit status: $status"
Write-Host "Press any key to close this window..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
"""

    script_path.write_text(script, encoding="utf-8")


def open_windows_terminal(
    *,
    profile_name: str,
    script_path: Path,
    log_path: Path,
    title: str,
) -> dict[str, Any]:
    """
    Open a Windows Terminal tab and start a job script in it.

    Returns launch payload with session info.
    """
    # Check if Windows Terminal is available
    wt_path = shutil.which("wt.exe")
    if not wt_path:
        # Fallback to PowerShell window
        return open_powershell_window(
            profile_name=profile_name,
            script_path=script_path,
            title=title,
        )

    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Build Windows Terminal command
    # wt.exe -w 0 new-tab -d "{cwd}" --title "{title}" PowerShell -NoExit -File "{script}"
    cmd = [
        "wt.exe",
        "-w", "0",  # Use current window
        "new-tab",
        "-d", str(script_path.parent),
        "--title", title,
        "PowerShell.exe",
        "-NoExit",
        "-ExecutionPolicy", "Bypass",
        "-File", str(script_path),
    ]

    try:
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW,
        )

        return {
            "success": True,
            "terminal": "windows-terminal",
            "profile_name": profile_name,
            "title": title,
            "log_path": str(log_path),
            "script_path": str(script_path),
        }
    except Exception as exc:
        # Fallback to PowerShell
        return open_powershell_window(
            profile_name=profile_name,
            script_path=script_path,
            title=title,
            error=str(exc),
        )


def open_powershell_window(
    *,
    profile_name: str,
    script_path: Path,
    title: str,
    error: str = "",
) -> dict[str, Any]:
    """Open a standalone PowerShell window as fallback."""
    cmd = [
        "PowerShell.exe",
        "-NoExit",
        "-ExecutionPolicy", "Bypass",
        "-Command",
        f"$Host.UI.RawUI.WindowTitle = '{title}'; & '{script_path}'",
    ]

    try:
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW,
        )

        return {
            "success": True,
            "terminal": "powershell",
            "profile_name": profile_name,
            "title": title,
            "script_path": str(script_path),
            "fallback_reason": error or "Windows Terminal not available",
        }
    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
            "profile_name": profile_name,
            "script_path": str(script_path),
        }


def list_windows_terminal_tabs() -> list[dict[str, Any]]:
    """
    List Windows Terminal tabs running AutoTester jobs.

    Note: This is best-effort detection on Windows.
    Returns list of tab-like objects with basic info.
    """
    # On Windows, we can't easily enumerate terminal tabs like tmux sessions
    # Instead, we check for running PowerShell processes that match our pattern

    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq PowerShell.exe", "/FO", "CSV", "/V"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        tabs = []
        for line in result.stdout.splitlines()[1:]:  # Skip header
            if not line.strip():
                continue
            # Parse CSV: "Image Name","PID","Session Name","Session#","Mem Usage","Status","User Name","CPU Time","Window Title"
            parts = [p.strip('"') for p in line.split(',')]
            if len(parts) < 9:
                continue

            window_title = parts[8]
            if "autotester__" in window_title.lower():
                tabs.append({
                    "process_id": int(parts[1]),
                    "window_title": window_title,
                    "status": parts[5],
                    "memory": parts[4],
                })

        return tabs
    except Exception:
        return []


def kill_windows_terminal_tab(process_id: int) -> bool:
    """Kill a Windows Terminal tab by process ID."""
    try:
        subprocess.run(
            ["taskkill", "/PID", str(process_id), "/F"],
            capture_output=True,
            timeout=10,
        )
        return True
    except Exception:
        return False


# ── Unified Terminal Session Interface ────────────────────────────────────────

class TerminalSession:
    """Unified interface for terminal sessions (tmux or Windows Terminal)."""

    def __init__(self, name: str, platform: str = "auto"):
        self.name = name
        self.platform = platform if platform != "auto" else (
            "windows" if sys.platform.startswith("win") else "unix"
        )

    def launch(
        self,
        *,
        script_path: Path,
        log_path: Path,
        title: str,
        mkdir_paths: list[Path] = None,
        env_exports: dict[str, str] = None,
        runner_command: str = "",
    ) -> dict[str, Any]:
        """Launch a new terminal session."""
        if self.platform == "windows":
            return open_windows_terminal(
                profile_name=self.name,
                script_path=script_path,
                log_path=log_path,
                title=title,
            )
        else:
            # Unix: Use tmux (imported from tmux_manager)
            from .tmux_manager import open_tmux_window

            return open_tmux_window(
                session_name=self.name,
                window_name=title,
                title=title,
                script_path=script_path,
                log_path=log_path,
                prompt_path=Path("/tmp/placeholder"),  # Not used in this context
                create_session=True,
            )

    def exists(self) -> bool:
        """Check if session exists."""
        if self.platform == "windows":
            # Check for Windows Terminal process with this name
            tabs = list_windows_terminal_tabs()
            return any(self.name in tab.get("window_title", "") for tab in tabs)
        else:
            from .tmux_manager import tmux_session_exists
            return tmux_session_exists(self.name)

    def kill(self) -> bool:
        """Kill the session."""
        if self.platform == "windows":
            tabs = list_windows_terminal_tabs()
            for tab in tabs:
                if self.name in tab.get("window_title", ""):
                    return kill_windows_terminal_tab(tab["process_id"])
            return False
        else:
            from .tmux_manager import kill_tmux_session
            return kill_tmux_session(self.name)

    def capture(self, line_count: int = 200) -> str:
        """Capture session output."""
        if self.platform == "windows":
            # Not easily supported on Windows
            return "[Windows Terminal capture not supported]"
        else:
            from .tmux_manager import capture_tmux_pane
            result = capture_tmux_pane(self.name, line_count)
            return result.get("content", "")
