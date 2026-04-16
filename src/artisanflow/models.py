"""ArtisanFlow data models."""

from __future__ import annotations

from datetime import datetime, date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
import uuid


def _uid() -> str:
    return uuid.uuid4().hex[:12]


# ── Enums ────────────────────────────────────────────────────────────

class CraftType(str, Enum):
    ALEBRIJE = "alebrije"
    BARRO_NEGRO = "barro_negro"
    TEXTILE = "textile"
    WOOD_CARVING = "wood_carving"
    LEATHER = "leather"
    JEWELRY = "jewelry"
    CANDLE = "candle"
    MEZCAL_CRAFT = "mezcal_craft"


class Community(str, Enum):
    ARRAZOLA = "arrazola"
    SAN_BARTOLO_COYOTEPEC = "san_bartolo_coyotepec"
    TEOTITLAN_DEL_VALLE = "teotitlan_del_valle"
    SAN_MARTIN_TILCAJETE = "san_martin_tilcajete"
    OCOTLAN = "ocotlan"
    SANTA_MARIA_ATZOMPA = "santa_maria_atzompa"


class QualityGrade(str, Enum):
    MUSEUM = "museum"
    PREMIUM = "premium"
    STANDARD = "standard"
    ARTISAN = "artisan"


class ProductCategory(str, Enum):
    HOME_DECOR = "home_decor"
    WEARABLE = "wearable"
    COLLECTIBLE = "collectible"
    FUNCTIONAL = "functional"
    CEREMONIAL = "ceremonial"


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PHOTOGRAPHED = "photographed"
    PACKED = "packed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    RETURNED = "returned"


class ShippingMethod(str, Enum):
    STANDARD = "standard"
    EXPRESS = "express"
    PREMIUM_INSURED = "premium_insured"


class BuyerType(str, Enum):
    INTERIOR_DESIGNER = "interior_designer"
    LUXURY_RETAILER = "luxury_retailer"
    COLLECTOR = "collector"
    GALLERY = "gallery"
    HOTEL_CHAIN = "hotel_chain"
    CORPORATE = "corporate"
    INDIVIDUAL = "individual"


class MembershipTier(str, Enum):
    FREE = "free"
    PROFESSIONAL = "professional"
    PREMIUM = "premium"


class TaskType(str, Enum):
    PHOTOGRAPH = "photograph"
    QUALITY_CHECK = "quality_check"
    PACK = "pack"
    LABEL = "label"
    SHIP = "ship"


class TaskStatus(str, Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Carrier(str, Enum):
    DHL = "dhl"
    FEDEX = "fedex"
    UPS = "ups"
    ESTAFETA = "estafeta"


class BoxTheme(str, Enum):
    HOME_DECOR = "home_decor"
    TEXTILE = "textile"
    POTTERY = "pottery"
    MIXED = "mixed"
    SEASONAL = "seasonal"


class BoxFrequency(str, Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"


class BoxStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class InsightType(str, Enum):
    SALES_TREND = "sales_trend"
    PRICING = "pricing"
    DEMAND = "demand"
    SHIPPING = "shipping"
    QUALITY = "quality"


# ── Models ───────────────────────────────────────────────────────────

class Artisan(BaseModel):
    id: str = Field(default_factory=_uid)
    name: str
    craft_type: CraftType
    community: Community
    contact: str = ""
    bio: str = ""
    years_experience: int = 0
    specialties: list[str] = Field(default_factory=list)
    photos: list[str] = Field(default_factory=list)
    rating: float = 5.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Product(BaseModel):
    id: str = Field(default_factory=_uid)
    artisan_id: str
    name: str
    description: str = ""
    craft_type: CraftType
    materials: list[str] = Field(default_factory=list)
    dimensions_cm: dict = Field(default_factory=dict)
    weight_kg: float = 0.0
    price_usd: float
    wholesale_price_usd: float = 0.0
    photos: list[str] = Field(default_factory=list)
    quality_grade: QualityGrade = QualityGrade.STANDARD
    stock_count: int = 1
    category: ProductCategory = ProductCategory.HOME_DECOR
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Order(BaseModel):
    id: str = Field(default_factory=_uid)
    product_ids: list[str] = Field(default_factory=list)
    buyer_id: str
    status: OrderStatus = OrderStatus.PENDING
    total_usd: float = 0.0
    shipping_method: ShippingMethod = ShippingMethod.STANDARD
    tracking_number: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None


class Buyer(BaseModel):
    id: str = Field(default_factory=_uid)
    name: str
    type: BuyerType = BuyerType.INDIVIDUAL
    company: str = ""
    country: str = "US"
    email: str = ""
    total_orders: int = 0
    total_spent_usd: float = 0.0
    membership_tier: MembershipTier = MembershipTier.FREE
    preferences: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class FulfillmentTask(BaseModel):
    id: str = Field(default_factory=_uid)
    order_id: str
    task_type: TaskType
    status: TaskStatus = TaskStatus.QUEUED
    assigned_to: str = ""
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class QualityAssessment(BaseModel):
    id: str = Field(default_factory=_uid)
    product_id: str
    inspector: str = ""
    authenticity_score: float = 0.0
    craftsmanship: float = 0.0
    materials_quality: float = 0.0
    finish_quality: float = 0.0
    cultural_accuracy: float = 0.0
    overall_grade: QualityGrade = QualityGrade.STANDARD
    photos: list[str] = Field(default_factory=list)
    notes: str = ""
    assessed_at: datetime = Field(default_factory=datetime.utcnow)


class ShipmentTracking(BaseModel):
    id: str = Field(default_factory=_uid)
    order_id: str
    carrier: Carrier = Carrier.DHL
    tracking_number: str = ""
    origin: str = "oaxaca"
    destination_country: str = ""
    status: str = "label_created"
    temperature_sensitive: bool = False
    insurance_usd: float = 0.0
    events: list[dict] = Field(default_factory=list)


class SubscriptionBox(BaseModel):
    id: str = Field(default_factory=_uid)
    buyer_id: str
    theme: BoxTheme = BoxTheme.MIXED
    frequency: BoxFrequency = BoxFrequency.MONTHLY
    price_usd: float = 149.0
    status: BoxStatus = BoxStatus.ACTIVE
    next_shipment_date: Optional[date] = None


class ArtisanInsight(BaseModel):
    id: str = Field(default_factory=_uid)
    insight_type: InsightType
    title: str
    description: str = ""
    priority: str = "medium"
    affected_artisans: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MarketplaceStats(BaseModel):
    total_artisans: int = 0
    total_products: int = 0
    active_orders: int = 0
    monthly_revenue_usd: float = 0.0
    top_crafts: list[str] = Field(default_factory=list)
    top_markets: list[str] = Field(default_factory=list)
    fulfillment_success_rate: float = 0.0
