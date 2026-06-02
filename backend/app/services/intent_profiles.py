"""Industry intent templates — extend per tenant via tenants.intent_config_json."""

from __future__ import annotations

from dataclasses import dataclass, field

# Intent keys match ChatIntent.value in intent.py
INTENT_STOCK = "stock_price"
INTENT_MENU = "menu_order"
INTENT_HOURS = "hours_location"
INTENT_CONTACT = "contact"
INTENT_GENERAL = "general"

BASE_KEYWORDS: dict[str, frozenset[str]] = {
    INTENT_STOCK: frozenset(
        {
            "stock",
            "in stock",
            "available",
            "availability",
            "price",
            "cost",
            "how much",
            "€",
            "eur",
            "buy",
            "purchase",
        }
    ),
    INTENT_MENU: frozenset(
        {
            "order",
            "menu",
            "total",
            "bill",
            "delivery",
            "takeaway",
            "take away",
        }
    ),
    INTENT_HOURS: frozenset(
        {
            "hours",
            "open",
            "opening",
            "close",
            "closing",
            "when are you",
            "address",
            "location",
            "where are you",
            "find you",
            "directions",
        }
    ),
    INTENT_CONTACT: frozenset(
        {
            "phone",
            "call",
            "email",
            "contact",
            "speak to",
            "talk to",
            "human",
            "manager",
            "whatsapp",
        }
    ),
}


@dataclass(frozen=True)
class IntentProfile:
    business_type: str
    keywords: dict[str, frozenset[str]] = field(default_factory=dict)


def _merge_keywords(*layers: dict[str, frozenset[str]]) -> dict[str, frozenset[str]]:
    out: dict[str, set[str]] = {}
    for layer in layers:
        for intent, words in layer.items():
            out.setdefault(intent, set()).update(words)
    return {k: frozenset(v) for k, v in out.items()}


RETAIL_ELECTRONICS = IntentProfile(
    business_type="retail_electronics",
    keywords=_merge_keywords(
        BASE_KEYWORDS,
        {
            INTENT_STOCK: frozenset(
                {"gb", "storage", "sku", "iphone", "samsung", "galaxy", "pixel", "refurbished"}
            ),
        },
    ),
)

RESTAURANT = IntentProfile(
    business_type="restaurant",
    keywords=_merge_keywords(
        BASE_KEYWORDS,
        {
            INTENT_MENU: frozenset(
                {
                    "curry",
                    "biryani",
                    "naan",
                    "starter",
                    "dessert",
                    "meal",
                    "set meal",
                    "poppadum",
                    "chips",
                    "tikka",
                    "korma",
                }
            ),
        },
    ),
)

GENERAL_SERVICES = IntentProfile(
    business_type="general",
    keywords=dict(BASE_KEYWORDS),
)

TEMPLATES: dict[str, IntentProfile] = {
    "retail_electronics": RETAIL_ELECTRONICS,
    "retail": RETAIL_ELECTRONICS,
    "restaurant": RESTAURANT,
    "food": RESTAURANT,
    "general": GENERAL_SERVICES,
    "services": GENERAL_SERVICES,
}

SLUG_DEFAULT_BUSINESS_TYPE: dict[str, str] = {
    "siyu": "retail_electronics",
    "india-gate": "restaurant",
    "demo": "general",
}


def resolve_business_type(slug: str, business_type: str | None) -> str:
    bt = (business_type or "").strip().lower()
    if bt and bt in TEMPLATES:
        return bt
    return SLUG_DEFAULT_BUSINESS_TYPE.get(slug, "general")


def get_profile(business_type: str) -> IntentProfile:
    return TEMPLATES.get(business_type, GENERAL_SERVICES)
