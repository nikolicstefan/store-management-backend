from common.extensions import db
from common.models.product_categories import product_categories


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)

    categories = db.relationship(
        "Category",
        secondary=product_categories,
        back_populates="products"
    )

    order_items = db.relationship(
        "OrderItem",
        back_populates="product"
    )

    def __repr__(self) -> str:
        return f"<Product id={self.id} name={self.name}>"
