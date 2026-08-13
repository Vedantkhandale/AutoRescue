import os
import pymysql

DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "autorescue_v2")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))

print(f"Connecting to MySQL at {DB_HOST}:{DB_PORT} as {DB_USER}")

try:
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
    conn.autocommit(True)
    with conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print(f"Database `{DB_NAME}` ensured.")
except Exception as e:
    print("Failed to ensure database:", e)
    raise
finally:
    try:
        conn.close()
    except:
        pass
