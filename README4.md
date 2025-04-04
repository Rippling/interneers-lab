# Week 4 - Interneers Lab 🚀

This week, we focused on **joining schemas in our database**. We introduced a **ProductCategory** model and linked it to the **Product** model using a **foreign key (ReferenceField)** in MongoDB.  

By the end of this week, we successfully:  
✅ Established relationships between products and categories  
✅ Implemented CRUD operations for categories  
✅ Added filters for fetching products  
✅ Migrated existing products to the new category structure  

---

## 🛠️ **Step 1: Add ProductCategory Model**
We added a `ProductCategory` model to `models.py` and modified the **Product** model's `category` field:  

- **Foreign Key:** `ReferenceField(ProductCategory)`  
- **Reverse Delete Rule:**
  - `reverse_delete_rule=2 (CASCADE)`: Deletes all related products if a category is removed.
  - `reverse_delete_rule=3 (NULLIFY)`: Keeps products even if their category is deleted.
![image](https://github.com/user-attachments/assets/d87c5195-cce4-4dd7-b6c8-533202122143)

---

## 🛠️ **Step 2: Implement CRUD for Product Categories**
We created two new files:  

### 🔹 **`product_category_repository.py`**  
Handles database operations:  
- `create_category()`  
- `get_category_by_id()`  
- `update_category()`  
- `delete_category()`  
- `format_category()`  

### 🔹 **`product_category_services.py`**  
Contains service functions, including:  
- `get_products_by_category()`: Fetches all products under a specific category.

---

## 🛠️ **Step 3: Update `product_repository.py`**
### 🔹 **Enhancements:**
1️⃣ When creating a product, if a new category is provided, it gets added to the database.  
2️⃣ While updating a product, if the category doesn't exist, it raises an error.  
3️⃣ Added methods to **add and remove products** in a category.

---

## 🛠️ **Step 4: Add Validations**
- **Used DRF Serializers** to validate requests.  
- **Set branding names which were previously `null`** for existing products without branding.
![image](https://github.com/user-attachments/assets/de2e6ebf-0e6a-4c3a-96cc-a5b402729920)

---

## 🛠️ **Step 5: Update Views and URLs**
- Modified `views.py` to handle all API changes.  
- Updated `urls.py` to include new category-related routes.

---

# 🔥 Advanced Tasks  
## ✅ **Step 1: Seed Script for Categories**
- **File:** `seed_categories.py`
- Ensures all products without a category get assigned a **default category** when the server starts.
```python
python -m products_mongo.seed_categories
```

## ✅ **Step 2: Implement Rich Filters**
- **File:** `product_services.py`
- Added advanced filtering options:
  - **Filter by category, name, price range, brand, etc.**
  -   ![image](https://github.com/user-attachments/assets/52b1fa15-4fa3-49e3-aad5-7994545792c6)


## ✅ **Step 3: Migrate Products Without a Category**
- **File:** `product_migrations.py`
- Moved products that were missing a category into a **separate default category**.
```python
python -m products_mongo.migrate_products
```
Finally tested everything using thunderclient successfully.
---

## 🎯 **Final Thoughts**
By the end of this week, we successfully implemented **category-based product management** and improved **query capabilities** with rich filters. 🚀

---
