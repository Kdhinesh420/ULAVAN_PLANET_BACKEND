
import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def main():
    print("Running review verification...")
    
    # Needs valid user ID and product ID
    user_id = 1
    product_id = 5 # From previous tests
    
    review_payload = {
        "user_id": user_id,
        "product_id": product_id,
        "rating": 5,
        "comment": "Great product!"
    }
    
    print(f"Attempting to create review for Product {product_id} by User {user_id}...")
    resp = requests.post(f"{BASE_URL}/reviews/", json=review_payload)
    print(f"Status Code: {resp.status_code}")
    print(f"Response: {resp.text}")
    
    if resp.status_code == 200:
        print("SUCCESS: Review created.")
        review_data = resp.json()
        print(f"Review ID: {review_data.get('id')}")
    else:
        print("FAILURE: Review creation failed.")

if __name__ == "__main__":
    main()
