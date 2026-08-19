from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg:///watch_next"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

# with engine.connect() as connection:
#     result = connection.execute(
#         text("SELECT * FROM users;")
#     )

#     for row in result:
#         print(row)
