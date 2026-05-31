from common.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    customer_email = db.Column(db.String(256), nullable=False)
    courier_email = db.Column(db.String(256), nullable=True)

    order_items = db.relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Order id={self.id} status={self.status}>"
