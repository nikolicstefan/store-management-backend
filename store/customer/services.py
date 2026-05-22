from typing import Any

from common.models.category import Category
from common.models.product import Product


def search_products(name: str, category: str) -> tuple[list[dict[str, Any]], list[str]]:
    name = name.strip()
    category = category.strip()

    products = (
        Product.query
        .join(Product.categories)
        .filter(Product.name.ilike(f"%{name}%"))
        .filter(Category.name.ilike(f"%{category}%"))
        .distinct()
        .order_by(Product.id)
        .all()
    )

    categories = (
        Category.query
        .join(Category.products)
        .filter(Category.name.ilike(f"%{category}%"))
        .filter(Product.name.ilike(f"%{name}%"))
        .distinct()
        .order_by(Category.name)
        .all()
    )

    return [
        {
            "categories": sorted(category.name for category in product.categories),
            "id": product.id,
            "name": product.name,
            "price": product.price
        }
        for product in products
    ], [
        category.name
        for category in categories
    ]
