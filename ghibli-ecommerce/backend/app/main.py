from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
from typing import Optional, List
import bcrypt
from jose import jwt
import os
from pydantic import BaseModel, Field
from enum import Enum

app = FastAPI(title="Ghibli Clothing Store API")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "ghibli_ecommerce"

client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]

users_collection = database.users
products_collection = database.products
carts_collection = database.carts
comments_collection = database.comments
orders_collection = database.orders

SECRET_KEY = "ghibli-secret-key-for-development"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    created_at: datetime

class GhibliCharacter(str, Enum):
    TOTORO = "totoro"
    CHIHIRO = "chihiro"
    HOWL = "howl"
    SOPHIE = "sophie"
    KIKI = "kiki"
    PONYO = "ponyo"
    SAN = "san"
    ASHITAKA = "ashitaka"
    CALCIFER = "calcifer"
    CATBUS = "catbus"

class ClothingType(str, Enum):
    TSHIRT = "t-shirt"
    HOODIE = "hoodie"
    SWEATER = "sweater"
    DRESS = "dress"
    JACKET = "jacket"
    PANTS = "pants"
    SKIRT = "skirt"
    ACCESSORIES = "accessories"

class Product(BaseModel):
    id: str
    name: str
    description: str
    price: float
    character: GhibliCharacter
    clothing_type: ClothingType
    image_url: str
    sizes: List[str]
    colors: List[str]
    stock: int
    created_at: datetime

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    character: GhibliCharacter
    clothing_type: ClothingType
    image_url: str
    sizes: List[str] = ["S", "M", "L", "XL"]
    colors: List[str] = ["Black", "White", "Navy"]
    stock: int = 100

class CartItem(BaseModel):
    id: str
    user_id: str
    product_id: str
    quantity: int
    size: str
    color: str
    added_at: datetime

class CartItemCreate(BaseModel):
    product_id: str
    quantity: int = 1
    size: str
    color: str

class Comment(BaseModel):
    id: str
    user_id: str
    product_id: str
    username: str
    content: str
    rating: int = Field(ge=1, le=5)
    created_at: datetime

class CommentCreate(BaseModel):
    product_id: str
    content: str
    rating: int = Field(ge=1, le=5)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        user = await users_collection.find_one({"username": username})
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        user["id"] = str(user["_id"])
        return user
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

async def init_sample_data():
    existing_products = await products_collection.count_documents({})
    if existing_products > 0:
        return
    
    sample_products = [
        {
            "name": "Totoro Forest Spirit T-Shirt",
            "description": "Soft cotton t-shirt featuring the beloved forest spirit Totoro from My Neighbor Totoro. Perfect for nature lovers and Ghibli fans.",
            "price": 24.99,
            "character": "totoro",
            "clothing_type": "t-shirt",
            "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["Forest Green", "Gray", "White"],
            "stock": 50,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Chihiro's Adventure Hoodie",
            "description": "Cozy hoodie inspired by Chihiro's journey in Spirited Away. Features mystical spirit world designs.",
            "price": 45.99,
            "character": "chihiro",
            "clothing_type": "hoodie",
            "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500&h=500&fit=crop",
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "colors": ["Midnight Blue", "Purple", "Black"],
            "stock": 30,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Howl's Moving Castle Jacket",
            "description": "Elegant jacket inspired by Howl's magical style. Perfect for those who want to add a touch of magic to their wardrobe.",
            "price": 89.99,
            "character": "howl",
            "clothing_type": "jacket",
            "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&h=500&fit=crop",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["Emerald Green", "Royal Blue", "Black"],
            "stock": 25,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Kiki's Delivery Service Dress",
            "description": "Charming dress inspired by Kiki's witch outfit. Perfect for everyday magic and special occasions.",
            "price": 55.99,
            "character": "kiki",
            "clothing_type": "dress",
            "image_url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500&h=500&fit=crop",
            "sizes": ["XS", "S", "M", "L", "XL"],
            "colors": ["Deep Purple", "Navy Blue", "Black"],
            "stock": 40,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Ponyo Ocean Wave Sweater",
            "description": "Soft sweater featuring ocean wave patterns inspired by Ponyo's underwater world.",
            "price": 39.99,
            "character": "ponyo",
            "clothing_type": "sweater",
            "image_url": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=500&h=500&fit=crop",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["Ocean Blue", "Coral Pink", "White"],
            "stock": 35,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Princess Mononoke Forest Pants",
            "description": "Comfortable pants inspired by San's connection to nature. Perfect for outdoor adventures.",
            "price": 42.99,
            "character": "san",
            "clothing_type": "pants",
            "image_url": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=500&h=500&fit=crop",
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "colors": ["Forest Green", "Earth Brown", "Black"],
            "stock": 45,
            "created_at": datetime.utcnow()
        }
    ]
    
    await products_collection.insert_many(sample_products)

@app.on_event("startup")
async def startup_event():
    await init_sample_data()

from .routes import router
app.include_router(router, prefix="/api")

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/")
async def root():
    products_count = await products_collection.count_documents({})
    return {"message": "Welcome to Ghibli Clothing Store API", "products_count": products_count}
