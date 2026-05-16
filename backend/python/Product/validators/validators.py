def validate_product_data(data, require_all_fields=True):
    """
    Validates product data for create (POST/PUT) and partial update (PATCH).
    When require_all_fields=True, all fields must be present.
    When require_all_fields=False, only provided fields are validated.
    Returns a dict of field-level errors, empty if all validations pass.

    Week 4: category_id is now optional on create — products can be created
    without a category and assigned to one later via the category endpoints.
    """
    errors = {}

    if require_all_fields:
        required_fields = ["name", "description", "price", "brand", "quantity"]
        for field in required_fields:
            if field not in data or data[field] in [None, ""]:
                errors[field] = f"{field} is required"

    # Must be a positive non-zero number, rejects booleans
    if "price" in data and "price" not in errors:
        if data["price"] in [None, ""]:
            errors["price"] = "Price cannot be null or empty"
        elif isinstance(data["price"], bool):
            errors["price"] = "Price must be a valid number"
        else:
            try:
                price = float(data["price"])
                if price <= 0:
                    errors["price"] = "Price must be a positive non-zero number"
            except (ValueError, TypeError):
                errors["price"] = "Price must be a valid number"

    # Must be a positive non-zero integer, bool excluded as it subclasses int in Python
    if "quantity" in data and "quantity" not in errors:
        if data["quantity"] in [None, ""]:
            errors["quantity"] = "Quantity cannot be null or empty"
        elif not isinstance(data["quantity"], int) or isinstance(
            data["quantity"], bool
        ):
            errors["quantity"] = "Quantity must be a valid integer"
        elif data["quantity"] <= 0:
            errors["quantity"] = "Quantity must be a positive non-zero integer"

    # Must be a non-empty string under 255 characters
    if "name" in data and "name" not in errors:
        if data["name"] in [None, ""]:
            errors["name"] = "Name cannot be null or empty"
        elif not isinstance(data["name"], str):
            errors["name"] = "Name must be a string"
        elif len(data["name"]) > 255:
            errors["name"] = "Name must be under 255 characters"

    if "description" in data and "description" not in errors:
        if data["description"] in [None, ""]:
            errors["description"] = "Description cannot be null or empty"
        elif not isinstance(data["description"], str):
            errors["description"] = "Description must be a string"

    if "brand" in data and "brand" not in errors:
        if data["brand"] in [None, ""]:
            errors["brand"] = "Brand cannot be null or empty"
        elif not isinstance(data["brand"], str):
            errors["brand"] = "Brand must be a string"

    # category_id is optional — validated only if explicitly provided
    if "category_id" in data and data["category_id"] is not None:
        if not isinstance(data["category_id"], str) or not data["category_id"].strip():
            errors["category_id"] = "category_id must be a non-empty string"

    return errors


def validate_category_data(data, require_all_fields=True):
    """
    Validates ProductCategory data for create and update operations.
    When require_all_fields=True (POST/PUT), both title and description are required.
    When require_all_fields=False (PATCH), only provided fields are validated.
    """
    errors = {}

    if require_all_fields:
        for field in ["title", "description"]:
            if field not in data or data[field] in [None, ""]:
                errors[field] = f"{field} is required"

    if "title" in data and "title" not in errors:
        if data["title"] in [None, ""]:
            errors["title"] = "Title cannot be null or empty"
        elif not isinstance(data["title"], str):
            errors["title"] = "Title must be a string"
        elif len(data["title"]) > 255:
            errors["title"] = "Title must be under 255 characters"

    if "description" in data and "description" not in errors:
        if data["description"] in [None, ""]:
            errors["description"] = "Description cannot be null or empty"
        elif not isinstance(data["description"], str):
            errors["description"] = "Description must be a string"

    return errors


def validate_csv_row(row: dict, row_number: int) -> dict:
    """
    Validates a single row from a CSV bulk import.

    Returns a dict with:
      - "errors": field-level errors for this row (empty if valid)
      - "row": the row number (1-indexed, excluding header) for error reporting
    """
    errors = validate_product_data(row, require_all_fields=True)
    return {"row": row_number, "errors": errors}
