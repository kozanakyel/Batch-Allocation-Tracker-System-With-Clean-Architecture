import abc
from allocation.domain.tracker import Tracker
from allocation.adapters.repository import AbstractBaseRepository

class AbstractTrackerRepository(AbstractBaseRepository):
    @abc.abstractmethod
    def add(self, tracker: Tracker):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, symbol) -> Tracker:
        raise NotImplementedError
    
class TrackerRepository(AbstractTrackerRepository):
    def __init__(self, session):
        self.session = session

    def add(self, tracker):
        self.session.add(tracker)

    def get(self, symbol):
        return self.session.query(Tracker).filter_by(symbol=symbol).first()
    
    def list(self):
        return self.session.query(Tracker).all()
