"""Build static FAQ-only knowledge.md for Siyu (inventory stays in inventory.csv)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "knowledge-base" / "tenants" / "siyu"
KB = DIR / "knowledge.md"
CSV = DIR / "inventory.csv"


def strip_merged_inventory_section(text: str) -> str:
    marker = "## Product availability & stock"
    if marker in text:
        text = text.split(marker)[0].rstrip()
    return text


def main() -> None:
    text = KB.read_text(encoding="utf-8")
    text = strip_merged_inventory_section(text)

    stock_note = """
## Product stock and prices

Stock and prices are loaded from the separate inventory file (`inventory.csv` on S3).
For availability questions, the assistant uses live lookup results — do not guess stock or price.
"""

    rules = """
## Assistant rules

- Be helpful, professional, and concise.
- Do not invent products, prices, or stock not returned by inventory lookup.
- For repairs, carrier contracts, or legal advice, refer to the shop.
"""

    KB.write_text(text + stock_note + rules, encoding="utf-8")
    rows = max(0, len(CSV.read_text(encoding="utf-8").strip().splitlines()) - 1)
    print(f"Wrote static FAQ to {KB} ({KB.stat().st_size // 1024} KB)")
    print(f"Keep dynamic inventory in {CSV} ({rows} SKUs)")


if __name__ == "__main__":
    main()
