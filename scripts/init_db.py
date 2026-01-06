#!/usr/bin/env python3
import argparse
import sqlite3
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize TARDOC SQLite database")
    parser.add_argument("--db", default="data/tardoc/tardoc.db")
    parser.add_argument("--schema", default="migrations/001_create_tardoc_tables.sql")
    args = parser.parse_args()

    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    schema_sql = Path(args.schema).read_text(encoding="utf-8")
    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema_sql)

    print(f"Initialized database at {db_path}")


if __name__ == "__main__":
    main()
