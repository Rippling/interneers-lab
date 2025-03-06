# Table of Contents:
+ [API Documentation](#api-documentation)
    + [Products Collection](#products-collection-products)
        1. [Product Model](#product-model)
        2. [List All Products](#list-all-products-get)
        3. [Create a Product](#create-a-new-product-post)
    + [Product Document](#product-document-productsid)
        1. [List a Product](#list-a-product-get)
        2. [Update a Product](#update-a-product-patch)
        3. [Delete a Product](#delete-a-product-delete)
    + [Unspecified Endpoints](#unspecified-endpoints)


# API Documentation:

## Products Collection [/products]

### Product model:
The product model is the primary resource managed by this API. It described a product, in JSON format.
+ Model (application/json)

        {
            "id": <integer> (required) Auto-assigned ID whenever a product is added,
            "name": <string> (required) The name of the product,
            "price": <integer> (required) The price of the product, non-negative values only,
            "brand": <string> The brand associated with the product, useful for filtering,
            "category": <string> The category of this item, can only be one of {"Appliances", "Gadgets", "Others"},
            "quantity": <integer> (required) Quantity of this item in stock, non-negative values only,
            "description": <string> Description of this item, in English,
        }


### List All products [GET]

Returns a list of all products currently in the system. The list is guarenteed to be sorted by ID.

Successful request:

+ Response 200 (application/json)

        [        
            {
                "name": "Bajaj DMH90 Neo 90L Desert Air Cooler",
                "price": 10999,
                "brand": "Bajaj",
                "category": "Appliances",
                "description": "Air Cooler for Home|For Larger Room|BIG ICE Chamber|Anti-Bacterial Honeycomb Pads",
                "quantity": 25,
                "id": 1
            },
            {
                "name": "Orient Electric 9W High Glow LED bulb| Pack of 2",
                "price": 108,
                "brand": "Orient Electric",
                "category": "Appliances",
                "description": "180-degree wide beam angle| Voltage surge protection up to 4 kV| 6500K, Cool White",
                "quantity": 205,
                "id": 2
            }
        ]


### Create a New Product [POST]

+ Request (application/json)

        {
            "name": "Bajaj DMH90 Neo 90L Desert Air Cooler",
            "price": 10999,
            "brand": "Bajaj",
            "category": "Appliances",
            "description": "Air Cooler for Home|For Larger Room|BIG ICE Chamber|Anti-Bacterial Honeycomb Pads",
            "quantity": 25
        }

+ Response 201 (application/json)

    + Headers

            Location: /products/2

    + Body

            {
                "name": "Bajaj DMH90 Neo 90L Desert Air Cooler",
                "price": 10999,
                "brand": "Bajaj",
                "category": "Appliances",
                "description": "Air Cooler for Home|For Larger Room|BIG ICE Chamber|Anti-Bacterial Honeycomb Pads",
                "quantity": 25,
                "id": 2
            }

<details>
<summary> Common errors </summary>
<br>
Invalid name:

+ Request (application/json)

        {
            "name": "",
            "price": 108,
            "quantity": 205
        }
+ Response 400 (application/json)

        {
            "code": "BAD_REQUEST",
            "message": "The server cannot process this request",
            "details": "'name' field is invalid",
            "timestamp": "2025-03-05 18:54:48.326889 GMT+0:00",
            "request": "POST /products",
            "suggestion": "Re-send the request with an appropriate name field, it must be a non-empty string"
        }

Missing name:

+ Request (application/json)

        {
            "price": 108,
            "quantity": 205
        }
+ Response 400 (application/json)

        {
            "code": "BAD_REQUEST",
            "message": "The server cannot process this request",
            "details": "'name' field is required for the product",
            "timestamp": "2025-03-05 18:59:06.884441 GMT+0:00",
            "request": "POST /products",
            "suggestion": "Re-send the request with an appropriate name field"
        }

Invalid price:

+ Request (application/json)

        {
            "name": "Orient Electric 9W High Glow LED bulb| Pack of 2",
            "price": -1,
            "quantity": 205
        }
+ Response 400 (application/json)

        {
            "code": "BAD_REQUEST",
            "message": "The server cannot process this request",
            "details": "'price' field is invalid",
            "timestamp": "2025-03-05 19:25:43.872771 GMT+0:00",
            "request": "POST /products",
            "suggestion": "Re-send the request with an appropriate price field, it must be a non-negative integer.             Check if you are sending a string instead"
        }

Missing price:

+ Request (application/json)

        {
            "name": "Orient Electric 9W High Glow LED bulb| Pack of 2",
            "price": -1,
            "quantity": 205
        }
+ Response 400 (application/json)

        {
            "code": "BAD_REQUEST",
            "message": "The server cannot process this request",
            "details": "'price' field is required for the product",
            "timestamp": "2025-03-05 19:27:38.548031 GMT+0:00",
            "request": "POST /products",
            "suggestion": "Re-send the request with an appropriate price field (non-negative integer)"
        }

Invalid price:

+ Request (application/json)

        {
            "name": "Orient Electric 9W High Glow LED bulb| Pack of 2",
            "price": 108,
            "quantity": -1
        }
+ Response 400 (application/json)

        {
            "code": "BAD_REQUEST",
            "message": "The server cannot process this request",
            "details": "'quantity' field is invalid",
            "timestamp": "2025-03-05 19:25:43.872771 GMT+0:00",
            "request": "POST /products",
            "suggestion": "Re-send the request with an appropriate quantity field, it must be a non-negative integer.             Check if you are sending a string instead"
        }

Missing quantity:

+ Request (application/json)

        {
            "name": "Orient Electric 9W High Glow LED bulb| Pack of 2",
            "price": 108,
        }
+ Response 400 (application/json)

        {
            "code": "BAD_REQUEST",
            "message": "The server cannot process this request",
            "details": "'quantity' field is required for the product",
            "timestamp": "2025-03-05 19:27:38.548031 GMT+0:00",
            "request": "POST /products",
            "suggestion": "Re-send the request with an appropriate quantity field (non-negative integer)"
        }

</details>        


## Product Document [/products/\<id\>]

### List a Product [GET]

+ Response 200 (application/json)

        {
            "name": "Orient Electric 9W High Glow LED bulb| Pack of 2",
            "price": 108,
            "brand": "Orient Electric",
            "category": "Appliances",
            "description": "180-degree wide beam angle| Voltage surge protection up to 4 kV| 6500K, Cool White",
            "quantity": 205,
            "id": 2
        }

### Update a Product [PATCH]

+ Request (application/json)  

        {
            "price": 120,
        }

+ Response 204 (application/json)  

        No content

### Delete a Product [DELETE]

+ Response 204 (application/json)

        No content


## Unspecified Endpoints:

Trying to access any unspecified endpoint, ie, an unspecified method on a URI that exists, returns
a typical error message.

        {
            "code": "BAD_REQUEST",
            "message": "The server cannot process this request",
            "details": "No endpoint for PUT request",
            "timestamp": "2025-03-05 18:18:32.320301 GMT+0:00",
            "request": "PUT /products",
            "suggestion": "Check the documentation at https://github.com/Alph3ga/interneers-lab for the available API endpoints"
        }
