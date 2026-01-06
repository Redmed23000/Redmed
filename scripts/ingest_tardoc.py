#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest official TARDOC documentation")
    parser.add_argument("--source", required=True, help="Path to official TARDOC file")
    parser.add_argument("--version", required=True, help="Official TARDOC version identifier")
    parser.add_argument("--output-dir", default="data/tardoc/raw")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    source = Path(args.source)

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    dest = output_dir / f"{args.version}_{timestamp}_{source.name}"
    dest.write_bytes(source.read_bytes())

    metadata_path = output_dir.parent / "metadata.json"
    metadata = []
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    metadata.append(
        {
            "version": args.version,
            "stored_as": str(dest),
            "ingested_at": timestamp,
        }
    )

    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Stored source file at {dest}")


if __name__ == "__main__":
    main()
