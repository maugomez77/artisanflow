"""ArtisanFlow FastAPI application."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from . import store, ai, research
from .models import (
    Artisan, Product, Order, Buyer, FulfillmentTask,
    QualityAssessment, ShipmentTracking, SubscriptionBox, ArtisanInsight,
)


async def _load_demo_if_empty():
    """Auto-load demo data if store is empty."""
    try:
        artisans = store.get_items("artisans")
        if not artisans:
            from . import demo_data
            demo_data.seed()
    except Exception:
        pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(_load_demo_if_empty())
    yield


app = FastAPI(
    title="ArtisanFlow API",
    description="Oaxacan artisan craft fulfillment and marketplace platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ───────────────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "artisanflow"}


@app.get("/api/stats")
def stats():
    return store.get_stats().model_dump()


# ── Artisans ─────────────────────────────────────────────────────────

@app.get("/api/artisans")
def list_artisans(craft_type: Optional[str] = None, community: Optional[str] = None):
    items = store.get_items("artisans")
    if craft_type:
        items = [i for i in items if i.get("craft_type") == craft_type]
    if community:
        items = [i for i in items if i.get("community") == community]
    return {"artisans": items, "total": len(items)}


@app.get("/api/artisans/{artisan_id}")
def get_artisan(artisan_id: str):
    item = store.get_item("artisans", artisan_id)
    if not item:
        raise HTTPException(404, "Artisan not found")
    products = [p for p in store.get_items("products") if p.get("artisan_id") == artisan_id]
    return {**item, "products": products}


@app.post("/api/artisans")
def create_artisan(artisan: Artisan):
    store.add_item("artisans", artisan)
    return artisan.model_dump()


@app.put("/api/artisans/{artisan_id}")
def update_artisan(artisan_id: str, updates: dict):
    result = store.update_item("artisans", artisan_id, updates)
    if not result:
        raise HTTPException(404, "Artisan not found")
    return result


# ── Products ─────────────────────────────────────────────────────────

@app.get("/api/products")
def list_products(
    craft_type: Optional[str] = None,
    category: Optional[str] = None,
    quality_grade: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
):
    items = store.get_items("products")
    if craft_type:
        items = [i for i in items if i.get("craft_type") == craft_type]
    if category:
        items = [i for i in items if i.get("category") == category]
    if quality_grade:
        items = [i for i in items if i.get("quality_grade") == quality_grade]
    if min_price is not None:
        items = [i for i in items if i.get("price_usd", 0) >= min_price]
    if max_price is not None:
        items = [i for i in items if i.get("price_usd", 0) <= max_price]
    return {"products": items, "total": len(items)}


@app.get("/api/products/{product_id}")
def get_product(product_id: str):
    item = store.get_item("products", product_id)
    if not item:
        raise HTTPException(404, "Product not found")
    artisan = store.get_item("artisans", item.get("artisan_id", ""))
    assessments = [q for q in store.get_items("quality_assessments") if q.get("product_id") == product_id]
    return {**item, "artisan": artisan, "quality_assessments": assessments}


@app.post("/api/products")
def create_product(product: Product):
    store.add_item("products", product)
    return product.model_dump()


@app.put("/api/products/{product_id}")
def update_product(product_id: str, updates: dict):
    result = store.update_item("products", product_id, updates)
    if not result:
        raise HTTPException(404, "Product not found")
    return result


# ── Orders ───────────────────────────────────────────────────────────

@app.get("/api/orders")
def list_orders(status: Optional[str] = None, buyer_id: Optional[str] = None):
    items = store.get_items("orders")
    if status:
        items = [i for i in items if i.get("status") == status]
    if buyer_id:
        items = [i for i in items if i.get("buyer_id") == buyer_id]
    return {"orders": items, "total": len(items)}


@app.get("/api/orders/{order_id}")
def get_order(order_id: str):
    item = store.get_item("orders", order_id)
    if not item:
        raise HTTPException(404, "Order not found")
    buyer = store.get_item("buyers", item.get("buyer_id", ""))
    tasks = [t for t in store.get_items("fulfillment_tasks") if t.get("order_id") == order_id]
    shipments = [s for s in store.get_items("shipments") if s.get("order_id") == order_id]
    products = [store.get_item("products", pid) for pid in item.get("product_ids", [])]
    return {**item, "buyer": buyer, "tasks": tasks, "shipments": shipments, "products": [p for p in products if p]}


@app.post("/api/orders")
def create_order(order: Order):
    store.add_item("orders", order)
    return order.model_dump()


@app.put("/api/orders/{order_id}")
def update_order(order_id: str, updates: dict):
    result = store.update_item("orders", order_id, updates)
    if not result:
        raise HTTPException(404, "Order not found")
    return result


# ── Buyers ───────────────────────────────────────────────────────────

@app.get("/api/buyers")
def list_buyers(buyer_type: Optional[str] = None, country: Optional[str] = None):
    items = store.get_items("buyers")
    if buyer_type:
        items = [i for i in items if i.get("type") == buyer_type]
    if country:
        items = [i for i in items if i.get("country") == country]
    return {"buyers": items, "total": len(items)}


@app.get("/api/buyers/{buyer_id}")
def get_buyer(buyer_id: str):
    item = store.get_item("buyers", buyer_id)
    if not item:
        raise HTTPException(404, "Buyer not found")
    orders = [o for o in store.get_items("orders") if o.get("buyer_id") == buyer_id]
    subs = [s for s in store.get_items("subscription_boxes") if s.get("buyer_id") == buyer_id]
    return {**item, "orders": orders, "subscriptions": subs}


@app.post("/api/buyers")
def create_buyer(buyer: Buyer):
    store.add_item("buyers", buyer)
    return buyer.model_dump()


# ── Fulfillment ──────────────────────────────────────────────────────

@app.get("/api/fulfillment")
def list_fulfillment(status: Optional[str] = None, task_type: Optional[str] = None):
    items = store.get_items("fulfillment_tasks")
    if status:
        items = [i for i in items if i.get("status") == status]
    if task_type:
        items = [i for i in items if i.get("task_type") == task_type]
    return {"tasks": items, "total": len(items)}


@app.put("/api/fulfillment/{task_id}")
def update_task(task_id: str, updates: dict):
    result = store.update_item("fulfillment_tasks", task_id, updates)
    if not result:
        raise HTTPException(404, "Task not found")
    return result


@app.get("/api/fulfillment/pipeline")
def fulfillment_pipeline():
    """Kanban-style pipeline view."""
    tasks = store.get_items("fulfillment_tasks")
    pipeline = {"queued": [], "in_progress": [], "completed": []}
    for t in tasks:
        status = t.get("status", "queued")
        if status in pipeline:
            pipeline[status].append(t)
    return pipeline


# ── Quality ──────────────────────────────────────────────────────────

@app.get("/api/quality")
def list_quality():
    return {"assessments": store.get_items("quality_assessments")}


@app.get("/api/quality/{assessment_id}")
def get_quality(assessment_id: str):
    item = store.get_item("quality_assessments", assessment_id)
    if not item:
        raise HTTPException(404, "Assessment not found")
    product = store.get_item("products", item.get("product_id", ""))
    return {**item, "product": product}


@app.post("/api/quality")
def create_quality(assessment: QualityAssessment):
    store.add_item("quality_assessments", assessment)
    return assessment.model_dump()


# ── Shipments ────────────────────────────────────────────────────────

@app.get("/api/shipments")
def list_shipments(status: Optional[str] = None, carrier: Optional[str] = None):
    items = store.get_items("shipments")
    if status:
        items = [i for i in items if i.get("status") == status]
    if carrier:
        items = [i for i in items if i.get("carrier") == carrier]
    return {"shipments": items, "total": len(items)}


@app.get("/api/shipments/{shipment_id}")
def get_shipment(shipment_id: str):
    item = store.get_item("shipments", shipment_id)
    if not item:
        raise HTTPException(404, "Shipment not found")
    order = store.get_item("orders", item.get("order_id", ""))
    return {**item, "order": order}


# ── Subscriptions ────────────────────────────────────────────────────

@app.get("/api/subscriptions")
def list_subscriptions(status: Optional[str] = None):
    items = store.get_items("subscription_boxes")
    if status:
        items = [i for i in items if i.get("status") == status]
    return {"subscriptions": items, "total": len(items)}


@app.put("/api/subscriptions/{sub_id}")
def update_subscription(sub_id: str, updates: dict):
    result = store.update_item("subscription_boxes", sub_id, updates)
    if not result:
        raise HTTPException(404, "Subscription not found")
    return result


# ── Insights ─────────────────────────────────────────────────────────

@app.get("/api/insights")
def list_insights(insight_type: Optional[str] = None, priority: Optional[str] = None):
    items = store.get_items("insights")
    if insight_type:
        items = [i for i in items if i.get("insight_type") == insight_type]
    if priority:
        items = [i for i in items if i.get("priority") == priority]
    return {"insights": items, "total": len(items)}


# ── AI Endpoints ─────────────────────────────────────────────────────

@app.post("/api/ai/grade")
def ai_grade(body: dict):
    """AI quality grading for a product."""
    return ai.grade_product_quality(
        product_name=body.get("name", ""),
        craft_type=body.get("craft_type", ""),
        description=body.get("description", ""),
        materials=body.get("materials", []),
    )


@app.post("/api/ai/pricing")
def ai_pricing(body: dict):
    """AI pricing optimization."""
    product_id = body.get("product_id", "")
    product = store.get_item("products", product_id) or body
    return ai.optimize_pricing(product)


@app.post("/api/ai/match")
def ai_match(body: dict):
    """AI buyer-product matching."""
    buyer_id = body.get("buyer_id", "")
    buyer = store.get_item("buyers", buyer_id)
    preferences = buyer.get("preferences", []) if buyer else body.get("preferences", [])
    products = store.get_items("products")
    return ai.match_buyers(products, preferences)


@app.post("/api/ai/story")
def ai_story(body: dict):
    """Generate cultural marketing story."""
    product_id = body.get("product_id", "")
    product = store.get_item("products", product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    artisan = store.get_item("artisans", product.get("artisan_id", ""))
    if not artisan:
        raise HTTPException(404, "Artisan not found")
    return ai.generate_cultural_story(artisan, product)


@app.post("/api/ai/demand")
def ai_demand(body: dict):
    """AI demand forecasting."""
    return ai.predict_demand(body.get("craft_type", "alebrije"), body.get("season", "current"))


@app.post("/api/ai/shipping")
def ai_shipping(body: dict):
    """AI shipping optimization."""
    order_id = body.get("order_id", "")
    order = store.get_item("orders", order_id) or body
    return ai.optimize_shipping(order, body.get("destination_country", "US"))


# ── Research Endpoints ───────────────────────────────────────────────

@app.get("/api/research/market")
def research_market(q: str = Query(...)):
    return {"results": research.search_market(q)}


@app.get("/api/research/weather")
def research_weather():
    return research.get_oaxaca_weather()


@app.get("/api/research/fairs")
def research_fairs():
    return {"results": research.search_artisan_fairs()}


@app.get("/api/research/prices/{craft_type}")
def research_prices(craft_type: str):
    return {"results": research.search_craft_prices(craft_type)}
