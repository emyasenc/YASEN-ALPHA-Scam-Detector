import sqlite3
from datetime import datetime
from pathlib import Path

class StatsDB:
    def __init__(self, db_path="stats.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database with a stats table."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_predictions INTEGER DEFAULT 0,
                scam_count INTEGER DEFAULT 0,
                confidence_sum REAL DEFAULT 0.0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Insert initial row if empty
        cursor.execute("SELECT COUNT(*) FROM stats")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO stats (total_predictions, scam_count, confidence_sum)
                VALUES (0, 0, 0.0)
            """)
        conn.commit()
        conn.close()

    def update(self, is_scam, probability):
        """Update stats after a prediction."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE stats
            SET total_predictions = total_predictions + 1,
                scam_count = scam_count + ?,
                confidence_sum = confidence_sum + ?,
                last_updated = CURRENT_TIMESTAMP
            WHERE id = 1
        """, (1 if is_scam else 0, probability))
        conn.commit()
        conn.close()

    def get_stats(self):
        """Get current stats from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT total_predictions, scam_count, confidence_sum, last_updated
            FROM stats WHERE id = 1
        """)
        row = cursor.fetchone()
        conn.close()

        if row:
            total, scam_count, confidence_sum, last_updated = row
            scam_rate = scam_count / total if total > 0 else 0
            avg_confidence = confidence_sum / total if total > 0 else 0
            return {
                "total_predictions": total,
                "scam_count": scam_count,
                "scam_rate": round(scam_rate, 4),
                "avg_confidence": round(avg_confidence, 4),
                "last_updated": last_updated
            }
        return None