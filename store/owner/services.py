from typing import Any

from common.extensions import db
from common.models import *
from common.services import ServiceError


def create_products(product_inputs: list[dict[str, Any]]) -> None:
    input_product_names = [product_input["name"] for product_input in product_inputs]

    existing_product = Product.query.filter(Product.name.in_(input_product_names)).first()
    if existing_product:
        raise ServiceError(f"Product {existing_product.name} already exists.")

    input_category_names = {
        category_name
        for product_input in product_inputs
        for category_name in product_input["category_names"]
    }
    existing_categories = Category.query.filter(Category.name.in_(input_category_names)).all()
    existing_category_names = {existing_category.name for existing_category in existing_categories}
    missing_category_names = input_category_names - existing_category_names

    categories_by_name = {existing_category.name: existing_category for existing_category in existing_categories}
    for missing_category_name in missing_category_names:
        category = Category(name=missing_category_name)
        db.session.add(category)
        categories_by_name[missing_category_name] = category

    for product_input in product_inputs:
        product = Product(
            name=product_input["name"],
            price=product_input["price"]
        )

        for category_name in product_input["category_names"]:
            product.categories.append(categories_by_name[category_name])

        db.session.add(product)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
