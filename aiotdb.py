import sqlite3
import os

DB_NAME = "aiotdb.db"

def setup_database():
    """Initialize database and create sensors table"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temp REAL NOT NULL,
            humidity REAL NOT NULL,
            mac TEXT,
            ip TEXT,
            device_name TEXT,
            type TEXT DEFAULT 'SIMULATED'
        )
    ''')
    conn.commit()
    conn.close()
    print(f"[DB] Database {DB_NAME} initialized.")

def insert_data(temp, humidity, mac=None, ip=None, device_name=None, data_type='SIMULATED'):
    """Insert sensor data with metadata into the database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sensors (temp, humidity, mac, ip, device_name, type) VALUES (?, ?, ?, ?, ?, ?)",
        (temp, humidity, mac, ip, device_name, data_type)
    )
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return record_id

if __name__ == "__main__":
    # Test code
    setup_database()
    rid = insert_data(25.5, 60.0, "AA:BB:CC:DD:EE:FF", "192.168.1.100", "Sim-Device")
    print(f"Test write successful, ID: {rid}")
