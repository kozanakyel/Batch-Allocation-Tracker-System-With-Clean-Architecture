from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, registry
from sqlalchemy.sql import func

from allocation.domain import model
from allocation.domain.tracker import Tracker
from allocation.domain.asset import Asset
from allocation.domain.aimodel import AIModel

mapper_registry = registry()


metadata = MetaData()

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)

products = Table(
    "products",
    metadata,
    Column("sku", String(255), primary_key=True),
    Column("version_number", Integer, nullable=False, server_default="0"),
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", ForeignKey("products.sku")),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)


assets = Table(
    "assets",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("symbol", String(25)),
    Column("source", String(100))
    
)

aimodels = Table(
    "aimodels",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("symbol", String(25)),
    Column("source", String(100)),
    Column("feature_counts", Integer),
    Column("model_name", String(500)),
    Column("ai_type", String(200)),
    Column("hashtag", String(100), nullable=True),
    Column("accuracy_score", Float()),
    Column("created_at", DateTime())
)


trackers = Table(
    "trackers",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("symbol", String(25)),
    Column("datetime_t", String(200)),
    Column("position", Integer, nullable=False),
    Column("created_at", DateTime())
)

allocations_tracker = Table(
    "allocations_tracker",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("tracker_id", ForeignKey("trackers.id")),
    Column("asset_id", ForeignKey("assets.id")),
)


def start_mappers():
    lines_mapper = mapper_registry.map_imperatively(model.OrderLine, order_lines)
    batches_mapper = mapper_registry.map_imperatively(
        model.Batch,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper,
                secondary=allocations,
                collection_class=set,
            )
        },
    )
    mapper_registry.map_imperatively(
        model.Product, products, properties={"batches": relationship(batches_mapper)}
    )
    
    
    lines_mapper_tracker = mapper_registry.map_imperatively(
        Tracker, trackers
    )
    
    mapper_registry.map_imperatively(
        Asset, 
        assets,
         properties={
            "_allocations_tracker": relationship(
                lines_mapper_tracker, secondary=allocations_tracker, collection_class=set,
            )
        },
    )
    
    mapper_registry.map_imperatively(
        AIModel, aimodels
    )