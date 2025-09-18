from sqlalchemy import create_engine, text

# IMPORTANT: use the encoded password
DATABASE_URL = "mysql+pymysql://root:%4039295937Nrb%21@127.0.0.1:3306/ecommerce_db"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DATABASE();"))
        for row in result:
            print("✅ Connected to database:", row[0])
except Exception as e:
    print("❌ Connection failed:", e)
