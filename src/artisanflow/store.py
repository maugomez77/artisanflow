"""ArtisanFlow hybrid store.

Postgres JSONB single-blob persistence when DATABASE_URL is set (Render deploy),
JSON file fallback for local dev / CLI. Render free tier has ephemeral disk —
JSON would be wiped on every cold start, so production must use Postgres.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .database import KVStore, SessionLocal, is_db_enabled
from .models import (
    Artisan, Product, Order, Buyer, FulfillmentTask,
    QualityAssessment, ShipmentTracking, SubscriptionBox,
    ArtisanInsight, MarketplaceStats,
)

STORE_DIR = Path.home() / ".artisanflow"
STORE_FILE = STORE_DIR / "store.json"

_KV_KEY = "main"

_COLLECTIONS = [
    "artisans", "products", "orders", "buyers", "fulfillment_tasks",
    "quality_assessments", "shipments", "subscription_boxes", "insights",
]

_MODEL_MAP: dict[str, type] = {
    "artisans": Artisan,
    "products": Product,
    "orders": Order,
    "buyers": Buyer,
    "fulfillment_tasks": FulfillmentTask,
    "quality_assessments": QualityAssessment,
    "shipments": ShipmentTracking,
    "subscription_boxes": SubscriptionBox,
    "insights": ArtisanInsight,
}


def _empty() -> dict:
    return {c: [] for c in _COLLECTIONS}


def _ensure_collections(data: dict) -> dict:
    for c in _COLLECTIONS:
        if c not in data:
            data[c] = []
    return data


def load() -> dict:
    if is_db_enabled():
        with SessionLocal() as s:
            row = s.get(KVStore, _KV_KEY)
            if row and row.value:
                return _ensure_collections({**row.value})
            return _empty()
    if not STORE_FILE.exists():
        return _empty()
    try:
        data = json.loads(STORE_FILE.read_text())
        return _ensure_collections(data)
    except (json.JSONDecodeError, KeyError):
        return _empty()


def save(data: dict) -> None:
    if is_db_enabled():
        # Normalize non-JSON-native types (datetime, etc.) via json round-trip
        # to match the `default=str` behavior of the file path.
        safe = json.loads(json.dumps(data, default=str))
        with SessionLocal() as s:
            row = s.get(KVStore, _KV_KEY)
            if row:
                row.value = safe
            else:
                s.add(KVStore(key=_KV_KEY, value=safe))
            s.commit()
        return
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    STORE_FILE.write_text(json.dumps(data, indent=2, default=str))


def add_item(collection: str, item: Any) -> dict:
    data = load()
    if isinstance(item, dict):
        data[collection].append(item)
    else:
        data[collection].append(item.model_dump())
    save(data)
    return data


def get_items(collection: str) -> list[dict]:
    return load().get(collection, [])


def get_item(collection: str, item_id: str) -> dict | None:
    for item in get_items(collection):
        if item.get("id") == item_id:
            return item
    return None


def update_item(collection: str, item_id: str, updates: dict) -> dict | None:
    data = load()
    for item in data.get(collection, []):
        if item.get("id") == item_id:
            item.update(updates)
            save(data)
            return item
    return None


def delete_item(collection: str, item_id: str) -> bool:
    data = load()
    items = data.get(collection, [])
    before = len(items)
    data[collection] = [i for i in items if i.get("id") != item_id]
    if len(data[collection]) < before:
        save(data)
        return True
    return False


def get_stats() -> MarketplaceStats:
    data = load()
    artisans = data.get("artisans", [])
    products = data.get("products", [])
    orders = data.get("orders", [])

    active_orders = [o for o in orders if o.get("status") in ("pending", "processing", "photographed", "packed", "shipped")]
    delivered = [o for o in orders if o.get("status") == "delivered"]
    total_orders = len(orders)

    revenue = sum(o.get("total_usd", 0) for o in orders)

    craft_counts: dict[str, int] = {}
    for p in products:
        ct = p.get("craft_type", "unknown")
        craft_counts[ct] = craft_counts.get(ct, 0) + 1
    top_crafts = sorted(craft_counts, key=craft_counts.get, reverse=True)[:5]

    market_counts: dict[str, int] = {}
    buyers = data.get("buyers", [])
    for b in buyers:
        c = b.get("country", "unknown")
        market_counts[c] = market_counts.get(c, 0) + 1
    top_markets = sorted(market_counts, key=market_counts.get, reverse=True)[:5]

    success_rate = (len(delivered) / total_orders * 100) if total_orders else 0.0

    return MarketplaceStats(
        total_artisans=len(artisans),
        total_products=len(products),
        active_orders=len(active_orders),
        monthly_revenue_usd=revenue,
        top_crafts=top_crafts,
        top_markets=top_markets,
        fulfillment_success_rate=round(success_rate, 1),
    )
