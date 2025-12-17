from fastapi import FastAPI, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from dependencies import get_db
from models.User import User
from models.Product import Product
from models.Cart import Cart

cartrouter = APIRouter(prefix="/cart", tags=["Carts"])
@cartrouter.post("/add")
def add_to_cart(user_id: int, product_id: int, quantity: int = 1, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Check if product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # Create cart entry
    cart_item = Cart(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity
    )
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return {"message": "Item added to cart"}

@cartrouter.get("/view/{user_id}")
def view_cart(user_id: int, db: Session = Depends(get_db)):
    query = text("""
        SELECT 
            cart.cart_id,
            cart.product_id,
            cart.quantity,
            products.name AS product_name,
            products.price,
            products.description,
            products.image_url,
            categories.name AS category_name,
            users.username AS user_name,
            users.phone,
            users.address
        FROM cart
        JOIN products ON cart.product_id = products.id
        LEFT JOIN categories ON products.category_id = categories.category_id
        JOIN users ON cart.user_id = users.id
        WHERE cart.user_id = :user_id
    """)

    results = db.execute(query, {"user_id": user_id}).fetchall()

    if not results:
        return {"message": "Cart is empty"}

    cart_items = []
    for row in results:
        cart_items.append({
            "cart_id": row[0],
            "product_id": row[1],
            "quantity": row[2],
            "product_name": row[3],
            "price": float(row[4]),
            "description": row[5],
            "image_url": row[6],
            "category_name": row[7],
            "user_name": row[8],
            "phone": row[9],
            "address": row[10],
            "total": float(row[4]) * row[2]
        })

    return {
        "user_id": user_id,
        "items": cart_items
    }

@cartrouter.delete("/remove/{cart_id}")
def remove_from_cart(cart_id: int, db: Session = Depends(get_db)):
    cart_item = db.query(Cart).filter(Cart.cart_id == cart_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}

@cartrouter.put("/update/{cart_id}")
def update_cart_item(cart_id: int, quantity: int, db: Session = Depends(get_db)):
    cart_item = db.query(Cart).filter(Cart.cart_id == cart_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    cart_item.quantity = quantity
    db.commit()
    return {"message": "Cart item updated"}

@cartrouter.get("/get")
def get_cart(user_id: int, db: Session = Depends(get_db)):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart_items


