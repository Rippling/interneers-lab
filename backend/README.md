# Django Product Management API

A comprehensive RESTful API for managing products and categories built with Django and Django REST Framework. This project implements a robust product management system with advanced features like stock management, categorization, and detailed product tracking.

## Features

### Product Management
- Complete CRUD operations for products and categories
- Automatic slug generation for SEO-friendly URLs
- Rich product details including SKU, pricing, dimensions, and weight
- Stock management with low stock alerts
- Featured products functionality
- Product status tracking (active, inactive, out of stock, discontinued)
- Product categorization and tagging
- Comprehensive validation rules

### Search and Filtering
- Advanced search capabilities across multiple fields
- Filter products by:
  - Category
  - Price range
  - Stock status
  - Featured status
  - Search terms (name, description, SKU, brand, tags)
- Sorting and ordering options
- Pagination support

### Admin Interface
- Custom Django admin interface
- Quick-edit functionality for stock and status
- Advanced filtering and search
- Organized fieldsets for better data management
- Visual indicators for stock status
- Collapsible metadata sections

## Project Structure
```
.
├── README.md
├── db.sqlite3
├── ecommerce/                  # Main project directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py            # Project settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py
├── manage.py
├── postman/                   # API testing
│   └── ProductCatalogAPI.postman_collection.json
├── products/                  # Main app directory
│   ├── __init__.py
│   ├── admin.py              # Admin interface customization
│   ├── apps.py
│   ├── migrations/           # Database migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_product_discount_price_alter_product_price.py
│   │   └── __init__.py
│   ├── models.py             # Database models
│   ├── serializers.py        # API serializers
│   ├── tests.py             # Unit tests
│   ├── urls.py              # App URL configuration
│   └── views.py             # API views and logic
└── requirements.txt          # Project dependencies
```

Key files and their purposes:
- `ecommerce/settings.py`: Project configuration, database settings, installed apps
- `ecommerce/urls.py`: Main URL routing configuration
- `products/models.py`: Database models for Product and Category
- `products/views.py`: API views and business logic
- `products/serializers.py`: Data serialization and validation
- `products/admin.py`: Django admin interface customization
- `postman/ProductCatalogAPI.postman_collection.json`: Ready-to-use API testing collection

## API Endpoints

### Categories
```http
# List all categories
GET /api/categories/

# Create a new category
POST /api/categories/
{
    "name": "Electronics",
    "description": "Electronic devices and accessories"
}

# Get category details
GET /api/categories/{slug}/

# Update category
PUT/PATCH /api/categories/{slug}/
{
    "name": "Updated Electronics",
    "description": "Updated description"
}

# Delete category (only if no associated products)
DELETE /api/categories/{slug}/
```

### Products
```http
# List all products
GET /api/products/

# Create a new product
POST /api/products/
{
    "sku": "ELE-12345",
    "name": "Wireless Headphones",
    "description": "High-quality wireless headphones",
    "category": 1,
    "brand": "AudioTech",
    "price": "99.99",
    "quantity": 50,
    "weight": 0.3,
    "dimensions": "18x15x8",
    "tags": "audio, wireless, headphones"
}

# Get product details
GET /api/products/{slug}/

# Update product
PUT/PATCH /api/products/{slug}/

# Delete product
DELETE /api/products/{slug}/

# List featured products
GET /api/products/featured/

# List low stock products
GET /api/products/low_stock/

# Update product stock
PATCH /api/products/{slug}/update_stock/
{
    "quantity": 25
}
```

## Filtering Examples

```http
# Filter by category
GET /api/products/?category=electronics

# Filter by price range
GET /api/products/?min_price=50&max_price=200

# Filter by stock status
GET /api/products/?stock_status=in_stock
GET /api/products/?stock_status=out_of_stock
GET /api/products/?stock_status=low_stock

# Search products
GET /api/products/?search=wireless

# Combined filters
GET /api/products/?category=electronics&min_price=50&max_price=200&stock_status=in_stock
```

## Data Validation Rules

### Product Validation
- SKU Format: ABC-12345 (3 uppercase letters, hyphen, 5 digits)
- Price: Must be greater than or equal to 0.01
- Discount Price: Must be less than regular price
- Quantity: Must be non-negative integer
- Dimensions Format: length x width x height (e.g., "10x20x30")
- Rating: Between 0.00 and 5.00
- Weight: Positive decimal number
- Required Fields: SKU, name, description, category, brand, price

### Category Validation
- Name: Required and unique
- Slug: Auto-generated from name, unique
- Cannot delete categories with associated products

## Setup and Installation

1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Apply migrations
```bash
python manage.py migrate
```

5. Create superuser for admin access
```bash
python manage.py createsuperuser
```

6. Run development server
```bash
python manage.py runserver
```

## Testing with Postman

### Setting Up Postman
1. Download and install Postman from [https://www.postman.com/downloads/](https://www.postman.com/downloads/)
2. Create a new collection named "Product Management API"
3. Set up base URL environment variable (optional):
   - Create new environment
   - Add variable `BASE_URL` with value `http://127.0.0.1:8000`

### 1. Category Management

#### Create Category
- Method: POST
- URL: `http://127.0.0.1:8000/api/categories/`
- Headers: 
  - Content-Type: application/json
- Body (raw JSON):
```json
{
    "name": "Electronics",
    "description": "Electronic devices and accessories"
}
```
- Expected Response (200 OK):
```json
{
    "id": 1,
    "name": "Electronics",
    "slug": "electronics",
    "description": "Electronic devices and accessories",
    "created_at": "2025-03-08T23:34:41.655300Z",
    "updated_at": "2025-03-08T23:34:41.655355Z"
}
```

#### Delete Category (with Products)
- Method: DELETE
- URL: `http://127.0.0.1:8000/api/categories/electronics/`
- Expected Response (400 Bad Request):
```json
{
    "error": "Cannot delete category with associated products"
}
```

### 2. Product Management

#### Create Product
- Method: POST
- URL: `http://127.0.0.1:8000/api/products/`
- Headers: 
  - Content-Type: application/json
- Body (raw JSON):
```json
{
    "sku": "ELE-12345",
    "name": "Wireless Headphones",
    "description": "High-quality wireless headphones",
    "category": 1,
    "brand": "AudioTech",
    "price": "99.99",
    "quantity": 50,
    "weight": 0.3,
    "dimensions": "18x15x8",
    "tags": "audio, wireless, headphones"
}
```
- Expected Response (201 Created):
```json
{
    "id": 1,
    "uuid": "2b1645af-c53f-4d45-be9e-67810f0c7925",
    "sku": "ELE-12345",
    "name": "Wireless Headphones",
    "slug": "wireless-headphones",
    "description": "High-quality wireless headphones",
    "category": 1,
    "category_name": "Electronics",
    // ... other fields ...
}
```

#### Test Validation (Invalid Price)
- Method: POST
- URL: `http://127.0.0.1:8000/api/products/`
- Body (raw JSON):
```json
{
    "sku": "ELE-11111",
    "name": "Test Product",
    "description": "Test product",
    "category": 1,
    "brand": "Test",
    "price": "0.00",
    "quantity": 10
}
```
- Expected Response (400 Bad Request):
```json
{
    "errors": {
        "price": ["Ensure this value is greater than or equal to 0.01."]
    }
}
```

### 3. Stock Management

#### Update Stock
- Method: PATCH
- URL: `http://127.0.0.1:8000/api/products/wireless-headphones/update_stock/`
- Body (raw JSON):
```json
{
    "quantity": 5
}
```
- Expected Response (200 OK):
```json
{
    "id": 1,
    "quantity": 5,
    "is_in_stock": true,
    "is_low_stock": true,
    // ... other fields ...
}
```

#### Check Low Stock Products
- Method: GET
- URL: `http://127.0.0.1:8000/api/products/low_stock/`
- Expected Response (200 OK):
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Wireless Headphones",
            "quantity": 5,
            "low_stock_threshold": 10,
            "is_low_stock": true,
            // ... other fields ...
        }
    ]
}
```

### 4. Search and Filtering

#### Search Products
- Method: GET
- URL: `http://127.0.0.1:8000/api/products/?search=wireless`

#### Filter by Category
- Method: GET
- URL: `http://127.0.0.1:8000/api/products/?category=electronics`

#### Filter by Price Range
- Method: GET
- URL: `http://127.0.0.1:8000/api/products/?min_price=50&max_price=200`

#### Combined Filters
- Method: GET
- URL: `http://127.0.0.1:8000/api/products/?category=electronics&min_price=50&max_price=200&stock_status=in_stock`

### Response Status Codes
- 200: Successful operation
- 201: Resource created
- 400: Bad request (validation error)
- 404: Resource not found
- 500: Server error

### Testing Tips
1. Use Postman's environment variables for base URL
2. Create a collection with all test cases
3. Test validation rules systematically
4. Check response status codes and bodies
5. Verify error messages are clear and helpful
6. Test edge cases (e.g., minimum/maximum values)
7. Verify all filters work in combination

## Admin Interface Access

1. Access the admin panel at: http://127.0.0.1:8000/admin/
2. Log in with superuser credentials
3. Navigate to Products or Categories sections
4. Use the interface to:
   - Manage products and categories
   - Monitor stock levels
   - Update product status
   - View and edit all product details
   - Search and filter items

## Error Handling

The API provides clear error messages for various scenarios:
- Invalid data format
- Validation failures
- Non-existent resources
- Business rule violations (e.g., deleting categories with products)

## Security Considerations

- CORS configuration for API access
- Admin interface authentication
- Data validation and sanitization
- Protected sensitive operations

## Dependencies

- Django >= 5.1.7
- Django REST Framework >= 3.15.2
- django-cors-headers >= 4.7.0
- python-dotenv >= 1.0.1

## Testing

This project includes a comprehensive test suite with unit tests. The tests are written using pytest and cover the following components:

- Unit tests for the service layer
- Parameterized tests for various validation scenarios

### Running Tests

You can run the tests using the `run_tests.py` script:

```bash
# Run all tests
python run_tests.py

# Run only unit tests
python run_tests.py --type unit

# Run tests with verbose output
python run_tests.py --verbose

# Run tests without coverage reporting
python run_tests.py --no-coverage
```

### Test Structure

The tests are organized in the following structure:

```
tests/
  ├── unit/                # Unit tests
  │   ├── test_product_service.py
  │   ├── test_category_service.py
  │   └── test_parameterized.py
  └── seed_test_data.py    # Script to seed test data
```

### Code Coverage

When you run the tests with coverage reporting enabled (the default), a coverage report will be generated in the console output and an HTML report will be generated in the `coverage_html` directory.

## Development Workflow

### Pull Request Process

1. Create a feature branch from `main`
2. Make your changes and add tests
3. Run tests locally to ensure they pass
4. Push your branch and create a pull request
5. The CI workflow will automatically run tests on your PR
6. After review and approval, your changes will be merged

### Seeding Test Data

You can use the provided seed script to populate the database with test data:

```python
from products.tests.seed_test_data import seed_all

# Seed categories and products
categories, products = seed_all()
``` 