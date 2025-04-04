# Product API Documentation

This Product API is designed with a **Repository, Service, and Controller layer architecture** for **separation of concerns** and efficient product management. It supports **CRUD operations**, **pagination**, and **sorting**, utilizing a `Product` model integrated with **MongoDB**.

## Architecture Layers

- **Controller Layer:** Handles HTTP requests and responses (thin layer).  
- **Service Layer:** Contains business logic and interacts with the repository layer.  
- **Repository Layer:** Manages database interactions, handling read/write operations in MongoDB.  


## Product Model

The Product model defines the schema for storing product details in a MongoDB collection.

```python
class Product(Document):
    name = StringField(max_length=100, required=True)
    description = StringField()
    category = StringField(max_length=50)
    price = DecimalField(precision=2, required=True)
    brand = StringField(max_length=50)
    quantity = IntField(default=0, min_value=0)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    
    meta = {"collection": "products_collection"}
```


## API Endpoints

| Endpoint               | HTTP Method | Description                                  |
|------------------------|-------------|----------------------------------------------|
| `/api/products/`       | GET         | Retrieve paginated, sortable product list    |
|                        | POST        | Create a new product                         |
| `/api/products/<id>/`  | GET         | Retrieve specific product details by ID      |
|                        | PUT         | Update specific product by ID                |
|                        | DELETE      | Delete specific product by ID                |

## Key Features

### Pagination
- Default: 2 items per page
- Customize with `page_size` parameter (e.g., `?page_size=5`)

### Sorting
- Sort by creation date: `?sort_by=created_at` (newest first)
- Sort by update date: `?sort_by=updated_at` (recently updated first)

### Validation
- Required fields: `name`, `price`
- Type checking for all fields
- Quantity minimum value: 0
- Returns `400/404` errors for invalid ObjectIds or missing products