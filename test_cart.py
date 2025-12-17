
import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def create_valid_category_and_product():
    # 1. Create Category
    # We can't easily create a category via API if there's no endpoint shown in previous file views (I only saw Product/User/Cart routes).
    # Checking main.py: app.include_router(category_router)
    # I haven't seen category_router code, but let's assume standard REST if it exists.
    # If not, I'll insert via SqlAlchemy directly or just hope ID 1 exists.
    # Actually, from the previous error `ForeignKeyViolation`, I know I need a valid category ID.
    # Let's try to create one if the endpoint exists, or assume ID 1 is valid or try to find a valid one.
    # I'll try to create a product with category_id=1. If it fails with FK violation, I'll know.
    # BUT, I just fixed product creation to return 404 if category missing.
    # So I need a valid category.
    # Let's inspect category routes quickly? No, let's just try to insert one if I can, or use row SQL.
    # Actually, let's use the DB session directly in a separate script or just try to find an existing one.
    # FOR NOW, I will try to use category_id=1.
    pass

def setup_test_data():
    # Create a user
    user_data = {
        "username": "testuser_cart",
        "email": "cart_test@example.com",
        "password": "password123",
        "phone": "1234567890",
        "address": "123 Test St"
    }
    # User creation endpoint? routers/user_routes.py was imported in main.
    # Assuming POST /users/
    # I'll check user_routes if this fails.
    user_resp = requests.post(f"{BASE_URL}/users/", json=user_data) 
    # If user already exists (400), we probably should get its ID.
    # Or just login.
    # Let's assume we can get a user.
    pass

# To make this robust, let's just use the reproduction script approach but focused on cart.
# I need correct User ID and Product ID.
# Since I don't want to over-engineer the test data setup blindly, I'll try to use existing IDs if possible or create fresh ones.
# Let's just create a quick cleaner script.

print("Please run this script after ensuring a User (id=1) and Product (id=1) exist, or adjust IDs.")
# Actually, I can't rely on user verification if I don't know the IDs.
# Let's query the DB for first user and product?
# Or just try to create them via API.

def main():
    print("Running cart verification...")
    
    # 1. Create a User
    user_payload = {
        "username": "cart_tester",
        "email": "cart_tester@example.com",
        "password": "securepassword",
        "phone": "555-0199",
        "address": "Cart Lane"
    }
    # main.py: app.include_router(userrouter) -> prefix?
    # view_file for user_routes wasn't called. I'll guess /users or /auth/register.
    # safe bet: `userrouter = APIRouter(prefix="/users", ...)`
    
    # Let's try to register.
    resp = requests.post(f"{BASE_URL}/users/register", json=user_payload)
    if resp.status_code == 404:
        resp = requests.post(f"{BASE_URL}/users/", json=user_payload)
    
    if resp.status_code in [200, 201]:
        print("User created.")
        user_id = resp.json().get("id") or resp.json().get("user_id") # adapt to schema
    elif resp.status_code == 400 and "already registered" in resp.text:
        print("User likely exists.")
        # We need an ID. If we can't get it, we might fail.
        # Let's assume ID 1 exists for this environment.
        user_id = 1
    else:
        print(f"User creation failed: {resp.status_code} {resp.text}")
        user_id = 1 # Fallback
        
    # 2. Create a Product
    # categories...
    # I'll create a product with NO category_id since that's optional now (or should be).
    # Wait, I made it optional in schema, but earlier `add_product` logic:
    # if product.category_id: ...
    # So if I omit it, it sends None, validation skips, and Product is created with Null category. Perfect.
    
    prod_payload = {
        "name": "Cart Test Product",
        "description": "For testing cart",
        "price": 50.0
        # No category_id
    }
    
    resp = requests.post(f"{BASE_URL}/products/addproduct", json=prod_payload)
    if resp.status_code == 200:
        print("Product created.")
        prod_data = resp.json()
        product_id = prod_data.get("id") or prod_data.get("product_id")
    else:
        print(f"Product creation failed: {resp.status_code} {resp.text}")
        product_id = 1 # Fallback

    if not user_id or not product_id:
        print("Cannot proceed without User ID and Product ID.")
        return

    print(f"Testing with User ID: {user_id}, Product ID: {product_id}")

    # 3. Add to Cart
    # POST /cart/add?user_id=X&product_id=Y&quantity=1
    resp = requests.post(f"{BASE_URL}/cart/add", params={"user_id": user_id, "product_id": product_id, "quantity": 2})
    print(f"Add to Cart: {resp.status_code} {resp.text}")
    
    if resp.status_code == 200:
        print("SUCCESS: Item added to cart.")
    else:
        print("FAILURE: Could not add to cart.")

    # 4. View Cart
    # GET /cart/view/{user_id}
    resp = requests.get(f"{BASE_URL}/cart/view/{user_id}")
    print(f"View Cart: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        items = data.get("items", [])
        found = any(item['product_id'] == product_id for item in items)
        if found:
            print(f"SUCCESS: verified item in cart. Items: {len(items)}")
        else:
            print("FAILURE: Item not found in cart view.")
    else:
        print(f"FAILURE: Could not view cart. {resp.text}")

if __name__ == "__main__":
    main()
