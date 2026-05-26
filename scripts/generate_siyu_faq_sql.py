"""Emit SQL to set tenants.faq_text from merged knowledge.md (no-S3 / fallback)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge-base" / "tenants" / "siyu" / "knowledge.md"
OUT = ROOT / "scripts" / "update-siyu-faq-from-kb.sql"


def main() -> None:
    text = KB.read_text(encoding="utf-8")
    OUT.write_text(
        "-- Run on RDS when S3 KB is not enabled. Sets full merged KB (incl. inventory) on faq_text.\n"
        "UPDATE tenants\n"
        "SET faq_text = $faq$\n"
        f"{text}\n"
        "$faq$\n"
        "WHERE slug = 'siyu';\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
