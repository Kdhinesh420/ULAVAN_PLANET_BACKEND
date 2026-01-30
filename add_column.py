from sqlalchemy import text
from db.session import engine

def add_column():
    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE products ADD COLUMN images TEXT"))
            conn.commit()
            print("Column 'images' added successfully.")
    except Exception as e:
        print(f"Error (might already exist): {e}")

if __name__ == "__main__":
    add_column()
