from db.session import engine
from sqlalchemy import text

def update_schema():
    try:
        with engine.connect() as conn:
            conn.execute(text('ALTER TABLE products ADD COLUMN IF NOT EXISTS image_url_2 TEXT;'))
            conn.execute(text('ALTER TABLE products ADD COLUMN IF NOT EXISTS image_url_3 TEXT;'))
            conn.commit()
            print("Database schema updated successfully (columns added if they didn't exist).")
    except Exception as e:
        print(f"Error updating schema: {e}")

if __name__ == "__main__":
    update_schema()
