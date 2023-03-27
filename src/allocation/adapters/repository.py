import abc
from allocation.domain import model


class AbstractBaseRepository():
    @abc.abstractmethod
    def add():
        raise NotImplementedError
    
    @abc.abstractmethod
    def get():
        raise NotImplementedError
    
    

class AbstractRepository(AbstractBaseRepository):
    @abc.abstractmethod
    def add(self, product: model.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, sku) -> model.Product:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, product):
        self.session.add(product)

    def get(self, sku):
        return self.session.query(model.Product).filter_by(sku=sku).first()