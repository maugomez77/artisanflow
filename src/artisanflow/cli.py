"""ArtisanFlow CLI — artisan craft fulfillment and marketplace for Oaxaca."""

from __future__ import annotations

import json
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich import box

from . import store, ai, research, demo_data
from .models import (
    CraftType, Community, QualityGrade, OrderStatus,
    BuyerType, TaskStatus, InsightType,
)

app = typer.Typer(
    name="artisanflow",
    help="Automated artisan craft fulfillment and marketplace for Oaxaca, Mexico",
    no_args_is_help=True,
)
console = Console()

TERRACOTTA = "red3"
ACCENT = "orange1"
EARTH = "wheat1"
CLAY = "dark_orange3"


def _header():
    console.print(Panel(
        "[bold red3]ArtisanFlow[/] [wheat1]- Oaxacan Artisan Marketplace[/]\n"
        "[dim]Connecting master artisans to the world[/]",
        border_style="red3",
        padding=(0, 2),
    ))


# ── Status ───────────────────────────────────────────────────────────

@app.command()
def status():
    """Show marketplace overview and stats."""
    _header()
    s = store.get_stats()

    table = Table(title="Marketplace Status", box=box.ROUNDED, border_style=TERRACOTTA)
    table.add_column("Metric", style="bold")
    table.add_column("Value", style=ACCENT)
    table.add_row("Total Artisans", str(s.total_artisans))
    table.add_row("Total Products", str(s.total_products))
    table.add_row("Active Orders", str(s.active_orders))
    table.add_row("Monthly Revenue", f"${s.monthly_revenue_usd:,.2f}")
    table.add_row("Top Crafts", ", ".join(s.top_crafts) if s.top_crafts else "-")
    table.add_row("Top Markets", ", ".join(s.top_markets) if s.top_markets else "-")
    table.add_row("Fulfillment Rate", f"{s.fulfillment_success_rate}%")
    console.print(table)

    # Weather advisory
    weather = research.get_oaxaca_weather()
    if "error" not in weather:
        advisory = weather.get("packaging_advisory", "")
        temp = weather.get("temperature_c", "?")
        humidity = weather.get("avg_humidity_pct", "?")
        console.print(Panel(
            f"[bold]Oaxaca Weather[/]: {temp}C | Humidity: {humidity}%\n{advisory}",
            border_style="yellow" if "HIGH" in advisory else "green",
            title="Packaging Advisory",
        ))


# ── Artisans ─────────────────────────────────────────────────────────

@app.command()
def artisans(
    craft: Optional[str] = typer.Option(None, help="Filter by craft type"),
    community: Optional[str] = typer.Option(None, help="Filter by community"),
):
    """List artisans."""
    _header()
    items = store.get_items("artisans")
    if craft:
        items = [i for i in items if i.get("craft_type") == craft]
    if community:
        items = [i for i in items if i.get("community") == community]

    table = Table(title=f"Artisans ({len(items)})", box=box.ROUNDED, border_style=TERRACOTTA)
    table.add_column("ID", style="dim")
    table.add_column("Name", style="bold")
    table.add_column("Craft", style=ACCENT)
    table.add_column("Community", style=EARTH)
    table.add_column("Exp", justify="right")
    table.add_column("Rating", justify="right", style="green")
    table.add_column("Specialties")

    for a in items:
        specs = ", ".join(a.get("specialties", [])[:2])
        table.add_row(
            a["id"], a["name"], a["craft_type"],
            a["community"].replace("_", " ").title(),
            f"{a.get('years_experience', 0)}yr",
            f"{a.get('rating', 0):.1f}",
            specs,
        )
    console.print(table)


# ── Products ─────────────────────────────────────────────────────────

@app.command()
def products(
    craft: Optional[str] = typer.Option(None, help="Filter by craft type"),
    grade: Optional[str] = typer.Option(None, help="Filter by quality grade"),
    category: Optional[str] = typer.Option(None, help="Filter by category"),
):
    """List products."""
    _header()
    items = store.get_items("products")
    if craft:
        items = [i for i in items if i.get("craft_type") == craft]
    if grade:
        items = [i for i in items if i.get("quality_grade") == grade]
    if category:
        items = [i for i in items if i.get("category") == category]

    table = Table(title=f"Products ({len(items)})", box=box.ROUNDED, border_style=TERRACOTTA)
    table.add_column("ID", style="dim")
    table.add_column("Name", style="bold", max_width=30)
    table.add_column("Craft", style=ACCENT)
    table.add_column("Grade", style="cyan")
    table.add_column("Price", justify="right", style="green")
    table.add_column("Wholesale", justify="right", style="dim")
    table.add_column("Stock", justify="right")
    table.add_column("Category")

    grade_colors = {"museum": "bold magenta", "premium": "cyan", "standard": "white", "artisan": "dim"}

    for p in items:
        g = p.get("quality_grade", "standard")
        table.add_row(
            p["id"], p["name"], p["craft_type"],
            f"[{grade_colors.get(g, 'white')}]{g}[/]",
            f"${p.get('price_usd', 0):,.0f}",
            f"${p.get('wholesale_price_usd', 0):,.0f}",
            str(p.get("stock_count", 0)),
            p.get("category", ""),
        )
    console.print(table)


# ── Orders ───────────────────────────────────────────────────────────

@app.command()
def orders(
    status_filter: Optional[str] = typer.Option(None, "--status", help="Filter by status"),
):
    """List orders."""
    _header()
    items = store.get_items("orders")
    if status_filter:
        items = [i for i in items if i.get("status") == status_filter]

    table = Table(title=f"Orders ({len(items)})", box=box.ROUNDED, border_style=TERRACOTTA)
    table.add_column("ID", style="dim")
    table.add_column("Buyer", style="bold")
    table.add_column("Items", justify="right")
    table.add_column("Total", justify="right", style="green")
    table.add_column("Status", style=ACCENT)
    table.add_column("Shipping")
    table.add_column("Tracking", style="dim")

    status_colors = {
        "pending": "yellow", "processing": "blue", "photographed": "cyan",
        "packed": "magenta", "shipped": "orange1", "delivered": "green", "returned": "red",
    }

    for o in items:
        buyer = store.get_item("buyers", o.get("buyer_id", ""))
        buyer_name = buyer.get("name", "?") if buyer else "?"
        s = o.get("status", "pending")
        table.add_row(
            o["id"], buyer_name, str(len(o.get("product_ids", []))),
            f"${o.get('total_usd', 0):,.0f}",
            f"[{status_colors.get(s, 'white')}]{s}[/]",
            o.get("shipping_method", ""),
            o.get("tracking_number", "") or "-",
        )
    console.print(table)


# ── Buyers ───────────────────────────────────────────────────────────

@app.command()
def buyers(
    buyer_type: Optional[str] = typer.Option(None, "--type", help="Filter by buyer type"),
):
    """List buyers."""
    _header()
    items = store.get_items("buyers")
    if buyer_type:
        items = [i for i in items if i.get("type") == buyer_type]

    table = Table(title=f"Buyers ({len(items)})", box=box.ROUNDED, border_style=TERRACOTTA)
    table.add_column("ID", style="dim")
    table.add_column("Name", style="bold")
    table.add_column("Type", style=ACCENT)
    table.add_column("Company")
    table.add_column("Country")
    table.add_column("Orders", justify="right")
    table.add_column("Spent", justify="right", style="green")
    table.add_column("Tier", style="cyan")

    for b in items:
        table.add_row(
            b["id"], b["name"], b.get("type", ""),
            b.get("company", "") or "-", b.get("country", ""),
            str(b.get("total_orders", 0)),
            f"${b.get('total_spent_usd', 0):,.0f}",
            b.get("membership_tier", "free"),
        )
    console.print(table)


# ── Fulfillment ──────────────────────────────────────────────────────

@app.command()
def fulfillment(
    status_filter: Optional[str] = typer.Option(None, "--status", help="Filter by status"),
):
    """Show fulfillment pipeline (kanban view)."""
    _header()
    tasks = store.get_items("fulfillment_tasks")
    if status_filter:
        tasks = [t for t in tasks if t.get("status") == status_filter]

    queued = [t for t in tasks if t.get("status") == "queued"]
    in_progress = [t for t in tasks if t.get("status") == "in_progress"]
    completed = [t for t in tasks if t.get("status") == "completed"]

    def _task_card(t: dict) -> str:
        order = store.get_item("orders", t.get("order_id", ""))
        buyer_id = order.get("buyer_id", "") if order else ""
        buyer = store.get_item("buyers", buyer_id)
        buyer_name = buyer.get("name", "?") if buyer else "?"
        return (
            f"[bold]{t.get('task_type', '')}[/] [{ACCENT}]{t['id']}[/]\n"
            f"Order: {t.get('order_id', '')}\n"
            f"Buyer: {buyer_name}\n"
            f"Assigned: {t.get('assigned_to', 'Unassigned')}"
        )

    panels = []
    for label, items, color in [("QUEUED", queued, "yellow"), ("IN PROGRESS", in_progress, "blue"), ("COMPLETED", completed, "green")]:
        content = "\n\n".join(_task_card(t) for t in items) if items else "[dim]Empty[/]"
        panels.append(Panel(content, title=f"{label} ({len(items)})", border_style=color, width=35))

    console.print(Panel("Fulfillment Pipeline", border_style=TERRACOTTA))
    console.print(Columns(panels, equal=True))


# ── Quality ──────────────────────────────────────────────────────────

@app.command()
def quality():
    """Show quality assessments."""
    _header()
    items = store.get_items("quality_assessments")

    table = Table(title=f"Quality Assessments ({len(items)})", box=box.ROUNDED, border_style=TERRACOTTA)
    table.add_column("ID", style="dim")
    table.add_column("Product", style="bold")
    table.add_column("Auth", justify="right")
    table.add_column("Craft", justify="right")
    table.add_column("Material", justify="right")
    table.add_column("Finish", justify="right")
    table.add_column("Cultural", justify="right")
    table.add_column("Grade", style="cyan")
    table.add_column("Inspector")

    for q in items:
        product = store.get_item("products", q.get("product_id", ""))
        pname = product.get("name", "?") if product else "?"
        g = q.get("overall_grade", "standard")
        grade_colors = {"museum": "bold magenta", "premium": "cyan", "standard": "white", "artisan": "dim"}
        table.add_row(
            q["id"], pname[:25],
            f"{q.get('authenticity_score', 0):.1f}",
            f"{q.get('craftsmanship', 0):.1f}",
            f"{q.get('materials_quality', 0):.1f}",
            f"{q.get('finish_quality', 0):.1f}",
            f"{q.get('cultural_accuracy', 0):.1f}",
            f"[{grade_colors.get(g, 'white')}]{g}[/]",
            q.get("inspector", ""),
        )
    console.print(table)


# ── Shipments ────────────────────────────────────────────────────────

@app.command()
def shipments():
    """Track shipments."""
    _header()
    items = store.get_items("shipments")

    table = Table(title=f"Shipments ({len(items)})", box=box.ROUNDED, border_style=TERRACOTTA)
    table.add_column("ID", style="dim")
    table.add_column("Order", style="bold")
    table.add_column("Carrier", style=ACCENT)
    table.add_column("Tracking")
    table.add_column("Destination")
    table.add_column("Status")
    table.add_column("Insurance", justify="right", style="green")
    table.add_column("Events", justify="right")

    status_colors = {"delivered": "green", "in_transit": "yellow", "customs": "orange1", "label_created": "dim"}

    for s in items:
        st = s.get("status", "")
        table.add_row(
            s["id"], s.get("order_id", ""),
            s.get("carrier", "").upper(),
            s.get("tracking_number", ""),
            s.get("destination_country", ""),
            f"[{status_colors.get(st, 'white')}]{st}[/]",
            f"${s.get('insurance_usd', 0):,.0f}",
            str(len(s.get("events", []))),
        )
    console.print(table)


# ── Subscriptions ────────────────────────────────────────────────────

@app.command()
def subscriptions():
    """List subscription boxes."""
    _header()
    items = store.get_items("subscription_boxes")

    table = Table(title=f"Subscription Boxes ({len(items)})", box=box.ROUNDED, border_style=TERRACOTTA)
    table.add_column("ID", style="dim")
    table.add_column("Buyer", style="bold")
    table.add_column("Theme", style=ACCENT)
    table.add_column("Frequency")
    table.add_column("Price", justify="right", style="green")
    table.add_column("Status")
    table.add_column("Next Shipment")

    for s in items:
        buyer = store.get_item("buyers", s.get("buyer_id", ""))
        buyer_name = buyer.get("name", "?") if buyer else "?"
        st = s.get("status", "")
        status_color = {"active": "green", "paused": "yellow", "cancelled": "red"}.get(st, "white")
        table.add_row(
            s["id"], buyer_name, s.get("theme", ""),
            s.get("frequency", ""),
            f"${s.get('price_usd', 0):,.0f}",
            f"[{status_color}]{st}[/]",
            str(s.get("next_shipment_date", "-")),
        )
    console.print(table)


# ── Insights ─────────────────────────────────────────────────────────

@app.command()
def insights():
    """Show AI-generated marketplace insights."""
    _header()
    items = store.get_items("insights")

    for ins in items:
        priority = ins.get("priority", "medium")
        color = {"high": "red", "medium": "yellow", "low": "green"}.get(priority, "white")
        console.print(Panel(
            f"[bold]{ins.get('title', '')}[/]\n\n"
            f"{ins.get('description', '')}\n\n"
            f"[dim]Type: {ins.get('insight_type', '')} | "
            f"Affected artisans: {len(ins.get('affected_artisans', []))}[/]",
            border_style=color,
            title=f"[{color}]{priority.upper()}[/] {ins.get('insight_type', '')}",
        ))


# ── AI Commands ──────────────────────────────────────────────────────

@app.command()
def grade(
    product_id: str = typer.Argument(..., help="Product ID to grade"),
):
    """AI quality grading for a product."""
    _header()
    product = store.get_item("products", product_id)
    if not product:
        console.print(f"[red]Product {product_id} not found[/]")
        raise typer.Exit(1)

    console.print(f"[bold]Grading[/] {product['name']}...")
    with console.status("AI analyzing craft quality..."):
        result = ai.grade_product_quality(
            product["name"], product["craft_type"],
            product.get("description", ""), product.get("materials", []),
        )

    console.print(Panel(
        json.dumps(result, indent=2),
        title=f"Quality Assessment: {product['name']}",
        border_style=TERRACOTTA,
    ))


@app.command()
def match(
    buyer_id: str = typer.Argument(..., help="Buyer ID to match products for"),
):
    """AI buyer-product matching."""
    _header()
    buyer = store.get_item("buyers", buyer_id)
    if not buyer:
        console.print(f"[red]Buyer {buyer_id} not found[/]")
        raise typer.Exit(1)

    console.print(f"[bold]Matching products for[/] {buyer['name']}...")
    products = store.get_items("products")
    with console.status("AI matching preferences..."):
        result = ai.match_buyers(products, buyer.get("preferences", []))

    console.print(Panel(
        json.dumps(result, indent=2),
        title=f"Product Matches: {buyer['name']}",
        border_style=TERRACOTTA,
    ))


@app.command()
def story(
    product_id: str = typer.Argument(..., help="Product ID to generate story for"),
):
    """Generate cultural marketing story for a product."""
    _header()
    product = store.get_item("products", product_id)
    if not product:
        console.print(f"[red]Product {product_id} not found[/]")
        raise typer.Exit(1)

    artisan = store.get_item("artisans", product.get("artisan_id", ""))
    if not artisan:
        console.print(f"[red]Artisan not found for product[/]")
        raise typer.Exit(1)

    console.print(f"[bold]Creating story for[/] {product['name']} by {artisan['name']}...")
    with console.status("AI crafting cultural narrative..."):
        result = ai.generate_cultural_story(artisan, product)

    if "title" in result:
        console.print(Panel(
            f"[bold]{result.get('title', '')}[/]\n\n"
            f"{result.get('story_en', '')}\n\n"
            f"[dim italic]{result.get('story_es', '')}[/]\n\n"
            f"[bold]Key Selling Points:[/]\n" +
            "\n".join(f"  - {p}" for p in result.get("key_selling_points", [])) +
            f"\n\n[bold]Cultural Context:[/] {result.get('cultural_context', '')}",
            title=f"Story: {product['name']}",
            border_style=TERRACOTTA,
        ))
    else:
        console.print(Panel(json.dumps(result, indent=2), border_style=TERRACOTTA))


# ── Demo ─────────────────────────────────────────────────────────────

@app.command()
def demo():
    """Load demo data (20 artisans, 50 products, 15 orders, etc.)."""
    _header()
    with console.status("Seeding demo data..."):
        counts = demo_data.seed()

    table = Table(title="Demo Data Loaded", box=box.ROUNDED, border_style=TERRACOTTA)
    table.add_column("Collection", style="bold")
    table.add_column("Count", justify="right", style=ACCENT)
    for k, v in counts.items():
        table.add_row(k.replace("_", " ").title(), str(v))
    console.print(table)
    console.print("[green]Demo data loaded successfully![/]")


# ── Serve ────────────────────────────────────────────────────────────

@app.command()
def serve(
    port: int = typer.Option(8000, help="Port to serve on"),
    host: str = typer.Option("0.0.0.0", help="Host to bind to"),
):
    """Start the ArtisanFlow API server."""
    _header()
    console.print(f"[bold]Starting API server[/] on {host}:{port}")
    import uvicorn
    uvicorn.run("artisanflow.api:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    app()
