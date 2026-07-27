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


def get_all_tasks():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, done FROM tasks"
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "done": row[2]
        }
        for row in rows
    ]


def get_task_by_id(task_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, done FROM tasks WHERE id = %s",
        (task_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return {
            "id": row[0],
            "title": row[1],
            "done": row[2]
        }

    return None


def create_task(title: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, done)
        VALUES (%s, %s)
        RETURNING id, title, done
        """,
        (title, False)
    )

    row = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }


def update_task(task_id: int, title=None, done=None):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, done FROM tasks WHERE id = %s",
        (task_id,)
    )

    existing = cursor.fetchone()

    if existing is None:
        cursor.close()
        conn.close()
        return None

    if title is not None:
        cursor.execute(
            """
            UPDATE tasks
            SET title = %s
            WHERE id = %s
            """,
            (title, task_id)
        )

    if done is not None:
        cursor.execute(
            """
            UPDATE tasks
            SET done = %s
            WHERE id = %s
            """,
            (done, task_id)
        )

    conn.commit()

    cursor.execute(
        "SELECT id, title, done FROM tasks WHERE id = %s",
        (task_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }


def delete_task(task_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM tasks WHERE id = %s",
        (task_id,)
    )

    task = cursor.fetchone()

    if task is None:
        cursor.close()
        conn.close()
        return False

    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return True