from csv import Error, reader
from io import StringIO
from typing import Any

from werkzeug.datastructures import FileStorage

from common.validation import ValidationError


def validate_file(file: Any) -> list[dict[str, Any]]:
    if file is None:
        raise ValidationError("Field file missing.")

    if not isinstance(file, FileStorage) or not file.filename.endswith(".csv"):
        raise ValidationError("Invalid file.")

    try:
        stream = StringIO(file.stream.read().decode("utf-8"))
        rows = list(reader(stream))
    except (UnicodeDecodeError, Error):
        raise ValidationError("Invalid file.")

    product_inputs = []
    seen_product_names = set()

    for line_number, row in enumerate(rows):
        if len(row) != 3:
            raise ValidationError(f"Incorrect number of values on line {line_number}.")

        category_names_str, name, price_str = [field.strip() for field in row]

        if not category_names_str:
            raise ValidationError(f"Incorrect category names on line {line_number}.")

        if not name:
            raise ValidationError(f"Incorrect name on line {line_number}.")

        if not price_str:
            raise ValidationError(f"Incorrect price on line {line_number}.")

        category_names = [category_name.strip() for category_name in category_names_str.split("|")]

        if (
            any(not category_name for category_name in category_names)
            or len(category_names) != len(set(category_names))
        ):
            raise ValidationError(f"Incorrect category names on line {line_number}.")

        if name in seen_product_names:
            raise ValidationError(f"Product {name} already exists.")

        seen_product_names.add(name)

        try:
            price = float(price_str)
        except ValueError:
            raise ValidationError(f"Incorrect price on line {line_number}.")

        if price <= 0:
            raise ValidationError(f"Incorrect price on line {line_number}.")

        product_inputs.append({
            "category_names": category_names,
            "name": name,
            "price": price
        })

    return product_inputs
