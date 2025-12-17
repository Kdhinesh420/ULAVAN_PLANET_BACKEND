
import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def main():
    print("Running order verification...")
    
    # Needs valid user ID and product ID
    # Assuming IDs from previous tests might exist, but safer to assume 1.
    user_id = 1
    
    # 1. Create Data (minimal)
    order_payload = {
        "user_id": user_id,
        "total_amount": 100.0,
        "status": "pending",
        "items": [
            {
                "product_id": 5, # From cart test success
                "quantity": 2,
                "price": 50.0
            }
        ]
    }
    
    print(f"Attempting to create order for User {user_id}...")
    resp = requests.post(f"{BASE_URL}/orders/", json=order_payload)
    print(f"Status Code: {resp.status_code}")
    print(f"Response: {resp.text}")
    
    if resp.status_code == 200:
        print("SUCCESS: Order created.")
        order_data = resp.json()
        print(f"Order ID: {order_data.get('id')}")
    else:
        print("FAILURE: Order creation failed.")

if __name__ == "__main__":
    main()
