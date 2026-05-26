"""Merge knowledge-base/tenants/siyu/knowledge.md + inventory.csv into one KB file."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "knowledge-base" / "tenants" / "siyu"
KB = DIR / "knowledge.md"
CSV = DIR / "inventory.csv"
OUT = DIR / "knowledge.md"


def main() -> None:
    text = KB.read_text(encoding="utf-8")
    # Strip old "separate file" section if re-run
    marker = "## Product availability & stock (IMPORTANT)"
    if marker in text:
        text = text.split(marker)[0].rstrip()

    csv_body = CSV.read_text(encoding="utf-8").strip()
    total = max(0, len(csv_body.splitlines()) - 1)

    appendix = f"""
## Product availability & stock (IMPORTANT — authoritative)

**Use only the inventory table below** for stock availability, SKU prices, and order totals. Do not guess.

### How to answer stock / price questions

1. Match **brand**, **product_name**, **color**, and **storage_gb** (when given).
2. Report **stock_qty** and **price_eur** from the matching row(s).
3. If **stock_qty is 0**, say **out of stock** and suggest similar in-stock items if possible.
4. If several rows match, list the best matches (up to 5) and ask the customer to confirm colour/storage.
5. If no match, ask clarifying questions or refer to **+353 85 232 4484** / **sales@siyu.ie**.

### Order totals

Sum **price_eur × quantity** for each line item from the table. Final total is confirmed at checkout. Delivery fee not included unless the shop confirms.

### Inventory table ({total} SKUs, sample generated for demo — verify with shop)

```csv
{csv_body}
```
"""

    rules = """
## Assistant rules

- Be helpful, professional, and concise.
- Do not invent products, prices, or stock not listed in the inventory table above.
- Prefer **refurbished** wording only when the row says Refurbished / Grade A / Grade B.
- For repairs, carrier contracts, or legal advice, refer to the shop.
"""

    OUT.write_text(text + appendix + rules, encoding="utf-8")
    print(f"Wrote merged KB to {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
