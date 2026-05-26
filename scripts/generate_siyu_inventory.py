"""Generate sample Siyu inventory CSV (200 rows). Run: python scripts/generate_siyu_inventory.py"""
import csv
import random
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "knowledge-base" / "tenants" / "siyu" / "inventory.csv"

random.seed(42)

phone_models = [
    ("Apple", "iPhone 17", "phone"),
    ("Apple", "iPhone 17 Pro", "phone"),
    ("Apple", "iPhone 17 Pro Max", "phone"),
    ("Apple", "iPhone 16", "phone"),
    ("Apple", "iPhone 15", "phone"),
    ("Apple", "iPhone 14", "phone"),
    ("Samsung", "Galaxy S25", "phone"),
    ("Samsung", "Galaxy S24", "phone"),
    ("Samsung", "Galaxy A55", "phone"),
    ("Samsung", "Galaxy A35", "phone"),
    ("Xiaomi", "Redmi Note 13", "phone"),
    ("Xiaomi", "Poco X6", "phone"),
    ("Google", "Pixel 8", "phone"),
    ("Google", "Pixel 8a", "phone"),
]
watch_models = [
    ("Garett", "Kids Twin 2 4G", "smartwatch"),
    ("Garett", "Atom", "smartwatch"),
    ("Garett", "Verona 2 Glow", "smartwatch"),
    ("Garett", "Rose Gold Solid", "smartwatch"),
    ("Garett", "Classic GT", "smartwatch"),
]
acc_models = [
    ("Spigen", "Ultra Hybrid Case", "case"),
    ("ESR", "MagSafe Case", "case"),
    ("Belkin", "USB-C Cable 2m", "cable"),
    ("Anker", "PowerPort 20W Charger", "charger"),
    ("Apple", "MagSafe Charger", "charger"),
    ("Samsung", "25W Super Fast Charger", "charger"),
    ("Generic", "Tempered Glass Screen Protector", "screen_protector"),
    ("Anker", "Soundcore Buds", "earbuds"),
    ("Apple", "AirPods Pro 2", "earbuds"),
    ("Samsung", "Galaxy Buds FE", "earbuds"),
    ("Generic", "Car Phone Mount", "accessory"),
    ("Belkin", "3-in-1 Wireless Charging Stand", "charger"),
    ("Spigen", "Rugged Armor Case", "case"),
    ("Generic", "Robot Vacuum X500", "vacuum"),
    ("Generic", "Robot Vacuum Pro M7", "vacuum"),
]
colors_phone = [
    "Black", "White", "Silver", "Deep Blue", "Cosmic Orange", "Sage",
    "Lavender", "Mist Blue", "Mint Green", "Navy Blue", "Icy Blue", "Pink",
]
colors_acc = ["Black", "White", "Blue", "Cream", "Clear", "Red", "Green", "Grey"]
conditions = ["New", "Refurbished", "Grade A Refurbished", "Grade B Refurbished"]

rows: list[dict] = []
sku_i = 1000


def add_row(brand, name, category, typ, color, storage, network, condition, features, stock, price):
    global sku_i
    sku_i += 1
    rows.append(
        {
            "sku": f"SYU-{sku_i}",
            "brand": brand,
            "product_name": name,
            "category": category,
            "type": typ,
            "color": color,
            "storage_gb": storage,
            "network": network,
            "condition": condition,
            "features": features,
            "stock_qty": stock,
            "price_eur": f"{price:.2f}",
        }
    )


for brand, base, cat in phone_models:
    for color in random.sample(colors_phone, 4):
        for storage in random.sample(["128", "256", "512"], 2):
            cond = random.choice(conditions)
            base_price = {"Apple": 1100, "Samsung": 900, "Xiaomi": 350, "Google": 650}[brand]
            st_mult = {"128": 1.0, "256": 1.15, "512": 1.35}.get(storage, 1.0)
            mult = 0.92 if "Refurbished" in cond else 1.0
            price = base_price * random.uniform(0.9, 1.1) * st_mult * mult
            stock = random.randint(0, 25)
            feats = "eSIM; Dual SIM" if brand == "Apple" else "Dual SIM; NFC; Fast charge"
            add_row(
                brand, f"{base} {storage}GB", cat, "smartphone", color, storage,
                "5G", cond, feats, stock, price,
            )

for brand, base, cat in watch_models:
    for color in random.sample(["Blue", "Pink", "Black", "Silver", "Rose Gold"], 3):
        price = random.uniform(109, 169)
        stock = random.randint(0, 18)
        feats = "GPS; Heart rate; 4G" if "4G" in base else "Bluetooth; AMOLED; IP68"
        net = "4G" if "4G" in base else "Bluetooth"
        add_row(brand, base, cat, "wearable", color, "N/A", net, "New", feats, stock, price)

while len(rows) < 200:
    brand, name, cat = random.choice(acc_models)
    color = random.choice(colors_acc)
    price = random.uniform(199, 449) if cat == "vacuum" else random.uniform(9.99, 149.99)
    stock = random.randint(0, 40)
    feats = random.choice(
        ["MagSafe compatible", "USB-C PD", "Wireless", "Drop protection", "Noise cancelling", "HEPA filter"]
    )
    add_row(brand, name, cat, cat, color, "N/A", "N/A", "New", feats, stock, price)

rows = rows[:200]
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print(f"Wrote {len(rows)} rows to {OUT}")
