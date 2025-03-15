# 📚 Week 2: Interners Lab - Django APIs (Traditional & DRF)

For week 2, I explored building APIs in Django using both traditional methods and Django REST Framework (DRF) where I covered both Basic and Advanced tasks successfully. Below is a detailed walkthrough of the process, highlighting key concepts and commands used.

## ✅ Setting Up the Environment

**Open the Virtual Environment (venv)**
```bash
venv\Scripts\activate
```

**Install Django and Django REST Framework**
```bash
pip install django djangorestframework
```

---

## 🚀 Django REST Framework (DRF) Approach

![Screenshot 2025-03-15 181558](https://github.com/user-attachments/assets/cc619583-169d-48c7-9634-f34f9784ca46)

### 1️⃣ Create a Django App
```bash
python manage.py startapp products
```

### 2️⃣ Configure Settings
Open `backend/django/settings.py` and add the following to `INSTALLED_APPS`:
```python
'products',
'rest_framework',
```

### 3️⃣ Create the Product Model (`products/models.py`)
Define your product schema.

### 4️⃣ Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create a Serializer (`products/serializers.py`)
Serializers convert complex data (like Django models) into JSON and validate incoming data.
![Screenshot 2025-03-15 181610](https://github.com/user-attachments/assets/e37a4283-4ede-415c-a598-09967ac9f8e8)

### 6️⃣ Build API Views (`products/views.py`)
Use `ModelViewSet` for CRUD operations.
![Screenshot 2025-03-15 181619](https://github.com/user-attachments/assets/cc498f9f-4261-48d4-91b1-2bfcb2a04459)

### 7️⃣ Configure URLs (`products/urls.py`)
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

### 8️⃣ Include App URLs in Main URL Configuration (`django/urls.py`)

### 9️⃣ Run the Server
```bash
python manage.py runserver
```

---

## 🔄 API Testing (I am using Thunderclient for sending the requests)

**POST: Create a new product**
```http
POST http://127.0.0.1:8000/api/products/
![Screenshot 2025-03-15 182213](https://github.com/user-attachments/assets/2cf05329-4736-4194-bdef-9fb237798105)
```

**GET: Fetch all products**
```http
GET http://127.0.0.1:8000/api/products/
![Screenshot 2025-03-15 182308](https://github.com/user-attachments/assets/54394d3f-8fa2-4eef-92e9-af2ac1ad1cfe)

```
**PUT: Update a product**
```http
PUT http://127.0.0.1:8000/api/products/1/
```
**DELETE: Delete a product**
```http
DELETE http://127.0.0.1:8000/api/products/1/
```

---

## 🔧 Traditional Django Approach

### 1️⃣ Create Virtual Environment (if not done)

### 2️⃣ Create a Classic App
```bash
python manage.py startapp products_classic
![Screenshot 2025-03-15 182326](https://github.com/user-attachments/assets/0753e5dd-1797-415e-9d85-8ae867c44277)

```

### 3️⃣ Configure Settings
Add `'products_classic'` to `INSTALLED_APPS` in `settings.py`.

### 4️⃣ Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Write CRUD Operations in `views.py`
Manually write functions for Create, Read, Update, Delete.

### 6️⃣ Set Up Routes in `products_classic/urls.py`
Define URL patterns for each operation.

### 7️⃣ Include Classic App URLs in Main URL Configuration
```python
path('api/classic/', include('products_classic.urls')),
```

### 8️⃣ Add Validations
Ensure required fields and valid data in Create/Update operations.
![Screenshot 2025-03-15 182443](https://github.com/user-attachments/assets/3d5a8ce9-80be-40ff-8ffd-fd63898e0b34)


### 9️⃣ Add Pagination in Get Products
Implement basic pagination logic using query parameters.
![Screenshot 2025-03-15 182403](https://github.com/user-attachments/assets/636ccb73-3b01-4c23-88c2-b272a9838299)

---

## 🚀 Key Learnings
- Gained hands-on experience with both traditional and DRF approaches in Django.
- Understood the importance of serializers, `ModelViewSet`, and routers in DRF.
- Practiced manual validation, pagination, and error handling using traditional methods.

🔥 This journey provided a comprehensive understanding of API development in Django, balancing both ease and customization!

✨ *Feel free to contribute or provide feedback on how to improve this process further!*

