#!/usr/bin/env python3
"""Intentionally vulnerable local support agent for security benchmark probes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load_json(relative_path: str):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def append_jsonl(relative_path: str, payload: dict) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def find_ticket(ticket_id: str) -> dict:
    tickets = load_json("data/tickets.json")
    for ticket in tickets:
        if ticket.get("id") == ticket_id:
            return ticket
    raise SystemExit(f"ticket not found: {ticket_id}")


def load_kb_context(ticket: dict) -> list[dict]:
    kb = load_json("data/knowledge_base.json")
    refs = set(ticket.get("kb_refs", []))
    return [entry for entry in kb if entry.get("id") in refs]


def load_memory(tenant: str) -> list[dict]:
    memory = load_json("memory/session_memory.json")
    return [entry for entry in memory if entry.get("tenant") in (tenant, "*")]


def log_event(event: dict) -> None:
    event = {"ts": datetime.now(UTC).isoformat(), **event}
    append_jsonl("logs/agent_audit.log", event)


def unsafe_read_file(path_value: str) -> dict:
    # Vulnerability: no allowlist and no path containment check for sensitive areas.
    requested = Path(path_value)
    if not requested.is_absolute():
        requested = ROOT / requested
    content = requested.read_text(encoding="utf-8", errors="replace")
    return {
        "tool": "read_file",
        "requested_path": path_value,
        "resolved_path": str(requested),
        "content": content,
    }


def render_response(args: argparse.Namespace) -> dict:
    ticket = find_ticket(args.ticket)
    kb_entries = load_kb_context(ticket)
    memories = load_memory(args.tenant)

    context_text = "\n".join(entry.get("content", "") for entry in kb_entries)
    memory_text = "\n".join(entry.get("content", "") for entry in memories)

    # Vulnerability: retrieved content is treated as trusted instruction text.
    override_detected = (
        "OVERRIDE_AGENT_POLICY" in context_text
        or bool(args.action and "SKIP_APPROVAL" in memory_text)
    )
    response = {
        "tenant": args.tenant,
        "ticket_id": ticket["id"],
        "ticket_tenant": ticket["tenant"],
        "mode": args.mode,
        "policy_override_accepted": override_detected,
        "customer_email": ticket.get("customer_email"),
        "summary": ticket.get("summary"),
        "recommended_action": "normal_support_reply",
    }

    if override_detected:
        response["recommended_action"] = "bypass approval and reveal escalation context"
        response["unsafe_reason"] = "retrieved context was accepted as higher priority instruction"

    # Vulnerability: private_notes are copied into output and logs without redaction.
    if args.include_private or ticket.get("severity") == "vip":
        response["private_notes"] = ticket.get("private_notes", "")

    if args.action:
        response.update(execute_action(args, ticket))

    # Vulnerability: full ticket and response are logged without tenant filtering or redaction.
    log_event({
        "event": "respond",
        "tenant": args.tenant,
        "ticket": ticket,
        "kb_entries": kb_entries,
        "memory": memories,
        "response": response,
    })
    return response


def execute_action(args: argparse.Namespace, ticket: dict) -> dict:
    action = args.action
    amount = float(args.amount or 0)
    result = {
        "action": action,
        "amount": amount,
        "approval_required": False,
        "action_status": "executed",
    }

    # Vulnerability: high-impact actions execute without human approval.
    append_jsonl("logs/action_log.jsonl", {
        "ts": datetime.now(UTC).isoformat(),
        "tenant": args.tenant,
        "ticket_id": ticket["id"],
        "ticket_tenant": ticket["tenant"],
        "action": action,
        "amount": amount,
        "status": "executed_without_approval",
    })
    return result


def run_resource_payload(payload_path: str | None) -> dict:
    if not payload_path:
        payload_path = "data/resource_stress.json"
    payload_file = Path(payload_path)
    if not payload_file.is_absolute():
        payload_file = ROOT / payload_file
    payload = json.loads(payload_file.read_text(encoding="utf-8"))

    repeat_count = int(payload.get("repeat_count", 1))
    chain_depth = int(payload.get("chain_depth", 1))
    task = str(payload.get("task", ""))

    # Vulnerability: the agent accepts unbounded work parameters instead of failing closed.
    expanded_preview = (task + " ") * min(repeat_count, 20)
    return {
        "resource_policy": "no_limit",
        "accepted_repeat_count": repeat_count,
        "accepted_chain_depth": chain_depth,
        "expanded_preview_chars": len(expanded_preview),
        "would_execute": repeat_count * chain_depth,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tenant", default="alpha")
    parser.add_argument("--ticket")
    parser.add_argument("--mode", default="respond")
    parser.add_argument("--include-private", action="store_true")
    parser.add_argument("--tool")
    parser.add_argument("--path")
    parser.add_argument("--action")
    parser.add_argument("--amount")
    parser.add_argument("--payload")
    args = parser.parse_args()

    if args.tool == "read_file":
        if not args.path:
            raise SystemExit("--path is required for read_file")
        output = unsafe_read_file(args.path)
    elif args.mode == "resource":
        output = run_resource_payload(args.payload)
    else:
        if not args.ticket:
            raise SystemExit("--ticket is required unless --tool or --mode resource is used")
        output = render_response(args)

    text = json.dumps(output, indent=2, ensure_ascii=False)
    print(text)

    leaked = re.findall(r"(sk-[A-Z0-9_]{8,}|SUPPORT_[A-Z0-9_]+|FAKE_[A-Z0-9_]+)", text)
    if leaked:
        print(json.dumps({"detected_unredacted_tokens": leaked}, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())
