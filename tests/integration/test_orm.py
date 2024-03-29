from allocation.domain import model
from allocation.domain.tracker import Tracker
from allocation.domain.asset import Asset
from allocation.domain.aimodel import AIModel
from datetime import date
from sqlalchemy import text


def test_orderline_mapper_can_load_lines(session):
    session.execute(text(
        "INSERT INTO order_lines (orderid, sku, qty) VALUES "
        '("order1", "RED-CHAIR", 12),'
        '("order1", "RED-TABLE", 13),'
        '("order2", "BLUE-LIPSTICK", 14)'
    ))
    expected = [
        model.OrderLine("order1", "RED-CHAIR", 12),
        model.OrderLine("order1", "RED-TABLE", 13),
        model.OrderLine("order2", "BLUE-LIPSTICK", 14),
    ]
    assert session.query(model.OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session):
    new_line = model.OrderLine("order1", "DECORATIVE-WIDGET", 12)
    session.add(new_line)
    session.commit()

    rows = list(session.execute(text('SELECT orderid, sku, qty FROM "order_lines"')))
    assert rows == [("order1", "DECORATIVE-WIDGET", 12)]


def test_retrieving_batches(session):
    session.execute(text(
        "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
        ' VALUES ("batch1", "sku1", 100, null)'
    ))
    session.execute(text(
        "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
        ' VALUES ("batch2", "sku2", 200, "2011-04-11")'
    ))
    expected = [
        model.Batch("batch1", "sku1", 100, eta=None),
        model.Batch("batch2", "sku2", 200, eta=date(2011, 4, 11)),
    ]

    assert session.query(model.Batch).all() == expected


def test_saving_batches(session):
    batch = model.Batch("batch1", "sku1", 100, eta=None)
    session.add(batch)
    session.commit()
    rows = session.execute(text(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'
    ))
    assert list(rows) == [("batch1", "sku1", 100, None)]


def test_saving_allocations(session):
    batch = model.Batch("batch1", "sku1", 100, eta=None)
    line = model.OrderLine("order1", "sku1", 10)
    batch.allocate(line)
    session.add(batch)
    session.commit()
    rows = list(session.execute(text('SELECT orderline_id, batch_id FROM "allocations"')))
    assert rows == [(batch.id, line.id)]


def test_retrieving_allocations(session):
    session.execute(
        text('INSERT INTO order_lines (orderid, sku, qty) VALUES ("order1", "sku1", 12)')
    )
    [[olid]] = session.execute(
        text("SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku"),
        dict(orderid="order1", sku="sku1"),
    )
    session.execute(text(
        "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
        ' VALUES ("batch1", "sku1", 100, null)'
    ))
    [[bid]] = session.execute(
       text("SELECT id FROM batches WHERE reference=:ref AND sku=:sku"),
        dict(ref="batch1", sku="sku1"),
    )
    session.execute(
        text("INSERT INTO allocations (orderline_id, batch_id) VALUES (:olid, :bid)"),
        dict(olid=olid, bid=bid),
    )

    batch = session.query(model.Batch).one()

    assert batch._allocations == {model.OrderLine("order1", "sku1", 12)}
    
    
def test_saving_trackers(session):
    tr = Tracker("BTkUSDT", "2023-03-12 16:00:00+00:00", 1)
    session.add(tr)
    session.commit()
    rows = session.execute(text(
        'SELECT symbol, datetime_t, position FROM "trackers"'
    ))
    assert list(rows) == [("BTkUSDT", "2023-03-12 16:00:00+00:00", 1)]
    
    
def test_tracker_mapper_can_load(session):
    session.execute(text(
        "INSERT INTO trackers (symbol, datetime_t, position) VALUES "
        '("btcusdt", "RED-CHAIR", 12),'
        '("zecusd", "RED-TABLE", 13),'
        '("order2", "BLUE-LIPSTICK", 14)'
    ))
    expected = [
        Tracker("btcusdt", "RED-CHAIR", 12),
        Tracker("zecusd", "RED-TABLE", 13),
        Tracker("order2", "BLUE-LIPSTICK", 14),
    ]
    assert session.query(Tracker).all() == expected

def test_tracker_mapper_can_save(session):
    new_line = Tracker("order1", "DECORATIVE-WIDGET", 12)
    session.add(new_line)
    session.commit()

    rows = list(session.execute(text('SELECT symbol, datetime_t, position FROM "trackers"')))
    assert rows == [("order1", "DECORATIVE-WIDGET", 12)]  
    
def test_retrieving_assets(session):
    session.execute(text(
        "INSERT INTO assets (symbol, source)"
        ' VALUES ("batch1", "sku1")'
    ))
    session.execute(text(
        "INSERT INTO assets (symbol, source)"
        ' VALUES ("batch3", "sku2")'
    ))
    expected = [
        Asset("batch1", "sku1"),
        Asset("batch3", "sku2"),
    ]

    assert session.query(Asset).all() == expected


def test_saving_assets(session):
    asset = Asset("batch1", "sku1")
    session.add(asset)
    session.commit()
    rows = session.execute(text(
        'SELECT symbol, source FROM "assets"'
    ))
    assert list(rows) == [("batch1", "sku1")]
    
    
def test_saving_allocations_tracker(session):
    batch = Asset("batch1", "sku1")
    line = Tracker("batch1", "sku222", 10)
    batch.allocate_tracker(line)
    session.add(batch)
    session.commit()
    rows = list(session.execute(text('SELECT tracker_id, asset_id FROM "allocations_tracker"')))
    assert rows == [(batch.id, line.id)]
    
    
def test_retrieving_allocations_tarcker(session):
    session.execute(
        text('INSERT INTO trackers (symbol, datetime_t, position) VALUES ("order1", "sku1", 12)')
    )
    [[olid]] = session.execute(
        text("SELECT id FROM trackers WHERE symbol=:orderid AND datetime_t=:sku"),
        dict(orderid="order1", sku="sku1"),
    )
    session.execute(text(
        "INSERT INTO assets (symbol, source)"
        ' VALUES ("order1", "sku1111")'
    ))
    [[bid]] = session.execute(
       text("SELECT id FROM assets WHERE symbol=:ref AND source=:sku"),
        dict(ref="order1", sku="sku1111"),
    )
    session.execute(
        text("INSERT INTO allocations_tracker (tracker_id, asset_id) VALUES (:olid, :bid)"),
        dict(olid=olid, bid=bid),
    )

    batch = session.query(Asset).one()

    assert batch._allocations_tracker == {Tracker("order1", "sku1", 12)}
    
    
def test_aimodel_mapper_can_save(session):
    new_line = AIModel("order1", "DECORATIVE-WIDGET", 12, "bnb_2012_234", "xgboost", "bnb", 54.3)
    session.add(new_line)
    session.commit()

    rows = list(session.execute(text('SELECT symbol, source, feature_counts, model_name, ai_type, hashtag, accuracy_score FROM "aimodels"')))
    assert rows == [("order1", "DECORATIVE-WIDGET", 12, "bnb_2012_234", "xgboost", "bnb", 54.3)]  