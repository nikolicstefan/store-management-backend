from common.extensions import db
from common.models.product_categories import product_categories


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)

    products = db.relationship(
        "Product",
        secondary=product_categories,
        back_populates="categories"
    )

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name}>"
