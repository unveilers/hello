#!/usr/bin/env python3
import requests
import json

API_URL = "http://localhost:8000/api"

user_data = {
    "username": "admin",
    "email": "admin@ghiblicloset.com",
    "password": "admin123",
    "full_name": "Admin User"
}

print("Registering admin user...")
response = requests.post(f"{API_URL}/auth/register", json=user_data)
if response.status_code == 200:
    token = response.json()["access_token"]
    print("✅ Admin user registered successfully")
else:
    login_data = {"username": "admin", "password": "admin123"}
    response = requests.post(f"{API_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Admin user logged in successfully")
    else:
        print("❌ Failed to authenticate admin user")
        exit(1)

headers = {"Authorization": f"Bearer {token}"}

new_products = [
    {
        "name": "Calcifer Fire Spirit Hoodie",
        "description": "Warm hoodie featuring the lovable fire demon Calcifer from Howl's Moving Castle. Perfect for staying cozy while channeling magical energy.",
        "price": 52.99,
        "character": "calcifer",
        "clothing_type": "hoodie",
        "image_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=500&h=500&fit=crop",
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "colors": ["Orange", "Red", "Yellow"],
        "stock": 40
    },
    {
        "name": "Catbus Adventure T-Shirt",
        "description": "Comfortable t-shirt featuring the magical Catbus from My Neighbor Totoro. Great for everyday adventures and forest explorations.",
        "price": 28.99,
        "character": "catbus",
        "clothing_type": "t-shirt",
        "image_url": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500&h=500&fit=crop",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "colors": ["Gray", "Brown", "Black"],
        "stock": 60
    },
    {
        "name": "Ashitaka Warrior Jacket",
        "description": "Rugged jacket inspired by Prince Ashitaka from Princess Mononoke. Built for outdoor adventures and connecting with nature.",
        "price": 95.99,
        "character": "ashitaka",
        "clothing_type": "jacket",
        "image_url": "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=500&h=500&fit=crop",
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Forest Green", "Earth Brown", "Navy Blue"],
        "stock": 20
    },
    {
        "name": "Sophie's Magical Dress",
        "description": "Elegant dress inspired by Sophie's transformation in Howl's Moving Castle. Perfect for special occasions and magical moments.",
        "price": 68.99,
        "character": "sophie",
        "clothing_type": "dress",
        "image_url": "https://images.unsplash.com/photo-1566479179817-c0b5b4b8b1c5?w=500&h=500&fit=crop",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "colors": ["Sky Blue", "Lavender", "White"],
        "stock": 35
    },
    {
        "name": "Totoro Forest Pants",
        "description": "Comfortable pants perfect for forest walks and nature adventures, inspired by Totoro's peaceful woodland home.",
        "price": 38.99,
        "character": "totoro",
        "clothing_type": "pants",
        "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=500&h=500&fit=crop",
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "colors": ["Forest Green", "Gray", "Brown"],
        "stock": 45
    },
    {
        "name": "Kiki's Witch Skirt",
        "description": "Flowing skirt inspired by Kiki's witch outfit. Perfect for young witches starting their delivery service adventures.",
        "price": 44.99,
        "character": "kiki",
        "clothing_type": "skirt",
        "image_url": "https://images.unsplash.com/photo-1583496661160-fb5886a13d44?w=500&h=500&fit=crop",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "colors": ["Deep Purple", "Black", "Navy Blue"],
        "stock": 30
    },
    {
        "name": "Ponyo Ocean Accessories Set",
        "description": "Magical accessories set inspired by Ponyo's underwater world. Includes hair clips, bracelet, and ocean-themed charms.",
        "price": 24.99,
        "character": "ponyo",
        "clothing_type": "accessories",
        "image_url": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=500&h=500&fit=crop",
        "sizes": ["One Size"],
        "colors": ["Ocean Blue", "Coral Pink", "Pearl White"],
        "stock": 50
    },
    {
        "name": "Chihiro Spirit World Sweater",
        "description": "Mystical sweater featuring designs from the spirit world in Spirited Away. Warm and magical for everyday wear.",
        "price": 48.99,
        "character": "chihiro",
        "clothing_type": "sweater",
        "image_url": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=500&h=500&fit=crop",
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Midnight Purple", "Spirit Gold", "Mystic Blue"],
        "stock": 25
    }
]

print(f"\nAdding {len(new_products)} new Studio Ghibli products...")

for i, product in enumerate(new_products, 1):
    print(f"Adding product {i}/{len(new_products)}: {product['name']}")
    response = requests.post(f"{API_URL}/products", json=product, headers=headers)
    
    if response.status_code == 200:
        print(f"✅ Successfully added: {product['name']}")
    else:
        print(f"❌ Failed to add: {product['name']} - {response.status_code}")
        print(f"   Error: {response.text}")

print(f"\n🎉 Finished adding products! Check the website to see the new items.")
