"""ArtisanFlow demo data — realistic Oaxacan artisan marketplace dataset."""

from __future__ import annotations

from datetime import datetime, date, timedelta
from . import store
from .models import (
    Artisan, Product, Order, Buyer, FulfillmentTask,
    QualityAssessment, ShipmentTracking, SubscriptionBox, ArtisanInsight,
    CraftType, Community, QualityGrade, ProductCategory, OrderStatus,
    ShippingMethod, BuyerType, MembershipTier, TaskType, TaskStatus,
    Carrier, BoxTheme, BoxFrequency, BoxStatus, InsightType,
)

_now = datetime.utcnow()
_day = timedelta(days=1)


def seed() -> dict[str, int]:
    """Seed store with demo data. Returns counts per collection."""
    data = store._empty()

    # ── 20 Artisans ──────────────────────────────────────────────────
    artisans = [
        Artisan(id="art-001", name="Jacobo Angeles", craft_type=CraftType.ALEBRIJE, community=Community.SAN_MARTIN_TILCAJETE, bio="Third-generation alebrije master. Known for intricate dot patterns and mythological creatures.", years_experience=35, specialties=["large alebrijes", "dot painting", "mythological figures"], rating=5.0),
        Artisan(id="art-002", name="Maria Jimenez", craft_type=CraftType.ALEBRIJE, community=Community.ARRAZOLA, bio="Pioneered fusion of traditional Zapotec symbols with contemporary design.", years_experience=22, specialties=["small alebrijes", "Zapotec symbols", "color theory"], rating=4.9),
        Artisan(id="art-003", name="Dona Rosa Real", craft_type=CraftType.BARRO_NEGRO, community=Community.SAN_BARTOLO_COYOTEPEC, bio="Keeper of the ancestral barro negro polishing technique. UNESCO heritage practitioner.", years_experience=45, specialties=["large vessels", "mirror polish", "ceremonial pieces"], rating=5.0),
        Artisan(id="art-004", name="Valente Nieto", craft_type=CraftType.BARRO_NEGRO, community=Community.SAN_BARTOLO_COYOTEPEC, bio="Innovator in barro negro — combines traditional firing with modern sculptural forms.", years_experience=18, specialties=["sculptures", "functional ware", "modern forms"], rating=4.7),
        Artisan(id="art-005", name="Porfirio Gutierrez", craft_type=CraftType.TEXTILE, community=Community.TEOTITLAN_DEL_VALLE, bio="Natural dye master using cochineal, indigo, and marigold. Exhibited at Smithsonian.", years_experience=30, specialties=["natural dyes", "large tapestries", "cochineal red"], rating=5.0),
        Artisan(id="art-006", name="Juana Martinez", craft_type=CraftType.TEXTILE, community=Community.TEOTITLAN_DEL_VALLE, bio="Backstrap loom weaver creating contemporary patterns rooted in Mixtec tradition.", years_experience=25, specialties=["backstrap loom", "Mixtec patterns", "table runners"], rating=4.8),
        Artisan(id="art-007", name="Manuel Jimenez Jr", craft_type=CraftType.WOOD_CARVING, community=Community.ARRAZOLA, bio="Son of the father of alebrijes. Carries forward the carving legacy with bold innovation.", years_experience=28, specialties=["copal wood", "large sculptures", "animal forms"], rating=4.9),
        Artisan(id="art-008", name="Inocencio Vasquez", craft_type=CraftType.WOOD_CARVING, community=Community.SAN_MARTIN_TILCAJETE, bio="Miniature specialist — creates impossibly detailed carvings under 5cm.", years_experience=20, specialties=["miniatures", "fine detail", "insects"], rating=4.6),
        Artisan(id="art-009", name="Guillermina Aguilar", craft_type=CraftType.JEWELRY, community=Community.OCOTLAN, bio="Silver filigree artisan from Ocotlan. Combines Zapotec motifs with modern wearability.", years_experience=15, specialties=["silver filigree", "Zapotec motifs", "earrings"], rating=4.8),
        Artisan(id="art-010", name="Dolores Porras", craft_type=CraftType.BARRO_NEGRO, community=Community.SANTA_MARIA_ATZOMPA, bio="Green-glazed pottery master from Atzompa. Known for whimsical animal figures.", years_experience=40, specialties=["green glaze", "animal figures", "mezcal cups"], rating=4.9),
        Artisan(id="art-011", name="Abigail Mendoza", craft_type=CraftType.TEXTILE, community=Community.TEOTITLAN_DEL_VALLE, bio="Creates museum-quality tapestries depicting Zapotec cosmology.", years_experience=32, specialties=["cosmological tapestries", "wall hangings", "natural dyes"], rating=5.0),
        Artisan(id="art-012", name="Pedro Linares Jr", craft_type=CraftType.ALEBRIJE, community=Community.SAN_MARTIN_TILCAJETE, bio="Fantasy creatures with surrealist influence. Each piece tells a dream narrative.", years_experience=19, specialties=["surrealist forms", "narrative pieces", "large installations"], rating=4.5),
        Artisan(id="art-013", name="Rufina Ruiz", craft_type=CraftType.LEATHER, community=Community.OCOTLAN, bio="Hand-tooled leather artisan making bags and belts with pre-Hispanic motifs.", years_experience=12, specialties=["tooled leather", "bags", "belts"], rating=4.4),
        Artisan(id="art-014", name="Santiago Ramirez", craft_type=CraftType.CANDLE, community=Community.OCOTLAN, bio="Beeswax candle maker using traditional Oaxacan techniques and copal resin scents.", years_experience=8, specialties=["beeswax", "copal scented", "ceremonial candles"], rating=4.3),
        Artisan(id="art-015", name="Enrique Flores", craft_type=CraftType.MEZCAL_CRAFT, community=Community.OCOTLAN, bio="Creates hand-blown mezcal copitas and jicara vessels for artisanal mezcal.", years_experience=16, specialties=["copitas", "jicaras", "serving sets"], rating=4.6),
        Artisan(id="art-016", name="Catalina Cruz", craft_type=CraftType.TEXTILE, community=Community.TEOTITLAN_DEL_VALLE, bio="Specialist in rebozos using pre-Hispanic ikat technique.", years_experience=27, specialties=["rebozos", "ikat", "silk blend"], rating=4.7),
        Artisan(id="art-017", name="Miguel Angel Vasquez", craft_type=CraftType.ALEBRIJE, community=Community.ARRAZOLA, bio="Known for enormous alebrijes that have been featured in Mexico City's alebrije parade.", years_experience=24, specialties=["monumental pieces", "parade floats", "neon colors"], rating=4.8),
        Artisan(id="art-018", name="Rosa Hernandez", craft_type=CraftType.BARRO_NEGRO, community=Community.SAN_BARTOLO_COYOTEPEC, bio="Delicate barro negro jewelry and ornaments with filigree-like clay work.", years_experience=14, specialties=["clay jewelry", "ornaments", "delicate work"], rating=4.5),
        Artisan(id="art-019", name="Francisco Toledo Jr", craft_type=CraftType.WOOD_CARVING, community=Community.SAN_MARTIN_TILCAJETE, bio="Artistic carvings inspired by his father's graphic art legacy.", years_experience=17, specialties=["artistic carvings", "graphic influence", "collector pieces"], rating=4.7),
        Artisan(id="art-020", name="Elena Mateos", craft_type=CraftType.JEWELRY, community=Community.OCOTLAN, bio="Gold and silver artisan combining pre-Hispanic casting with modern minimalism.", years_experience=10, specialties=["lost-wax casting", "minimalist design", "gold work"], rating=4.6),
    ]

    # ── 50 Products ──────────────────────────────────────────────────
    products = [
        # Alebrijes ($50-$2000)
        Product(id="prod-001", artisan_id="art-001", name="Jaguar Guardian", description="60cm hand-carved copal wood jaguar with 10,000+ hand-painted dots in Zapotec patterns.", craft_type=CraftType.ALEBRIJE, materials=["copal wood", "natural pigments", "aniline dyes"], dimensions_cm={"l": 60, "w": 25, "h": 40}, weight_kg=2.8, price_usd=1800.0, wholesale_price_usd=1100.0, quality_grade=QualityGrade.MUSEUM, stock_count=1, category=ProductCategory.COLLECTIBLE),
        Product(id="prod-002", artisan_id="art-001", name="Quetzalcoatl Serpent", description="Feathered serpent alebrije with iridescent wing detail.", craft_type=CraftType.ALEBRIJE, materials=["copal wood", "aniline dyes"], dimensions_cm={"l": 45, "w": 15, "h": 30}, weight_kg=1.5, price_usd=950.0, wholesale_price_usd=580.0, quality_grade=QualityGrade.PREMIUM, stock_count=2, category=ProductCategory.COLLECTIBLE),
        Product(id="prod-003", artisan_id="art-002", name="Owl of Wisdom", description="Small owl alebrije with Zapotec calendar glyphs.", craft_type=CraftType.ALEBRIJE, materials=["copal wood", "natural pigments"], dimensions_cm={"l": 12, "w": 8, "h": 15}, weight_kg=0.3, price_usd=120.0, wholesale_price_usd=72.0, quality_grade=QualityGrade.PREMIUM, stock_count=8, category=ProductCategory.HOME_DECOR),
        Product(id="prod-004", artisan_id="art-002", name="Hummingbird Set", description="Set of 3 hummingbird alebrijes in graduating sizes.", craft_type=CraftType.ALEBRIJE, materials=["copal wood", "aniline dyes"], dimensions_cm={"l": 10, "w": 5, "h": 8}, weight_kg=0.4, price_usd=180.0, wholesale_price_usd=108.0, quality_grade=QualityGrade.STANDARD, stock_count=5, category=ProductCategory.HOME_DECOR),
        Product(id="prod-005", artisan_id="art-012", name="Dream Coyote", description="Surrealist coyote with melting clock motifs. Limited edition.", craft_type=CraftType.ALEBRIJE, materials=["copal wood", "acrylic", "gold leaf"], dimensions_cm={"l": 35, "w": 12, "h": 25}, weight_kg=1.2, price_usd=650.0, wholesale_price_usd=400.0, quality_grade=QualityGrade.PREMIUM, stock_count=3, category=ProductCategory.COLLECTIBLE),
        Product(id="prod-006", artisan_id="art-017", name="Monumental Dragon", description="1-meter alebrije dragon. Parade-worthy centerpiece.", craft_type=CraftType.ALEBRIJE, materials=["copal wood", "wire frame", "aniline dyes"], dimensions_cm={"l": 100, "w": 40, "h": 60}, weight_kg=8.5, price_usd=2000.0, wholesale_price_usd=1200.0, quality_grade=QualityGrade.MUSEUM, stock_count=1, category=ProductCategory.COLLECTIBLE),
        Product(id="prod-007", artisan_id="art-017", name="Mini Alebrije Cat", description="Pocket-sized alebrije cat with neon geometric patterns.", craft_type=CraftType.ALEBRIJE, materials=["copal wood", "aniline dyes"], dimensions_cm={"l": 6, "w": 3, "h": 5}, weight_kg=0.1, price_usd=50.0, wholesale_price_usd=30.0, quality_grade=QualityGrade.ARTISAN, stock_count=20, category=ProductCategory.HOME_DECOR),
        Product(id="prod-008", artisan_id="art-007", name="Eagle Warrior", description="Carved eagle warrior in copal wood. Traditional Aztec motif.", craft_type=CraftType.WOOD_CARVING, materials=["copal wood", "natural pigments"], dimensions_cm={"l": 30, "w": 20, "h": 45}, weight_kg=2.0, price_usd=450.0, wholesale_price_usd=270.0, quality_grade=QualityGrade.PREMIUM, stock_count=2, category=ProductCategory.COLLECTIBLE),

        # Barro Negro ($30-$500)
        Product(id="prod-009", artisan_id="art-003", name="Ceremonial Vessel", description="Large barro negro vessel with mirror-polish finish. Ancestral technique.", craft_type=CraftType.BARRO_NEGRO, materials=["black clay", "quartz polish"], dimensions_cm={"l": 30, "w": 30, "h": 45}, weight_kg=4.5, price_usd=500.0, wholesale_price_usd=300.0, quality_grade=QualityGrade.MUSEUM, stock_count=1, category=ProductCategory.CEREMONIAL),
        Product(id="prod-010", artisan_id="art-003", name="Barro Negro Olla", description="Traditional cooking pot with ritual markings.", craft_type=CraftType.BARRO_NEGRO, materials=["black clay"], dimensions_cm={"l": 25, "w": 25, "h": 20}, weight_kg=2.8, price_usd=180.0, wholesale_price_usd=108.0, quality_grade=QualityGrade.PREMIUM, stock_count=4, category=ProductCategory.FUNCTIONAL),
        Product(id="prod-011", artisan_id="art-004", name="Modern Skull", description="Contemporary calavera sculpture in polished barro negro.", craft_type=CraftType.BARRO_NEGRO, materials=["black clay", "quartz polish"], dimensions_cm={"l": 15, "w": 12, "h": 18}, weight_kg=1.2, price_usd=95.0, wholesale_price_usd=57.0, quality_grade=QualityGrade.STANDARD, stock_count=10, category=ProductCategory.HOME_DECOR),
        Product(id="prod-012", artisan_id="art-004", name="Geometric Vase Set", description="Set of 3 minimalist barro negro vases.", craft_type=CraftType.BARRO_NEGRO, materials=["black clay"], dimensions_cm={"l": 10, "w": 10, "h": 25}, weight_kg=2.0, price_usd=150.0, wholesale_price_usd=90.0, quality_grade=QualityGrade.STANDARD, stock_count=6, category=ProductCategory.HOME_DECOR),
        Product(id="prod-013", artisan_id="art-010", name="Green Glaze Mezcal Set", description="6 copitas with iguana motif in Atzompa green glaze.", craft_type=CraftType.BARRO_NEGRO, materials=["clay", "lead-free green glaze"], dimensions_cm={"l": 8, "w": 8, "h": 6}, weight_kg=1.5, price_usd=85.0, wholesale_price_usd=50.0, quality_grade=QualityGrade.STANDARD, stock_count=12, category=ProductCategory.FUNCTIONAL),
        Product(id="prod-014", artisan_id="art-010", name="Whimsical Cat", description="Green-glazed cat with flower crown. Signature Dolores Porras style.", craft_type=CraftType.BARRO_NEGRO, materials=["clay", "lead-free green glaze"], dimensions_cm={"l": 20, "w": 12, "h": 25}, weight_kg=1.8, price_usd=120.0, wholesale_price_usd=72.0, quality_grade=QualityGrade.PREMIUM, stock_count=4, category=ProductCategory.HOME_DECOR),
        Product(id="prod-015", artisan_id="art-018", name="Clay Filigree Earrings", description="Barro negro earrings with filigree-like clay detail.", craft_type=CraftType.BARRO_NEGRO, materials=["black clay", "silver hooks"], dimensions_cm={"l": 2, "w": 1, "h": 5}, weight_kg=0.02, price_usd=35.0, wholesale_price_usd=20.0, quality_grade=QualityGrade.STANDARD, stock_count=25, category=ProductCategory.WEARABLE),
        Product(id="prod-016", artisan_id="art-018", name="Barro Negro Pendant", description="Round pendant with etched Zapotec glyph.", craft_type=CraftType.BARRO_NEGRO, materials=["black clay", "leather cord"], dimensions_cm={"l": 3, "w": 3, "h": 0.5}, weight_kg=0.03, price_usd=30.0, wholesale_price_usd=18.0, quality_grade=QualityGrade.ARTISAN, stock_count=30, category=ProductCategory.WEARABLE),

        # Textiles ($100-$3000)
        Product(id="prod-017", artisan_id="art-005", name="Cochineal Tapestry Grande", description="2m x 3m wall tapestry dyed with cochineal, indigo, and marigold. Museum quality.", craft_type=CraftType.TEXTILE, materials=["wool", "cochineal", "indigo", "marigold"], dimensions_cm={"l": 300, "w": 200, "h": 1}, weight_kg=5.0, price_usd=3000.0, wholesale_price_usd=1800.0, quality_grade=QualityGrade.MUSEUM, stock_count=1, category=ProductCategory.HOME_DECOR),
        Product(id="prod-018", artisan_id="art-005", name="Zapotec Diamond Rug", description="1.5m x 2m floor rug with traditional diamond pattern in natural dyes.", craft_type=CraftType.TEXTILE, materials=["wool", "natural dyes"], dimensions_cm={"l": 200, "w": 150, "h": 1}, weight_kg=3.5, price_usd=1200.0, wholesale_price_usd=720.0, quality_grade=QualityGrade.PREMIUM, stock_count=2, category=ProductCategory.HOME_DECOR),
        Product(id="prod-019", artisan_id="art-006", name="Mixtec Table Runner", description="Backstrap loom table runner with Mixtec codex-inspired patterns.", craft_type=CraftType.TEXTILE, materials=["cotton", "natural dyes"], dimensions_cm={"l": 180, "w": 35, "h": 0.5}, weight_kg=0.4, price_usd=180.0, wholesale_price_usd=108.0, quality_grade=QualityGrade.PREMIUM, stock_count=6, category=ProductCategory.HOME_DECOR),
        Product(id="prod-020", artisan_id="art-006", name="Woven Cushion Covers", description="Set of 4 cushion covers in earth tones.", craft_type=CraftType.TEXTILE, materials=["cotton", "wool blend"], dimensions_cm={"l": 45, "w": 45, "h": 1}, weight_kg=0.8, price_usd=220.0, wholesale_price_usd=132.0, quality_grade=QualityGrade.STANDARD, stock_count=8, category=ProductCategory.HOME_DECOR),
        Product(id="prod-021", artisan_id="art-011", name="Cosmological Wall Hanging", description="Depicts the Zapotec creation myth. 3 months to weave.", craft_type=CraftType.TEXTILE, materials=["wool", "cochineal", "indigo", "gold thread"], dimensions_cm={"l": 250, "w": 180, "h": 1}, weight_kg=4.5, price_usd=2800.0, wholesale_price_usd=1680.0, quality_grade=QualityGrade.MUSEUM, stock_count=1, category=ProductCategory.COLLECTIBLE),
        Product(id="prod-022", artisan_id="art-016", name="Silk Rebozo", description="Hand-woven rebozo in ikat technique with silk and cotton.", craft_type=CraftType.TEXTILE, materials=["silk", "cotton", "natural dyes"], dimensions_cm={"l": 220, "w": 70, "h": 0.3}, weight_kg=0.3, price_usd=450.0, wholesale_price_usd=270.0, quality_grade=QualityGrade.PREMIUM, stock_count=3, category=ProductCategory.WEARABLE),
        Product(id="prod-023", artisan_id="art-016", name="Cotton Table Runner Set", description="Pair of matching ikat runners in indigo/cream.", craft_type=CraftType.TEXTILE, materials=["cotton", "indigo"], dimensions_cm={"l": 150, "w": 30, "h": 0.5}, weight_kg=0.5, price_usd=160.0, wholesale_price_usd=96.0, quality_grade=QualityGrade.STANDARD, stock_count=10, category=ProductCategory.HOME_DECOR),
        Product(id="prod-024", artisan_id="art-011", name="Zapotec Pillow Collection", description="Set of 6 pillows with different glyph motifs.", craft_type=CraftType.TEXTILE, materials=["wool", "cotton", "natural dyes"], dimensions_cm={"l": 50, "w": 50, "h": 10}, weight_kg=3.0, price_usd=540.0, wholesale_price_usd=324.0, quality_grade=QualityGrade.PREMIUM, stock_count=2, category=ProductCategory.HOME_DECOR),

        # Wood Carvings ($25-$800)
        Product(id="prod-025", artisan_id="art-007", name="Copal Nahual Set", description="Set of 5 Nahual spirit animals in natural finish.", craft_type=CraftType.WOOD_CARVING, materials=["copal wood"], dimensions_cm={"l": 15, "w": 8, "h": 20}, weight_kg=1.5, price_usd=350.0, wholesale_price_usd=210.0, quality_grade=QualityGrade.PREMIUM, stock_count=3, category=ProductCategory.COLLECTIBLE),
        Product(id="prod-026", artisan_id="art-008", name="Miniature Insect Collection", description="12 carved insects under 3cm each. Incredible detail.", craft_type=CraftType.WOOD_CARVING, materials=["copal wood", "natural pigments"], dimensions_cm={"l": 3, "w": 2, "h": 2}, weight_kg=0.2, price_usd=280.0, wholesale_price_usd=168.0, quality_grade=QualityGrade.PREMIUM, stock_count=4, category=ProductCategory.COLLECTIBLE),
        Product(id="prod-027", artisan_id="art-008", name="Micro Alebrije Frog", description="2cm frog with full dot pattern. Magnifying glass recommended.", craft_type=CraftType.WOOD_CARVING, materials=["copal wood", "aniline dyes"], dimensions_cm={"l": 2, "w": 1.5, "h": 1.5}, weight_kg=0.01, price_usd=45.0, wholesale_price_usd=27.0, quality_grade=QualityGrade.STANDARD, stock_count=15, category=ProductCategory.COLLECTIBLE),
        Product(id="prod-028", artisan_id="art-019", name="Graphic Jaguar Panel", description="Flat carved panel with bold graphic jaguar. Gallery ready.", craft_type=CraftType.WOOD_CARVING, materials=["cedar", "ink", "lacquer"], dimensions_cm={"l": 60, "w": 40, "h": 3}, weight_kg=2.5, price_usd=800.0, wholesale_price_usd=480.0, quality_grade=QualityGrade.MUSEUM, stock_count=1, category=ProductCategory.COLLECTIBLE),
        Product(id="prod-029", artisan_id="art-019", name="Carved Letter Opener", description="Functional letter opener with lizard handle.", craft_type=CraftType.WOOD_CARVING, materials=["copal wood", "natural pigments"], dimensions_cm={"l": 25, "w": 3, "h": 2}, weight_kg=0.1, price_usd=25.0, wholesale_price_usd=15.0, quality_grade=QualityGrade.ARTISAN, stock_count=30, category=ProductCategory.FUNCTIONAL),
        Product(id="prod-030", artisan_id="art-007", name="Tree of Life", description="Traditional Oaxacan tree of life with 20 animal figures.", craft_type=CraftType.WOOD_CARVING, materials=["copal wood", "aniline dyes", "wire"], dimensions_cm={"l": 40, "w": 30, "h": 50}, weight_kg=3.0, price_usd=680.0, wholesale_price_usd=408.0, quality_grade=QualityGrade.PREMIUM, stock_count=2, category=ProductCategory.HOME_DECOR),

        # Jewelry
        Product(id="prod-031", artisan_id="art-009", name="Filigree Chandelier Earrings", description="Sterling silver filigree earrings with Zapotec rain god motif.", craft_type=CraftType.JEWELRY, materials=["sterling silver"], dimensions_cm={"l": 2, "w": 2, "h": 7}, weight_kg=0.02, price_usd=95.0, wholesale_price_usd=57.0, quality_grade=QualityGrade.PREMIUM, stock_count=10, category=ProductCategory.WEARABLE),
        Product(id="prod-032", artisan_id="art-009", name="Silver Cuff Bracelet", description="Wide cuff with hammered texture and glyph engraving.", craft_type=CraftType.JEWELRY, materials=["sterling silver"], dimensions_cm={"l": 6, "w": 4, "h": 6}, weight_kg=0.05, price_usd=180.0, wholesale_price_usd=108.0, quality_grade=QualityGrade.PREMIUM, stock_count=5, category=ProductCategory.WEARABLE),
        Product(id="prod-033", artisan_id="art-020", name="Gold Quetzal Pendant", description="14k gold pendant using lost-wax casting. Quetzal bird design.", craft_type=CraftType.JEWELRY, materials=["14k gold"], dimensions_cm={"l": 3, "w": 2, "h": 0.5}, weight_kg=0.01, price_usd=650.0, wholesale_price_usd=390.0, quality_grade=QualityGrade.MUSEUM, stock_count=2, category=ProductCategory.WEARABLE),
        Product(id="prod-034", artisan_id="art-020", name="Minimalist Silver Ring Set", description="Stack of 3 thin silver rings with micro-etched patterns.", craft_type=CraftType.JEWELRY, materials=["sterling silver"], dimensions_cm={"l": 2, "w": 2, "h": 0.5}, weight_kg=0.01, price_usd=75.0, wholesale_price_usd=45.0, quality_grade=QualityGrade.STANDARD, stock_count=20, category=ProductCategory.WEARABLE),

        # Leather
        Product(id="prod-035", artisan_id="art-013", name="Tooled Leather Tote", description="Large tote bag with Monte Alban relief pattern.", craft_type=CraftType.LEATHER, materials=["vegetable-tanned leather"], dimensions_cm={"l": 40, "w": 15, "h": 35}, weight_kg=1.0, price_usd=320.0, wholesale_price_usd=192.0, quality_grade=QualityGrade.PREMIUM, stock_count=4, category=ProductCategory.WEARABLE),
        Product(id="prod-036", artisan_id="art-013", name="Leather Belt - Jaguar", description="Hand-tooled belt with running jaguar motif.", craft_type=CraftType.LEATHER, materials=["vegetable-tanned leather", "brass buckle"], dimensions_cm={"l": 110, "w": 4, "h": 0.5}, weight_kg=0.3, price_usd=85.0, wholesale_price_usd=50.0, quality_grade=QualityGrade.STANDARD, stock_count=8, category=ProductCategory.WEARABLE),

        # Candles
        Product(id="prod-037", artisan_id="art-014", name="Copal Beeswax Candle Set", description="6 beeswax candles infused with copal resin. Traditional Oaxacan scent.", craft_type=CraftType.CANDLE, materials=["beeswax", "copal resin", "cotton wick"], dimensions_cm={"l": 5, "w": 5, "h": 15}, weight_kg=1.2, price_usd=65.0, wholesale_price_usd=39.0, quality_grade=QualityGrade.STANDARD, stock_count=15, category=ProductCategory.HOME_DECOR),
        Product(id="prod-038", artisan_id="art-014", name="Ceremonial Candle - Dia de Muertos", description="Large decorated candle for Day of the Dead altars.", craft_type=CraftType.CANDLE, materials=["beeswax", "marigold essence", "natural pigments"], dimensions_cm={"l": 10, "w": 10, "h": 30}, weight_kg=1.5, price_usd=45.0, wholesale_price_usd=27.0, quality_grade=QualityGrade.STANDARD, stock_count=20, category=ProductCategory.CEREMONIAL),

        # Mezcal Craft
        Product(id="prod-039", artisan_id="art-015", name="Artisan Copita Set", description="Set of 4 hand-blown glass copitas for mezcal tasting.", craft_type=CraftType.MEZCAL_CRAFT, materials=["hand-blown glass"], dimensions_cm={"l": 5, "w": 5, "h": 8}, weight_kg=0.4, price_usd=60.0, wholesale_price_usd=36.0, quality_grade=QualityGrade.STANDARD, stock_count=12, category=ProductCategory.FUNCTIONAL),
        Product(id="prod-040", artisan_id="art-015", name="Jicara Serving Bowl", description="Traditional jicara gourd bowl for mezcal service.", craft_type=CraftType.MEZCAL_CRAFT, materials=["jicara gourd", "natural lacquer"], dimensions_cm={"l": 15, "w": 15, "h": 8}, weight_kg=0.2, price_usd=40.0, wholesale_price_usd=24.0, quality_grade=QualityGrade.ARTISAN, stock_count=8, category=ProductCategory.FUNCTIONAL),

        # More products to reach 50
        Product(id="prod-041", artisan_id="art-001", name="Butterfly Spirit", description="Medium alebrije butterfly with gold accents.", craft_type=CraftType.ALEBRIJE, materials=["copal wood", "aniline dyes", "gold leaf"], dimensions_cm={"l": 20, "w": 25, "h": 15}, weight_kg=0.6, price_usd=380.0, wholesale_price_usd=228.0, quality_grade=QualityGrade.PREMIUM, stock_count=3, category=ProductCategory.HOME_DECOR),
        Product(id="prod-042", artisan_id="art-003", name="Barro Negro Candelabra", description="Five-arm candelabra in mirror-polish barro negro.", craft_type=CraftType.BARRO_NEGRO, materials=["black clay", "quartz polish"], dimensions_cm={"l": 30, "w": 30, "h": 35}, weight_kg=3.5, price_usd=350.0, wholesale_price_usd=210.0, quality_grade=QualityGrade.PREMIUM, stock_count=2, category=ProductCategory.HOME_DECOR),
        Product(id="prod-043", artisan_id="art-005", name="Indigo Meditation Rug", description="Small meditation mat in deep indigo with central mandala.", craft_type=CraftType.TEXTILE, materials=["wool", "indigo"], dimensions_cm={"l": 100, "w": 100, "h": 1}, weight_kg=1.5, price_usd=380.0, wholesale_price_usd=228.0, quality_grade=QualityGrade.PREMIUM, stock_count=4, category=ProductCategory.HOME_DECOR),
        Product(id="prod-044", artisan_id="art-009", name="Filigree Statement Necklace", description="Elaborate silver filigree collar necklace.", craft_type=CraftType.JEWELRY, materials=["sterling silver", "turquoise"], dimensions_cm={"l": 20, "w": 15, "h": 2}, weight_kg=0.08, price_usd=420.0, wholesale_price_usd=252.0, quality_grade=QualityGrade.MUSEUM, stock_count=1, category=ProductCategory.WEARABLE),
        Product(id="prod-045", artisan_id="art-012", name="Flying Fish Alebrije", description="Psychedelic flying fish with mandala patterns.", craft_type=CraftType.ALEBRIJE, materials=["copal wood", "aniline dyes"], dimensions_cm={"l": 25, "w": 10, "h": 20}, weight_kg=0.8, price_usd=280.0, wholesale_price_usd=168.0, quality_grade=QualityGrade.STANDARD, stock_count=5, category=ProductCategory.HOME_DECOR),
        Product(id="prod-046", artisan_id="art-004", name="Barro Negro Mezcal Set", description="Decanter + 4 cups in matte barro negro.", craft_type=CraftType.BARRO_NEGRO, materials=["black clay"], dimensions_cm={"l": 15, "w": 15, "h": 25}, weight_kg=2.5, price_usd=145.0, wholesale_price_usd=87.0, quality_grade=QualityGrade.STANDARD, stock_count=7, category=ProductCategory.FUNCTIONAL),
        Product(id="prod-047", artisan_id="art-006", name="Mixtec Shawl", description="Large shawl with codex-inspired border pattern.", craft_type=CraftType.TEXTILE, materials=["wool", "natural dyes"], dimensions_cm={"l": 200, "w": 80, "h": 0.5}, weight_kg=0.6, price_usd=280.0, wholesale_price_usd=168.0, quality_grade=QualityGrade.PREMIUM, stock_count=3, category=ProductCategory.WEARABLE),
        Product(id="prod-048", artisan_id="art-013", name="Leather Journal", description="Hand-tooled leather journal with Monte Alban cover.", craft_type=CraftType.LEATHER, materials=["vegetable-tanned leather", "handmade paper"], dimensions_cm={"l": 15, "w": 2, "h": 20}, weight_kg=0.4, price_usd=55.0, wholesale_price_usd=33.0, quality_grade=QualityGrade.STANDARD, stock_count=12, category=ProductCategory.FUNCTIONAL),
        Product(id="prod-049", artisan_id="art-015", name="Mezcal Tasting Flight Board", description="Wooden board with 5 copita holders and agave carving.", craft_type=CraftType.MEZCAL_CRAFT, materials=["parota wood", "hand-blown glass"], dimensions_cm={"l": 40, "w": 12, "h": 5}, weight_kg=1.0, price_usd=95.0, wholesale_price_usd=57.0, quality_grade=QualityGrade.PREMIUM, stock_count=6, category=ProductCategory.FUNCTIONAL),
        Product(id="prod-050", artisan_id="art-014", name="Marigold Pillar Candle", description="Large pillar candle with embedded dried marigolds.", craft_type=CraftType.CANDLE, materials=["beeswax", "dried marigolds", "cotton wick"], dimensions_cm={"l": 8, "w": 8, "h": 20}, weight_kg=0.8, price_usd=35.0, wholesale_price_usd=21.0, quality_grade=QualityGrade.ARTISAN, stock_count=25, category=ProductCategory.HOME_DECOR),
    ]

    # ── 8 Buyers ─────────────────────────────────────────────────────
    buyers = [
        Buyer(id="buy-001", name="Sarah Chen", type=BuyerType.INTERIOR_DESIGNER, company="Chen Interiors", country="US", email="sarah@cheninteriors.com", total_orders=12, total_spent_usd=18500.0, membership_tier=MembershipTier.PREMIUM, preferences=["textiles", "barro_negro", "large pieces"]),
        Buyer(id="buy-002", name="Galerie Rive Gauche", type=BuyerType.GALLERY, company="Galerie Rive Gauche", country="FR", email="contact@galerierivegauche.fr", total_orders=8, total_spent_usd=24000.0, membership_tier=MembershipTier.PREMIUM, preferences=["museum grade", "alebrijes", "collectible"]),
        Buyer(id="buy-003", name="Takeshi Yamamoto", type=BuyerType.COLLECTOR, company="", country="JP", email="takeshi@artcollect.jp", total_orders=5, total_spent_usd=9800.0, membership_tier=MembershipTier.PROFESSIONAL, preferences=["alebrijes", "wood_carving", "miniatures"]),
        Buyer(id="buy-004", name="Four Seasons Oaxaca", type=BuyerType.HOTEL_CHAIN, company="Four Seasons Hotels", country="MX", email="procurement@fourseasons.com", total_orders=3, total_spent_usd=35000.0, membership_tier=MembershipTier.PREMIUM, preferences=["textiles", "barro_negro", "bulk orders"]),
        Buyer(id="buy-005", name="Martha Rodriguez", type=BuyerType.LUXURY_RETAILER, company="Maison Oaxaca", country="US", email="martha@maisonoaxaca.com", total_orders=15, total_spent_usd=42000.0, membership_tier=MembershipTier.PREMIUM, preferences=["all crafts", "premium", "wholesale"]),
        Buyer(id="buy-006", name="Klaus Weber", type=BuyerType.COLLECTOR, company="", country="DE", email="klaus.weber@web.de", total_orders=4, total_spent_usd=6200.0, membership_tier=MembershipTier.PROFESSIONAL, preferences=["barro_negro", "ceremonial", "museum grade"]),
        Buyer(id="buy-007", name="Anthropologie Buying", type=BuyerType.CORPORATE, company="Anthropologie", country="US", email="buying@anthropologie.com", total_orders=2, total_spent_usd=28000.0, membership_tier=MembershipTier.PREMIUM, preferences=["home_decor", "textiles", "candles", "wholesale"]),
        Buyer(id="buy-008", name="Emma Thompson", type=BuyerType.INDIVIDUAL, company="", country="GB", email="emma.t@gmail.com", total_orders=2, total_spent_usd=850.0, membership_tier=MembershipTier.FREE, preferences=["jewelry", "small alebrijes"]),
    ]

    # ── 15 Orders ────────────────────────────────────────────────────
    orders = [
        Order(id="ord-001", product_ids=["prod-001", "prod-017"], buyer_id="buy-002", status=OrderStatus.DELIVERED, total_usd=4800.0, shipping_method=ShippingMethod.PREMIUM_INSURED, tracking_number="DHL-OAX-78234", created_at=_now - 30 * _day, shipped_at=_now - 25 * _day, delivered_at=_now - 18 * _day),
        Order(id="ord-002", product_ids=["prod-009", "prod-042"], buyer_id="buy-006", status=OrderStatus.DELIVERED, total_usd=850.0, shipping_method=ShippingMethod.PREMIUM_INSURED, tracking_number="DHL-OAX-78290", created_at=_now - 28 * _day, shipped_at=_now - 23 * _day, delivered_at=_now - 16 * _day),
        Order(id="ord-003", product_ids=["prod-018", "prod-019", "prod-020"], buyer_id="buy-001", status=OrderStatus.DELIVERED, total_usd=1600.0, shipping_method=ShippingMethod.EXPRESS, tracking_number="FDX-OAX-45123", created_at=_now - 25 * _day, shipped_at=_now - 21 * _day, delivered_at=_now - 14 * _day),
        Order(id="ord-004", product_ids=["prod-003", "prod-004", "prod-007"], buyer_id="buy-008", status=OrderStatus.DELIVERED, total_usd=350.0, shipping_method=ShippingMethod.STANDARD, tracking_number="FDX-OAX-45200", created_at=_now - 22 * _day, shipped_at=_now - 18 * _day, delivered_at=_now - 10 * _day),
        Order(id="ord-005", product_ids=["prod-031", "prod-032", "prod-033"], buyer_id="buy-008", status=OrderStatus.SHIPPED, total_usd=925.0, shipping_method=ShippingMethod.EXPRESS, tracking_number="DHL-OAX-78401", created_at=_now - 10 * _day, shipped_at=_now - 7 * _day),
        Order(id="ord-006", product_ids=["prod-006"], buyer_id="buy-002", status=OrderStatus.SHIPPED, total_usd=2000.0, shipping_method=ShippingMethod.PREMIUM_INSURED, tracking_number="DHL-OAX-78455", created_at=_now - 8 * _day, shipped_at=_now - 5 * _day),
        Order(id="ord-007", product_ids=["prod-021", "prod-024"], buyer_id="buy-004", status=OrderStatus.PACKED, total_usd=3340.0, shipping_method=ShippingMethod.PREMIUM_INSURED, created_at=_now - 5 * _day),
        Order(id="ord-008", product_ids=["prod-025", "prod-026", "prod-028"], buyer_id="buy-003", status=OrderStatus.PHOTOGRAPHED, total_usd=1430.0, shipping_method=ShippingMethod.EXPRESS, created_at=_now - 4 * _day),
        Order(id="ord-009", product_ids=["prod-035", "prod-036", "prod-048"], buyer_id="buy-005", status=OrderStatus.PROCESSING, total_usd=460.0, shipping_method=ShippingMethod.STANDARD, created_at=_now - 3 * _day),
        Order(id="ord-010", product_ids=["prod-037", "prod-038", "prod-050"], buyer_id="buy-001", status=OrderStatus.PROCESSING, total_usd=145.0, shipping_method=ShippingMethod.STANDARD, created_at=_now - 2 * _day),
        Order(id="ord-011", product_ids=["prod-022", "prod-047"], buyer_id="buy-005", status=OrderStatus.PENDING, total_usd=730.0, shipping_method=ShippingMethod.EXPRESS, created_at=_now - 1 * _day),
        Order(id="ord-012", product_ids=["prod-011", "prod-012", "prod-013", "prod-046"], buyer_id="buy-007", status=OrderStatus.PENDING, total_usd=475.0, shipping_method=ShippingMethod.STANDARD, created_at=_now - 1 * _day),
        Order(id="ord-013", product_ids=["prod-005", "prod-045"], buyer_id="buy-003", status=OrderStatus.PENDING, total_usd=930.0, shipping_method=ShippingMethod.PREMIUM_INSURED, created_at=_now),
        Order(id="ord-014", product_ids=["prod-039", "prod-040", "prod-049"], buyer_id="buy-001", status=OrderStatus.PENDING, total_usd=195.0, shipping_method=ShippingMethod.STANDARD, created_at=_now),
        Order(id="ord-015", product_ids=["prod-002", "prod-041"], buyer_id="buy-005", status=OrderStatus.PENDING, total_usd=1330.0, shipping_method=ShippingMethod.EXPRESS, created_at=_now),
    ]

    # ── 10 Fulfillment Tasks ─────────────────────────────────────────
    tasks = [
        FulfillmentTask(id="task-001", order_id="ord-007", task_type=TaskType.PHOTOGRAPH, status=TaskStatus.COMPLETED, assigned_to="Carlos M.", started_at=_now - 4 * _day, completed_at=_now - 3 * _day),
        FulfillmentTask(id="task-002", order_id="ord-007", task_type=TaskType.QUALITY_CHECK, status=TaskStatus.COMPLETED, assigned_to="Ana L.", started_at=_now - 3 * _day, completed_at=_now - 2 * _day),
        FulfillmentTask(id="task-003", order_id="ord-007", task_type=TaskType.PACK, status=TaskStatus.COMPLETED, assigned_to="Roberto S.", started_at=_now - 2 * _day, completed_at=_now - 1 * _day),
        FulfillmentTask(id="task-004", order_id="ord-007", task_type=TaskType.LABEL, status=TaskStatus.IN_PROGRESS, assigned_to="Carlos M.", started_at=_now),
        FulfillmentTask(id="task-005", order_id="ord-008", task_type=TaskType.PHOTOGRAPH, status=TaskStatus.COMPLETED, assigned_to="Carlos M.", started_at=_now - 3 * _day, completed_at=_now - 2 * _day),
        FulfillmentTask(id="task-006", order_id="ord-008", task_type=TaskType.QUALITY_CHECK, status=TaskStatus.IN_PROGRESS, assigned_to="Ana L.", started_at=_now - 1 * _day),
        FulfillmentTask(id="task-007", order_id="ord-009", task_type=TaskType.PHOTOGRAPH, status=TaskStatus.QUEUED, assigned_to="Carlos M."),
        FulfillmentTask(id="task-008", order_id="ord-010", task_type=TaskType.PHOTOGRAPH, status=TaskStatus.QUEUED),
        FulfillmentTask(id="task-009", order_id="ord-011", task_type=TaskType.PHOTOGRAPH, status=TaskStatus.QUEUED),
        FulfillmentTask(id="task-010", order_id="ord-012", task_type=TaskType.PHOTOGRAPH, status=TaskStatus.QUEUED),
    ]

    # ── 12 Quality Assessments ───────────────────────────────────────
    assessments = [
        QualityAssessment(id="qa-001", product_id="prod-001", inspector="Ana L.", authenticity_score=10.0, craftsmanship=10.0, materials_quality=9.5, finish_quality=10.0, cultural_accuracy=10.0, overall_grade=QualityGrade.MUSEUM, notes="Exceptional. Jacobo Angeles masterwork. Museum acquisition quality."),
        QualityAssessment(id="qa-002", product_id="prod-009", inspector="Ana L.", authenticity_score=10.0, craftsmanship=9.5, materials_quality=9.0, finish_quality=10.0, cultural_accuracy=10.0, overall_grade=QualityGrade.MUSEUM, notes="Dona Rosa tradition at its finest. Perfect mirror polish."),
        QualityAssessment(id="qa-003", product_id="prod-017", inspector="Ana L.", authenticity_score=10.0, craftsmanship=10.0, materials_quality=10.0, finish_quality=9.5, cultural_accuracy=10.0, overall_grade=QualityGrade.MUSEUM, notes="Porfirio Gutierrez cochineal mastery. Smithsonian level."),
        QualityAssessment(id="qa-004", product_id="prod-003", inspector="Roberto S.", authenticity_score=9.0, craftsmanship=8.5, materials_quality=8.0, finish_quality=8.5, cultural_accuracy=9.0, overall_grade=QualityGrade.PREMIUM, notes="Beautiful Zapotec glyphs. Consistent paint application."),
        QualityAssessment(id="qa-005", product_id="prod-011", inspector="Roberto S.", authenticity_score=7.0, craftsmanship=7.5, materials_quality=7.0, finish_quality=7.0, cultural_accuracy=7.5, overall_grade=QualityGrade.STANDARD, notes="Good contemporary piece. Polish could be deeper."),
        QualityAssessment(id="qa-006", product_id="prod-019", inspector="Ana L.", authenticity_score=9.5, craftsmanship=9.0, materials_quality=8.5, finish_quality=9.0, cultural_accuracy=9.5, overall_grade=QualityGrade.PREMIUM, notes="Excellent backstrap loom work. Codex patterns accurately rendered."),
        QualityAssessment(id="qa-007", product_id="prod-025", inspector="Ana L.", authenticity_score=9.0, craftsmanship=9.0, materials_quality=8.5, finish_quality=8.5, cultural_accuracy=9.0, overall_grade=QualityGrade.PREMIUM, notes="Traditional Nahual forms well executed."),
        QualityAssessment(id="qa-008", product_id="prod-031", inspector="Roberto S.", authenticity_score=9.5, craftsmanship=9.0, materials_quality=9.0, finish_quality=9.0, cultural_accuracy=9.0, overall_grade=QualityGrade.PREMIUM, notes="Delicate filigree. Rain god motif historically accurate."),
        QualityAssessment(id="qa-009", product_id="prod-035", inspector="Roberto S.", authenticity_score=8.0, craftsmanship=8.5, materials_quality=9.0, finish_quality=8.0, cultural_accuracy=8.0, overall_grade=QualityGrade.PREMIUM, notes="Excellent leather quality. Monte Alban relief clean and deep."),
        QualityAssessment(id="qa-010", product_id="prod-006", inspector="Ana L.", authenticity_score=10.0, craftsmanship=9.5, materials_quality=9.0, finish_quality=9.5, cultural_accuracy=9.0, overall_grade=QualityGrade.MUSEUM, notes="Monumental piece. Gallery/museum centerpiece quality."),
        QualityAssessment(id="qa-011", product_id="prod-028", inspector="Ana L.", authenticity_score=9.5, craftsmanship=10.0, materials_quality=9.0, finish_quality=9.5, cultural_accuracy=8.5, overall_grade=QualityGrade.MUSEUM, notes="Graphic style is unique. Gallery-ready."),
        QualityAssessment(id="qa-012", product_id="prod-021", inspector="Ana L.", authenticity_score=10.0, craftsmanship=10.0, materials_quality=10.0, finish_quality=10.0, cultural_accuracy=10.0, overall_grade=QualityGrade.MUSEUM, notes="Perfect 50/50. Zapotec cosmology tapestry. 3-month labor of love."),
    ]

    # ── 6 Shipments ──────────────────────────────────────────────────
    shipments = [
        ShipmentTracking(id="ship-001", order_id="ord-001", carrier=Carrier.DHL, tracking_number="DHL-OAX-78234", destination_country="FR", status="delivered", insurance_usd=500.0, events=[
            {"date": str(_now - 25 * _day), "status": "picked_up", "location": "Oaxaca Hub"},
            {"date": str(_now - 23 * _day), "status": "in_transit", "location": "Mexico City"},
            {"date": str(_now - 21 * _day), "status": "customs", "location": "CDG Paris"},
            {"date": str(_now - 18 * _day), "status": "delivered", "location": "Paris, France"},
        ]),
        ShipmentTracking(id="ship-002", order_id="ord-002", carrier=Carrier.DHL, tracking_number="DHL-OAX-78290", destination_country="DE", status="delivered", insurance_usd=200.0, events=[
            {"date": str(_now - 23 * _day), "status": "picked_up", "location": "Oaxaca Hub"},
            {"date": str(_now - 20 * _day), "status": "in_transit", "location": "Mexico City"},
            {"date": str(_now - 17 * _day), "status": "customs", "location": "Frankfurt"},
            {"date": str(_now - 16 * _day), "status": "delivered", "location": "Berlin, Germany"},
        ]),
        ShipmentTracking(id="ship-003", order_id="ord-003", carrier=Carrier.FEDEX, tracking_number="FDX-OAX-45123", destination_country="US", status="delivered", insurance_usd=150.0, events=[
            {"date": str(_now - 21 * _day), "status": "picked_up", "location": "Oaxaca Hub"},
            {"date": str(_now - 19 * _day), "status": "in_transit", "location": "Mexico City"},
            {"date": str(_now - 16 * _day), "status": "customs", "location": "Laredo, TX"},
            {"date": str(_now - 14 * _day), "status": "delivered", "location": "San Francisco, CA"},
        ]),
        ShipmentTracking(id="ship-004", order_id="ord-005", carrier=Carrier.DHL, tracking_number="DHL-OAX-78401", destination_country="GB", status="in_transit", insurance_usd=100.0, events=[
            {"date": str(_now - 7 * _day), "status": "picked_up", "location": "Oaxaca Hub"},
            {"date": str(_now - 5 * _day), "status": "in_transit", "location": "Mexico City"},
            {"date": str(_now - 3 * _day), "status": "in_transit", "location": "Miami Hub"},
            {"date": str(_now - 1 * _day), "status": "customs", "location": "Heathrow, London"},
        ]),
        ShipmentTracking(id="ship-005", order_id="ord-006", carrier=Carrier.DHL, tracking_number="DHL-OAX-78455", destination_country="FR", status="in_transit", temperature_sensitive=True, insurance_usd=800.0, events=[
            {"date": str(_now - 5 * _day), "status": "picked_up", "location": "Oaxaca Hub"},
            {"date": str(_now - 3 * _day), "status": "in_transit", "location": "Mexico City"},
            {"date": str(_now - 1 * _day), "status": "in_transit", "location": "Miami Hub"},
        ]),
        ShipmentTracking(id="ship-006", order_id="ord-004", carrier=Carrier.FEDEX, tracking_number="FDX-OAX-45200", destination_country="GB", status="delivered", insurance_usd=50.0, events=[
            {"date": str(_now - 18 * _day), "status": "picked_up", "location": "Oaxaca Hub"},
            {"date": str(_now - 15 * _day), "status": "in_transit", "location": "Mexico City"},
            {"date": str(_now - 12 * _day), "status": "customs", "location": "Heathrow, London"},
            {"date": str(_now - 10 * _day), "status": "delivered", "location": "London, UK"},
        ]),
    ]

    # ── 4 Subscription Boxes ─────────────────────────────────────────
    subs = [
        SubscriptionBox(id="sub-001", buyer_id="buy-001", theme=BoxTheme.HOME_DECOR, frequency=BoxFrequency.MONTHLY, price_usd=199.0, status=BoxStatus.ACTIVE, next_shipment_date=date(2026, 4, 15)),
        SubscriptionBox(id="sub-002", buyer_id="buy-005", theme=BoxTheme.MIXED, frequency=BoxFrequency.MONTHLY, price_usd=299.0, status=BoxStatus.ACTIVE, next_shipment_date=date(2026, 4, 10)),
        SubscriptionBox(id="sub-003", buyer_id="buy-008", theme=BoxTheme.POTTERY, frequency=BoxFrequency.QUARTERLY, price_usd=149.0, status=BoxStatus.ACTIVE, next_shipment_date=date(2026, 6, 1)),
        SubscriptionBox(id="sub-004", buyer_id="buy-003", theme=BoxTheme.MIXED, frequency=BoxFrequency.QUARTERLY, price_usd=349.0, status=BoxStatus.PAUSED, next_shipment_date=date(2026, 7, 1)),
    ]

    # ── 6 AI Insights ────────────────────────────────────────────────
    insights = [
        ArtisanInsight(id="ins-001", insight_type=InsightType.SALES_TREND, title="Alebrije demand surging in Japan", description="Japanese collector market showing 40% YoY growth. Miniatures and museum-grade pieces most sought after. Recommend increasing inventory from Tilcajete workshops.", priority="high", affected_artisans=["art-001", "art-002", "art-008", "art-012"]),
        ArtisanInsight(id="ins-002", insight_type=InsightType.PRICING, title="Textiles underpriced for EU market", description="Comparable Peruvian textiles sell 25-35% higher in European galleries. Cochineal-dyed pieces from Porfirio Gutierrez especially undervalued.", priority="high", affected_artisans=["art-005", "art-011"]),
        ArtisanInsight(id="ins-003", insight_type=InsightType.DEMAND, title="Hotel sector bulk orders incoming", description="3 luxury hotel chains planning Oaxaca-themed room renovations. Combined potential: $120K in textiles and pottery.", priority="high", affected_artisans=["art-005", "art-006", "art-010", "art-011", "art-016"]),
        ArtisanInsight(id="ins-004", insight_type=InsightType.SHIPPING, title="Rainy season packaging advisory", description="Humidity levels rising in Oaxaca valley. Barro negro and textiles need extra moisture protection for next 3 months.", priority="medium", affected_artisans=["art-003", "art-004", "art-005", "art-006"]),
        ArtisanInsight(id="ins-005", insight_type=InsightType.QUALITY, title="New copal wood sourcing needed", description="Primary copal wood supplier reporting lower quality this season. Recommend quality checks on all new wood carvings.", priority="medium", affected_artisans=["art-001", "art-002", "art-007", "art-008", "art-012", "art-017", "art-019"]),
        ArtisanInsight(id="ins-006", insight_type=InsightType.SALES_TREND, title="Mezcal craft accessories trending", description="Instagram #mezcalculture driving 60% increase in copita and jicara searches. Stock up on mezcal craft accessories.", priority="medium", affected_artisans=["art-015"]),
    ]

    # Assemble and save
    data["artisans"] = [a.model_dump() for a in artisans]
    data["products"] = [p.model_dump() for p in products]
    data["orders"] = [o.model_dump() for o in orders]
    data["buyers"] = [b.model_dump() for b in buyers]
    data["fulfillment_tasks"] = [t.model_dump() for t in tasks]
    data["quality_assessments"] = [q.model_dump() for q in assessments]
    data["shipments"] = [s.model_dump() for s in shipments]
    data["subscription_boxes"] = [s.model_dump() for s in subs]
    data["insights"] = [i.model_dump() for i in insights]
    store.save(data)

    return {k: len(v) for k, v in data.items()}
