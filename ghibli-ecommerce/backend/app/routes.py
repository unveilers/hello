from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from .main import (
    users_collection, products_collection, carts_collection, comments_collection,
    User, UserCreate, UserLogin, Product, ProductCreate, 
    CartItem, CartItemCreate, Comment, CommentCreate,
    hash_password, verify_password, create_access_token, get_current_user
)

router = APIRouter()

@router.post("/auth/register", response_model=dict)
async def register(user_data: UserCreate):
    existing_username = await users_collection.find_one({"username": user_data.username})
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    existing_email = await users_collection.find_one({"email": user_data.email})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user_data.password)
    user = {
        "username": user_data.username,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    }
    result = await users_collection.insert_one(user)
    user["id"] = str(result.inserted_id)
    
    access_token = create_access_token(data={"sub": user["username"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "full_name": user["full_name"]
        }
    }

@router.post("/auth/login", response_model=dict)
async def login(user_data: UserLogin):
    user = await users_collection.find_one({"username": user_data.username})
    if not user or not verify_password(user_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user["username"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"],
            "full_name": user["full_name"]
        }
    }

@router.get("/products", response_model=List[Product])
async def get_products(character: Optional[str] = None, clothing_type: Optional[str] = None):
    filter_query = {}
    if character:
        filter_query["character"] = character
    if clothing_type:
        filter_query["clothing_type"] = clothing_type
    
    products = []
    async for product in products_collection.find(filter_query):
        product["id"] = str(product["_id"])
        del product["_id"]
        products.append(product)
    
    return products

@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    try:
        product = await products_collection.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product["id"] = str(product["_id"])
        del product["_id"]
        return product
    except:
        raise HTTPException(status_code=404, detail="Product not found")

@router.post("/products", response_model=Product)
async def create_product(product_data: ProductCreate, current_user: dict = Depends(get_current_user)):
    product = {
        "name": product_data.name,
        "description": product_data.description,
        "price": product_data.price,
        "character": product_data.character,
        "clothing_type": product_data.clothing_type,
        "image_url": product_data.image_url,
        "sizes": product_data.sizes,
        "colors": product_data.colors,
        "stock": product_data.stock,
        "created_at": datetime.utcnow()
    }
    result = await products_collection.insert_one(product)
    product["id"] = str(result.inserted_id)
    return product

@router.get("/cart", response_model=List[CartItem])
async def get_cart(current_user: dict = Depends(get_current_user)):
    cart_items = []
    async for item in carts_collection.find({"user_id": current_user["id"]}):
        item["id"] = str(item["_id"])
        del item["_id"]
        cart_items.append(item)
    return cart_items

@router.post("/cart", response_model=CartItem)
async def add_to_cart(item_data: CartItemCreate, current_user: dict = Depends(get_current_user)):
    try:
        product = await products_collection.find_one({"_id": ObjectId(item_data.product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
    except:
        raise HTTPException(status_code=404, detail="Product not found")
    
    existing_item = await carts_collection.find_one({
        "user_id": current_user["id"],
        "product_id": item_data.product_id,
        "size": item_data.size,
        "color": item_data.color
    })
    
    if existing_item:
        await carts_collection.update_one(
            {"_id": existing_item["_id"]},
            {"$inc": {"quantity": item_data.quantity}}
        )
        existing_item["quantity"] += item_data.quantity
        existing_item["id"] = str(existing_item["_id"])
        del existing_item["_id"]
        return existing_item
    
    cart_item = {
        "user_id": current_user["id"],
        "product_id": item_data.product_id,
        "quantity": item_data.quantity,
        "size": item_data.size,
        "color": item_data.color,
        "added_at": datetime.utcnow()
    }
    result = await carts_collection.insert_one(cart_item)
    cart_item["id"] = str(result.inserted_id)
    return cart_item

@router.put("/cart/{item_id}")
async def update_cart_item(item_id: str, quantity: int, current_user: dict = Depends(get_current_user)):
    try:
        cart_item = await carts_collection.find_one({
            "_id": ObjectId(item_id),
            "user_id": current_user["id"]
        })
        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        
        if quantity <= 0:
            await carts_collection.delete_one({"_id": ObjectId(item_id)})
            return {"message": "Item removed from cart"}
        
        await carts_collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": {"quantity": quantity}}
        )
        cart_item["quantity"] = quantity
        cart_item["id"] = str(cart_item["_id"])
        del cart_item["_id"]
        return cart_item
    except:
        raise HTTPException(status_code=404, detail="Cart item not found")

@router.delete("/cart/{item_id}")
async def remove_from_cart(item_id: str, current_user: dict = Depends(get_current_user)):
    try:
        cart_item = await carts_collection.find_one({
            "_id": ObjectId(item_id),
            "user_id": current_user["id"]
        })
        if not cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        
        await carts_collection.delete_one({"_id": ObjectId(item_id)})
        return {"message": "Item removed from cart"}
    except:
        raise HTTPException(status_code=404, detail="Cart item not found")

@router.get("/products/{product_id}/comments", response_model=List[Comment])
async def get_product_comments(product_id: str):
    comments = []
    async for comment in comments_collection.find({"product_id": product_id}).sort("created_at", -1):
        comment["id"] = str(comment["_id"])
        del comment["_id"]
        comments.append(comment)
    return comments

@router.post("/comments", response_model=Comment)
async def create_comment(comment_data: CommentCreate, current_user: dict = Depends(get_current_user)):
    try:
        product = await products_collection.find_one({"_id": ObjectId(comment_data.product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
    except:
        raise HTTPException(status_code=404, detail="Product not found")
    
    comment = {
        "user_id": current_user["id"],
        "product_id": comment_data.product_id,
        "username": current_user["username"],
        "content": comment_data.content,
        "rating": comment_data.rating,
        "created_at": datetime.utcnow()
    }
    result = await comments_collection.insert_one(comment)
    comment["id"] = str(result.inserted_id)
    return comment
