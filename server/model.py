from sqlalchemy import Column, Integer, Numeric, String, CheckConstraint, ForeignKey
from database import Base


class OrderDetails(Base):
    __tablename__ = 'orders_details'  # Ensure the table name matches your SQL definition

    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('menu_items.item_id'), primary_key=True)
    quantity = Column(Integer)
    total_price = Column(Numeric(10, 2))

    def __repr__(self):
        return f"OrderDetails(id={self.order_id}, item_id={self.item_id}, quantity={self.quantity}, total_price={self.total_price})"

class Order(Base):
    __tablename__ = 'orders'  # Ensure the table name matches your SQL definition

    order_id = Column(Integer, primary_key=True)  # SERIAL type in PostgreSQL
    status = Column(String(255), CheckConstraint("status IN ('in transit', 'delivered')"))

class MenuItem(Base):
    __tablename__ = 'menu_items'  # Ensure the table name matches your SQL definition

    item_id = Column(Integer, primary_key=True)  # SERIAL type in PostgreSQL
    name = Column(String(255))
    description = Column(String(1000))
    price = Column(Numeric(10, 2))

