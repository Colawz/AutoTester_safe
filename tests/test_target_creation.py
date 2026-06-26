from pathlib import Path

from api.app import create_app
from core import target_manager


def test_create_target_accepts_windows_backslash_separator(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.setattr(target_manager, "get_targets_root", lambda: tmp_path / "TargetsRepo")

    client = create_app().test_client()
    response = client.post(
        "/api/targets",
        json={"name": r"WinSource\sample-tool", "description": "Requirement text"},
    )

    payload = response.get_json()
    assert response.status_code == 201
    assert payload["success"] is True
    assert payload["name"] == "WinSource/sample-tool"
    assert (tmp_path / "TargetsRepo" / "WinSource" / "sample-tool" / "requirement.md").exists()
