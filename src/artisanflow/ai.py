"""ArtisanFlow AI features — Claude-powered quality grading, pricing, matching, storytelling."""

from __future__ import annotations

import json
import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()

_MODEL = "claude-sonnet-4-20250514"


def _client():
    from anthropic import Anthropic
    return Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))


def _ask(system: str, prompt: str, max_tokens: int = 2048) -> str:
    resp = _client().messages.create(
        model=_MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def _ask_json(system: str, prompt: str) -> dict:
    raw = _ask(system, prompt)
    # Extract JSON from markdown code blocks if present
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0]
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0]
    return json.loads(raw.strip())


# ── AI Features ──────────────────────────────────────────────────────

def grade_product_quality(product_name: str, craft_type: str, description: str, materials: list[str]) -> dict:
    """AI quality/authenticity assessment for a product."""
    system = """You are an expert Oaxacan craft appraiser with 30 years of experience.
Evaluate crafts on authenticity, craftsmanship, materials, finish, and cultural accuracy.
Return JSON with: authenticity_score (1-10), craftsmanship (1-10), materials_quality (1-10),
finish_quality (1-10), cultural_accuracy (1-10), overall_grade (museum/premium/standard/artisan),
notes (string), estimated_value_usd (number)."""

    prompt = f"""Evaluate this Oaxacan craft:
Name: {product_name}
Type: {craft_type}
Description: {description}
Materials: {', '.join(materials)}

Return your assessment as JSON."""

    return _ask_json(system, prompt)


def optimize_pricing(product: dict, market_data: str = "") -> dict:
    """Optimal pricing for different markets."""
    system = """You are a pricing strategist for luxury artisan crafts.
Analyze the product and suggest optimal pricing for different markets.
Return JSON with: recommended_retail_usd, recommended_wholesale_usd,
markets (dict of country -> recommended_price_usd), pricing_rationale (string),
premium_potential (bool), suggested_positioning (string)."""

    prompt = f"""Optimize pricing for this Oaxacan craft:
{json.dumps(product, indent=2, default=str)}

Market context: {market_data or 'General international luxury craft market'}

Return pricing recommendations as JSON."""

    return _ask_json(system, prompt)


def match_buyers(products: list[dict], buyer_preferences: list[str]) -> dict:
    """Match products to buyer preferences."""
    system = """You are a luxury craft matchmaker connecting Oaxacan artisans with global buyers.
Analyze products against buyer preferences and return ranked matches.
Return JSON with: matches (list of {product_id, product_name, match_score (1-10),
match_reasons (list of strings)}), summary (string)."""

    product_summaries = [
        f"- {p['name']} ({p['craft_type']}, ${p['price_usd']}, {p['quality_grade']})"
        for p in products[:20]
    ]

    prompt = f"""Match these products to a buyer:

Products:
{chr(10).join(product_summaries)}

Buyer preferences: {', '.join(buyer_preferences)}

Return matches as JSON."""

    return _ask_json(system, prompt)


def generate_cultural_story(artisan: dict, product: dict) -> dict:
    """Generate marketing story for international buyers."""
    system = """You are a cultural storyteller specializing in Oaxacan art traditions.
Create compelling narratives that honor the artisan's heritage while appealing to
international luxury buyers. Return JSON with: title (string), story_en (string, 150-200 words),
story_es (string, Spanish translation), key_selling_points (list of 3 strings),
cultural_context (string, 50 words about the tradition)."""

    prompt = f"""Create a cultural marketing story:

Artisan: {artisan.get('name')} from {artisan.get('community')}
Bio: {artisan.get('bio')}
Years of experience: {artisan.get('years_experience')}

Product: {product.get('name')}
Description: {product.get('description')}
Craft type: {product.get('craft_type')}
Materials: {', '.join(product.get('materials', []))}
Quality grade: {product.get('quality_grade')}

Return the story as JSON."""

    return _ask_json(system, prompt)


def predict_demand(craft_type: str, season: str = "current") -> dict:
    """Demand forecasting for craft types."""
    system = """You are a market analyst for artisan crafts with deep knowledge of seasonal
trends, tourism patterns, and global luxury market dynamics.
Return JSON with: demand_level (high/medium/low), trend (rising/stable/declining),
peak_months (list), key_markets (list of countries), price_outlook (string),
recommendations (list of 3 strings), confidence (0-1)."""

    prompt = f"""Forecast demand for Oaxacan {craft_type} crafts.
Season: {season}
Consider: tourism patterns, holiday gift seasons, interior design trends,
gallery exhibition calendars, and social media influence.

Return forecast as JSON."""

    return _ask_json(system, prompt)


def optimize_shipping(order: dict, destination_country: str) -> dict:
    """Best carrier/route recommendation."""
    system = """You are a logistics expert specializing in shipping fragile artisan crafts
from Oaxaca, Mexico to international destinations.
Return JSON with: recommended_carrier (dhl/fedex/ups/estafeta),
recommended_method (standard/express/premium_insured), estimated_cost_usd (number),
estimated_days (number), packaging_notes (string), insurance_recommended (bool),
insurance_amount_usd (number), customs_notes (string), route (list of strings)."""

    total = order.get("total_usd", 0)
    products = order.get("product_ids", [])

    prompt = f"""Recommend shipping for this order:
Destination: {destination_country}
Order value: ${total}
Number of items: {len(products)}
Shipping method requested: {order.get('shipping_method', 'standard')}

Consider: fragility of Oaxacan crafts, customs requirements, insurance needs,
and the rainy season in Oaxaca valley (humidity impacts packaging).

Return recommendation as JSON."""

    return _ask_json(system, prompt)


def analyze_marketplace(stats: dict) -> dict:
    """AI analysis of marketplace performance."""
    system = """You are a marketplace analytics expert for artisan e-commerce.
Analyze performance metrics and provide actionable insights.
Return JSON with: health_score (1-10), strengths (list of 3),
weaknesses (list of 3), opportunities (list of 3),
recommendations (list of 5 actionable items), revenue_forecast (string)."""

    prompt = f"""Analyze this artisan marketplace:
{json.dumps(stats, indent=2, default=str)}

Return analysis as JSON."""

    return _ask_json(system, prompt)
