from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from fastapi import Response, status
from typing import Optional, List

app = FastAPI()

products = [
    {"id": 1, "name": "Smartphone", "price": 20000, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Headphones", "price": 1500, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "T-shirt", "price": 799, "category": "Clothing", "in_stock": True},
    {"id": 4, "name": "Running Shoes", "price": 2999, "category": "Footwear", "in_stock": False},
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False},
]

feedback = []

orders = []

cart = []

class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)

class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=50)


class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem] = Field(..., min_items=1)

class NewProduct(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    category: str
    in_stock: bool = True

class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str

@app.get("/products/audit")
def product_audit():

    in_stock_list = [p for p in products if p["in_stock"]]
    out_stock_list = [p for p in products if not p["in_stock"]]

    stock_value = sum(p["price"] * 10 for p in in_stock_list)

    priciest = max(products, key=lambda p: p["price"])

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock_list),
        "out_of_stock_names": [p["name"] for p in out_stock_list],
        "total_stock_value": stock_value,
        "most_expensive": {
            "name": priciest["name"],
            "price": priciest["price"]
        }
    }

@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }

@app.get("/products/category/{category_name}")
def get_by_category(category_name: str):
    
    result = [p for p in products if p["category"] == category_name]
    
    if not result:
        return {"error": "No products found in this category"}
    
    return {
        "category": category_name,
        "products": result,
        "total": len(result)
    }

@app.get("/products/instock")
def get_instock():
    available = [p for p in products if p["in_stock"] == True]

    return {
        "in_stock_products": available,
        "count": len(available)
    }

@app.get("/store/summary")
def store_summary():
    
    in_stock_count = len([p for p in products if p["in_stock"]])
    out_stock_count = len(products) - in_stock_count

    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": in_stock_count,
        "out_of_stock": out_stock_count,
        "categories": categories
    }

@app.get("/products/search/{keyword}")
def search_products(keyword: str):

    results = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]

    if not results:
        return {"message": "No products matched your search"}

    return {
        "keyword": keyword,
        "results": results,
        "total_matches": len(results)
    }

@app.get("/products/deals")
def get_deals():

    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])

    return {
        "best_deal": cheapest,
        "premium_pick": expensive
    }

@app.get("/products/filter")
def filter_products(
    category: str = Query(None),
    max_price: int = Query(None),
    min_price: int = Query(None, description="Minimum price")
):

    result = products

    if category:
        result = [p for p in result if p["category"] == category]

    if max_price:
        result = [p for p in result if p["price"] <= max_price]

    if min_price:
        result = [p for p in result if p["price"] >= min_price]

    return {
        "filters_applied": {
            "category": category,
            "max_price": max_price,
            "min_price": min_price
        },
        "products": result,
        "total": len(result)
    }

@app.get("/products/sort")
def sort_products(
    sort_by: str = Query("price"),
    order: str = Query("asc")
):

    # ✅ Validate sort_by
    if sort_by not in ["price", "name"]:
        raise HTTPException(
            status_code=400,
            detail="sort_by must be 'price' or 'name'"
        )

    # ✅ Validate order
    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="order must be 'asc' or 'desc'"
        )

    reverse = True if order == "desc" else False

    sorted_products = sorted(
        products,
        key=lambda p: p[sort_by],
        reverse=reverse
    )

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_products
    }

@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):

    start = (page - 1) * limit
    end = start + limit

    paginated_products = products[start:end]

    total_pages = -(-len(products) // limit)  # ceiling division

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "products": paginated_products
    }

@app.get("/products/sort-by-category")
def sort_by_category():

    result = sorted(
        products,
        key=lambda p: (p["category"], p["price"])
    )

    return {
        "products": result,
        "total": len(result)
    }

@app.get("/products/browse")
def browse_products(
    keyword: str = Query(None),
    sort_by: str = Query("price"),
    order: str = Query("asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(4, ge=1, le=20),
):

    result = products
    if keyword:
        result = [
            p for p in result
            if keyword.lower() in p["name"].lower()
        ]

    if sort_by in ["price", "name"]:
        result = sorted(
            result,
            key=lambda p: p[sort_by],
            reverse=(order == "desc")
        )

    total = len(result)
    start = (page - 1) * limit
    paged = result[start: start + limit]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total,
        "total_pages": -(-total // limit),
        "products": paged
    }

@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    
    for product in products:
        if product["id"] == product_id:
            return {
                "name": product["name"],
                "price": product["price"]
            }

    return {"error": "Product not found"}

@app.put("/products/discount")
def bulk_discount(
    category: str = Query(..., description="Category to discount"),
    discount_percent: int = Query(..., ge=1, le=99, description="% off"),
):

    updated = []

    for p in products:
        if p["category"] == category:
            p["price"] = int(p["price"] * (1 - discount_percent / 100))
            updated.append(p)

    if not updated:
        return {
            "message": f"No products found in category: {category}"
        }

    return {
        "message": f"{discount_percent}% discount applied to {category}",
        "updated_count": len(updated),
        "updated_products": updated
    }

@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):
    feedback.append(data.dict())

    return {
        "message": "Feedback submitted successfully",
        "feedback": data.dict(),
        "total_feedback": len(feedback)
    }

@app.get("/products/summary")
def product_summary():
    in_stock = [p for p in products if p["in_stock"]]
    out_stock = [p for p in products if not p["in_stock"]]

    expensive = max(products, key=lambda p: p["price"])
    cheapest = min(products, key=lambda p: p["price"])

    categories = list(set(p["category"] for p in products))

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock),
        "out_of_stock_count": len(out_stock),
        "most_expensive": {
            "name": expensive["name"],
            "price": expensive["price"]
        },
        "cheapest": {
            "name": cheapest["name"],
            "price": cheapest["price"]
        },
        "categories": categories
    }

@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):

    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:

        product = next((p for p in products if p["id"] == item.product_id), None)

        if not product:
            failed.append({
                "product_id": item.product_id,
                "reason": "Product not found"
            })

        elif not product["in_stock"]:
            failed.append({
                "product_id": item.product_id,
                "reason": f"{product['name']} is out of stock"
            })

        else:
            subtotal = product["price"] * item.quantity
            grand_total += subtotal

            confirmed.append({
                "product": product["name"],
                "qty": item.quantity,
                "subtotal": subtotal
            })

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }

@app.post("/orders")
def place_order(order: dict):

    order_id = len(orders) + 1

    new_order = {
        "order_id": order_id,
        "items": order.get("items", []),
        "status": "pending"   
    }

    orders.append(new_order)

    return {
        "message": "Order placed successfully",
        "order": new_order
    }

@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):

    results = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not results:
        return {
            "message": f"No orders found for: {customer_name}"
        }

    return {
        "customer_name": customer_name,
        "total_found": len(results),
        "orders": results
    }

@app.get("/orders/page")
def get_orders_paged(
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1, le=20),
):

    start = (page - 1) * limit

    return {
        "page": page,
        "limit": limit,
        "total": len(orders),
        "total_pages": -(-len(orders) // limit),
        "orders": orders[start: start + limit],
    }

@app.get("/orders/{order_id}")
def get_order(order_id: int):

    for order in orders:
        if order["order_id"] == order_id:
            return {"order": order}

    return {"error": "Order not found"}

@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):

    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = "confirmed"

            return {
                "message": "Order confirmed",
                "order": order
            }

    return {"error": "Order not found"}

@app.post("/products", status_code=201)
def add_product(product: NewProduct):
    for p in products:
        if p["name"].lower() == product.name.lower():
            raise HTTPException(
                status_code=400,
                detail="Product already exists"
            )
    
    next_id = max(p["id"] for p in products) + 1 if products else 1

    new_product = {
        "id": next_id,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "in_stock": product.in_stock
    }

    products.append(new_product)

    return {
        "message": "Product added",
        "product": new_product
    }

@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    price: int = None,
    in_stock: bool = None
):

    for product in products:
        if product["id"] == product_id:

            if price is not None:
                product["price"] = price

            if in_stock is not None:
                product["in_stock"] = in_stock

            return {
                "message": "Product updated",
                "product": product
            }

    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
def delete_product(product_id: int, response: Response):

    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {
                "message": f"Product '{product['name']}' deleted"
            }

    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "Product not found"}

@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int):

    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not product["in_stock"]:
        raise HTTPException(
            status_code=400,
            detail=f"{product['name']} is out of stock"
        )

    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            item["subtotal"] = item["quantity"] * item["unit_price"]

            return {
                "message": "Cart updated",
                "cart_item": item
            }

    subtotal = product["price"] * quantity

    cart_item = {
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": subtotal
    }

    cart.append(cart_item)

    return {
        "message": "Added to cart",
        "cart_item": cart_item
    }

@app.get("/cart")
def view_cart():

    grand_total = sum(item["subtotal"] for item in cart)

    return {
        "items": cart,
        "item_count": len(cart),
        "grand_total": grand_total
    }

@app.delete("/cart/{product_id}")
def remove_from_cart(product_id: int):

    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            return {"message": f"{item['product_name']} removed from cart"}

    raise HTTPException(status_code=404, detail="Item not in cart")

@app.post("/cart/checkout")
def checkout(data: CheckoutRequest):

    if not cart:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty — add items first"
        )

    created_orders = []
    order_id_start = len(orders) + 1

    for i, item in enumerate(cart):
        order = {
            "order_id": order_id_start + i,
            "customer_name": data.customer_name,
            "delivery_address": data.delivery_address,
            "product": item["product_name"],
            "quantity": item["quantity"],
            "total_price": item["subtotal"]
        }

        orders.append(order)
        created_orders.append(order)

    cart.clear()  

    return {
        "message": "Order placed successfully",
        "orders_placed": created_orders,
        "total_orders": len(created_orders)
    }

@app.get("/orders")
def get_orders():
    return {"orders": orders}