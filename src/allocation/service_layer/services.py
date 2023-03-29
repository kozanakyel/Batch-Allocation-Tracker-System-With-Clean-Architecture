from __future__ import annotations
from typing import Optional
from datetime import date
import json
from flask import jsonify

from allocation.domain.asset import Asset, allocate_tracker

from allocation.domain.aimodel import AIModel
from allocation.domain.model import OrderLine
from allocation.service_layer import unit_of_work
from allocation.domain import model

from allocation.adapters.repository import AbstractBaseRepository
from allocation.domain.tracker import Tracker
from allocation.domain.asset import InvalidSymbol

class InvalidSku(Exception):
    pass


def add_batch(
    ref: str, sku: str, qty: int, eta: Optional[date],
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        product = uow.products.get(sku=sku)
        if product is None:
            product = model.Product(sku, batches=[])
            uow.products.add(product)
        product.batches.append(model.Batch(ref, sku, qty, eta))
        uow.commit()


def allocate(
    orderid: str, sku: str, qty: int,
    uow: unit_of_work.AbstractUnitOfWork,
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f"Invalid sku {line.sku}")
        batchref = product.allocate(line)
        uow.commit()
    return 


def add_asset(
    symbol: str, source: str,
    repo: AbstractBaseRepository, session,
) -> None:
    repo.add(Asset(symbol, source))
    session.commit()
    
def is_valid_symbol(symbol, assets):
    return symbol in {asset.symbol for asset in assets}

    
def allocate_tracker(
    symbol: str, datetime_t: str, position: int,
    repo: AbstractBaseRepository, session
) -> tuple:
    tracker = Tracker(symbol, datetime_t, position)
    print(f'tracker created_at : {tracker.created_at}')
    assets = repo.list()
    if not is_valid_symbol(tracker.symbol, assets):
        raise InvalidSymbol(f"Invalid symbol {tracker.symbol}")
    result_tracker = allocate_tracker(tracker, assets)
    session.commit()
    print(f'result print allocatie tracker:L {result_tracker}')
    return result_tracker

def get_position(
    symbol: str, 
    repo: AbstractBaseRepository, session,
):
    result = repo.get(symbol)
    session.commit()
    return result.symbol, result.position, result.datetime_t