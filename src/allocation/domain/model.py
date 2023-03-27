from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, List, Set
from allocation.domain.tracker import Tracker


def allocate_tracker(tracker: Tracker, assets: List[Asset]) -> str:
    try:
        asset = next(a for a in sorted(assets) if a.can_allocate(tracker))
        asset.allocate_tracker(tracker)
        return asset.symbol, tracker.position
    except StopIteration:
        raise OutOfStock(f"Symbol not included {tracker.symbol}")

class Asset:
    def __init__(self, symbol: str, source: str):
        self.symbol = symbol
        self.source = source
        self._allocations_tracker = set()
        
    def allocate_tracker(self, tracker: Tracker):
        if self.can_allocate(tracker):
            self._allocations_tracker.add(tracker)
            
    def deallocate(self, tracker: Tracker):
        if tracker in self._allocations_tracker:
            self._allocations_tracker.remove(tracker)
            
    def can_allocate(self, tracker: Tracker) -> bool:
        return tracker.symbol == self.symbol
        
    def __repr__(self):
        return f"<Asset {self.symbol}, source: {self.source}>"

class AIModel:
    def __init__(self, symbol: str, source: str, feature_counts: int,
                 model_name: str, ai_type: str, hashtag: str, accuracy_score: float, created_at=datetime.now()):
        self.symbol = symbol
        self.source = source
        self.feature_counts = feature_counts
        self.model_name = model_name
        self.ai_type = ai_type
        self.hashtag = hashtag
        self.created_at = created_at
        
    @property    
    def get_filepath(self):
        return f"./src/KZ_project/dl_models/model_stack/{self.hashtag}/{self.model_name}"
               
    def __repr__(self):
        return f"<AIModel {self.symbol}, source: {self.source}, model_name: {self.model_name}>"
               


class OutOfStock(Exception):
    pass


class Product:
    def __init__(self, sku: str, batches: List[Batch], version_number: int = 0):
        self.sku = sku
        self.batches = batches
        self.version_number = version_number

    def allocate(self, line: OrderLine) -> str:
        try:
            batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
            batch.allocate(line)
            self.version_number += 1
            return batch.reference
        except StopIteration:
            raise OutOfStock(f"Out of stock for sku {line.sku}")


@dataclass(unsafe_hash=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()  # type: Set[OrderLine]

    def __repr__(self):
        return f"<Batch {self.reference}>"

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty