from sqlalchemy import Column, Integer, Numeric, String, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class MenuItem(Base):
    __tablename__ = 'menu_items'  # Matches your SQL definition

    item_id = Column(Integer, primary_key=True)  # SERIAL in PostgreSQL
    name = Column(String(255))
    description = Column(String(1000))
    price = Column(Numeric(10, 2))
    category = Column(String(100), nullable=False)  # Category (e.g., main dish, drink, etc.)
    image_url = Column(String(255), nullable=True)

    def __repr__(self):
        return f"MenuItem(id={self.item_id}, name={self.name}, price={self.price})"


class Order(Base):
    __tablename__ = 'orders'  # Matches your SQL definition

    order_id = Column(Integer, primary_key=True)  # SERIAL in PostgreSQL
    bill = Column(Numeric(10, 2))  # DECIMAL type for bill
    status = Column(String(255), CheckConstraint("status IN ('in transit', 'delivered')"))

    def __repr__(self):
        return f"Order(id={self.order_id}, bill={self.bill}, status={self.status})"


class OrderDetails(Base):
    __tablename__ = 'orders_details'  # Matches your SQL definition

    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('menu_items.item_id'), primary_key=True)
    quantity = Column(Integer)
    total_price = Column(Numeric(10, 2))

    # Relationships
    order = relationship("Order", backref="order_details")
    menu_item = relationship("MenuItem", backref="order_details")

    def __repr__(self):
        return f"OrderDetails(order_id={self.order_id}, item_id={self.item_id}, quantity={self.quantity}, total_price={self.total_price})"
