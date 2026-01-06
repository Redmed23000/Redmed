#!/usr/bin/env python3
import argparse
import json
import sqlite3
from datetime import datetime
from pathlib import Path


def load_rules(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def upsert_codes(conn: sqlite3.Connection, rules: dict, source_version: str) -> None:
    for code in rules.get("codes", []):
        conn.execute(
            """
            INSERT INTO codes (code, description, time_unit_minutes, source_version, effective_date, expiry_date)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(code) DO UPDATE SET
                description = excluded.description,
                time_unit_minutes = excluded.time_unit_minutes,
                source_version = excluded.source_version,
                effective_date = excluded.effective_date,
                expiry_date = excluded.expiry_date
            """,
            (
                code["code"],
                code.get("description", ""),
                code.get("time_unit_minutes", 0),
                source_version,
                code.get("effective_date", datetime.utcnow().date().isoformat()),
                code.get("expiry_date"),
            ),
        )


def upsert_exclusions(conn: sqlite3.Connection, rules: dict, source_version: str) -> None:
    for exclusion in rules.get("exclusions", []):
        code_id = conn.execute("SELECT id FROM codes WHERE code = ?", (exclusion["code"],)).fetchone()
        if not code_id:
            continue
        conn.execute(
            """
            INSERT INTO exclusions (code_id, excluded_code, reason, source_version, effective_date, expiry_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                code_id[0],
                exclusion["excluded_code"],
                exclusion.get("reason"),
                source_version,
                exclusion.get("effective_date", datetime.utcnow().date().isoformat()),
                exclusion.get("expiry_date"),
            ),
        )


def upsert_incompatibilities(conn: sqlite3.Connection, rules: dict, source_version: str) -> None:
    for incompat in rules.get("incompatibilities", []):
        code_a = conn.execute("SELECT id FROM codes WHERE code = ?", (incompat["code_a"],)).fetchone()
        code_b = conn.execute("SELECT id FROM codes WHERE code = ?", (incompat["code_b"],)).fetchone()
        if not code_a or not code_b:
            continue
        conn.execute(
            """
            INSERT INTO incompatibilities (code_id_a, code_id_b, reason, source_version, effective_date, expiry_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                code_a[0],
                code_b[0],
                incompat.get("reason"),
                source_version,
                incompat.get("effective_date", datetime.utcnow().date().isoformat()),
                incompat.get("expiry_date"),
            ),
        )


def upsert_conditions(conn: sqlite3.Connection, rules: dict, source_version: str) -> None:
    for condition in rules.get("conditions", []):
        code_id = conn.execute("SELECT id FROM codes WHERE code = ?", (condition["code"],)).fetchone()
        if not code_id:
            continue
        conn.execute(
            """
            INSERT INTO conditions (code_id, expression, message, source_version, effective_date, expiry_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                code_id[0],
                condition["expression"],
                condition.get("message"),
                source_version,
                condition.get("effective_date", datetime.utcnow().date().isoformat()),
                condition.get("expiry_date"),
            ),
        )


def upsert_limits(conn: sqlite3.Connection, rules: dict, source_version: str) -> None:
    for limit in rules.get("limits", []):
        code_id = conn.execute("SELECT id FROM codes WHERE code = ?", (limit["code"],)).fetchone()
        if not code_id:
            continue
        conn.execute(
            """
            INSERT INTO limits (code_id, limit_type, value, period, message, source_version, effective_date, expiry_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                code_id[0],
                limit["limit_type"],
                limit["value"],
                limit.get("period", "unknown"),
                limit.get("message"),
                source_version,
                limit.get("effective_date", datetime.utcnow().date().isoformat()),
                limit.get("expiry_date"),
            ),
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Update TARDOC rules from JSON bundle")
    parser.add_argument("--db", default="data/tardoc/tardoc.db")
    parser.add_argument("--rules", required=True, help="Path to JSON rules bundle")
    parser.add_argument("--version", required=True, help="Source version for the update")
    args = parser.parse_args()

    rules_path = Path(args.rules)
    if not rules_path.exists():
        raise SystemExit(f"Rules file not found: {rules_path}")

    with sqlite3.connect(args.db) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        rules = load_rules(rules_path)
        upsert_codes(conn, rules, args.version)
        upsert_exclusions(conn, rules, args.version)
        upsert_incompatibilities(conn, rules, args.version)
        upsert_conditions(conn, rules, args.version)
        upsert_limits(conn, rules, args.version)
        conn.execute(
            "INSERT INTO tardoc_updates (source_version, applied_at, summary) VALUES (?, ?, ?)",
            (args.version, datetime.utcnow().isoformat(), f"Loaded {rules_path.name}"),
        )

    print(f"Updated rules from {rules_path}")


if __name__ == "__main__":
    main()
