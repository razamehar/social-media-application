from typing import Tuple

def create_tables(conn, cur):
    #conn, cur = db  # Unpack the connection and cursor


    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY NOT NULL,
            email VARCHAR NOT NULL UNIQUE,
            password VARCHAR NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100),
            content VARCHAR(300),
            published BOOLEAN,
            created_on TIMESTAMPTZ DEFAULT NOW(),
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            PRIMARY KEY (post_id, user_id)
        )
    """)

    # Commit changes and close the connection properly
    conn.commit()
    cur.close()
    conn.close()
