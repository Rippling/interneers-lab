# API Documentation:

## Products Collection [/products]

### List All products [GET]

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

## Product Document [/products/<id>]

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