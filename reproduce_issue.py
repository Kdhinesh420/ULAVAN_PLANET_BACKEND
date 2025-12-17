
import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def create_product(product_data):
    response = requests.post(f"{BASE_URL}/products/addproduct", json=product_data)
    return response

def main():
    print("Running verification script...")
    
    product_data_invalid_cat = {
        "name": "Test Product Invalid Cat",
        "description": "This should now fail with 404",
        "price": 10.0,
        "category_id": 999999
    }
    
    print(f"\nAttempting to create product with invalid category_id: {product_data_invalid_cat}")
    response = create_product(product_data_invalid_cat)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 404 and "Category not found" in response.text:
         print("SUCCESS: Received expected 404 error for invalid category.")
    elif response.status_code == 200:
         print("FAILURE: Product still created with invalid category!")
    elif response.status_code == 500:
         print("FAILURE: Server error (Original FK violation still happening or new error).")
    else:
         print(f"Unexpected status: {response.status_code}")

if __name__ == "__main__":
    main()
