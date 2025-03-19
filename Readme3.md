# Week 3

This week, we explored **MongoEngine**, set up **CRUD operations** in `ProductService`, added a **repository layer** for MongoDB connection, and analyzed everything using `test_script` and **MongoDB Compass**. Additionally, I learned about **audit columns** to improve API tracking.

## Steps Followed

## Step 1: Setting Up MongoDB and MongoEngine

1. **Install MongoDB and MongoEngine:**
   ```sh
   pip install pymongo mongoengine
   ```

2. **Update Django settings (`settings.py`):**
   ```python
   from mongoengine import connect

   MONGO_URI = "mongodb+srv://vidushiagg:vidushi%40123@atlascluster.metohzo.mongodb.net/interneerslab?retryWrites=true&w=majority"

   connect(
       host=MONGO_URI
   )
   ```

3. **Test MongoDB Connection (`test_connection.py`):**
   ```python
   from mongoengine import connect

   def init_db():
       connect(host=MONGO_URI, alias="default")
   ```

## Step 2: Creating Models and Layers

1. **Create `products_mongo` folder and define `models.py`:**
   ```python
   from mongoengine import Document, StringField, FloatField, IntField, DateTimeField
   from datetime import datetime

   class Product(Document):
       name = StringField(required=True, max_length=200)
       description = StringField()
       category = StringField()
       price = FloatField(required=True)
       brand = StringField()
       quantity_in_warehouse = IntField(default=0)
       created_at = DateTimeField(default=datetime.utcnow)
       updated_at = DateTimeField(default=datetime.utcnow)

       meta = {'collection': 'products'}
   ```

2. **Implement Repository Layer (`product_repository.py`):**
   - Handles direct interactions with MongoDB.

3. **Implement Service Layer (`product_service.py`):**
   - Handles business logic.

4. **Create API Endpoints using Django REST Framework (`views.py`):**
   - Implements a thin controller layer.

5. **Define Routes (`urls.py` in Django app):**
   - Exposes API for interaction via Thunder Client or HTTP requests.

## Step 3: Testing and Enhancements

1. **Update `models.py` with Audit Columns:**
   - Added `created_at` and `updated_at` fields to track product changes.

2. **Ensure MongoDB connection works (`test_connection.py`)**
   - Defined `init_db()` to use MongoDB connection.


## Step 4: Enhancements and Pagination

1. **Enhanced `product_service.py` with Audit Columns:**
   - Ensured structured API responses.

2. **Implemented Pagination & Filtering:**
   - Allowed fetching products by **date range**.

3. **Test Everything:**
   - Used `test_service.py`.
   - Verified using **MongoDB Compass**.
   - Tested API calls via **Thunder Client**.
       (i) Post: http://127.0.0.1:8000/api/mongo/products/
           ![Screenshot 2025-03-19 204408](https://github.com/user-attachments/assets/dae982db-e65e-4c54-8f75-1caa6f6da96d)
           Method: POST
       (ii) Get using pagination: http://127.0.0.1:8000/api/mongo/products/?page=1&per_page=1
            ![Screenshot 2025-03-19 204117](https://github.com/user-attachments/assets/681e1329-6db9-48c8-8a6d-ea23a42998f0)
            Method: GET
       (iii) Get using Date Range: http://127.0.0.1:8000/api/mongo/products/?start_date=2024-03-01&end_date=2024-03-19
            ![Screenshot 2025-03-19 204052](https://github.com/user-attachments/assets/893906a1-cdbc-40af-90a2-e6feb6a2a3c6)
            Method: POST
       (iv) Update the product: http://127.0.0.1:8000/api/mongo/products/{product_id}
            ![Screenshot 2025-03-19 204148](https://github.com/user-attachments/assets/1098099d-5c76-40dc-94a0-ae739e13d67d)
            Method: PUT
       (v) Delete the product: http://127.0.0.1:8000/api/mongo/products/{product_id}
           ![Screenshot 2025-03-19 204203](https://github.com/user-attachments/assets/5f2b74a6-bc27-43a6-8d5a-5704d982a883)
           Method: DELETE
---

Now, the setup is complete, and we can efficiently manage products with MongoDB, ensuring structured responses and smooth CRUD operations!
