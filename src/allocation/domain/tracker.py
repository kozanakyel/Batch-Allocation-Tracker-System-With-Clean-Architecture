from datetime import datetime

class Tracker:
    def __init__(self, symbol: str, datetime_t: str, position: int, created_at=datetime.now()):
        self.symbol = symbol
        self.datetime_t = datetime_t
        self.position = position
        self.created_at = created_at
        
        
    def __repr__(self):
        return f"<Tracker {self.symbol}, datetime: {self.datetime_t}, position: {self.position}, created_at: {self.created_at}>"