import os
import psycopg
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_db():
    return psycopg.connect(DATABASE_URL)


def create_tables():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


def seed_tasks():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            """
            INSERT INTO tasks (title, done)
            VALUES (%s, %s)
            """,
            [
                ("Learn FastAPI", False),
                ("Build CRUD API", False),
                ("Submit FlyRank assignment", True)
            ]
        )

        conn.commit()

    cursor.close()
    conn.close()