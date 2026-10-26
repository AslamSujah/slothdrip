import sqlite3
from datetime import datetime

DB = "slothdrip_plants.db"

def _conn():
    c = sqlite3.connect(DB)
    c.execute("""CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT, plant TEXT, days_since_watered REAL, avg_temp_c REAL,
        humidity_pct REAL, soil_type TEXT, p_water REAL, verdict TEXT,
        note TEXT, watered INTEGER DEFAULT 0)""")
    return c

def add_log(plant, days, temp, hum, soil, p, verdict, note, watered=False):
    with _conn() as c:
        c.execute("INSERT INTO logs(ts,plant,days_since_watered,avg_temp_c,humidity_pct,soil_type,p_water,verdict,note,watered) VALUES(?,?,?,?,?,?,?,?,?,?)",
                  (datetime.now().isoformat(timespec="seconds"), plant, days, temp, hum, soil, p, verdict, note, int(watered)))

def get_logs(limit=50):
    with _conn() as c:
        return c.execute("SELECT ts,plant,days_since_watered,avg_temp_c,humidity_pct,soil_type,p_water,verdict,note,watered FROM logs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
