import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, Any, List

class Database:
    def __init__(self, db_uri: str = "sqlite:///mira.db"):
        self.db_path = db_uri.replace("sqlite:///", "")
        self.conn = None
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Users table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                language TEXT DEFAULT 'he',
                warns INTEGER DEFAULT 0,
                notes TEXT DEFAULT '[]',
                notes_count INTEGER DEFAULT 0,
                is_blocked INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Groups table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                group_id INTEGER PRIMARY KEY,
                title TEXT,
                username TEXT,
                language TEXT DEFAULT 'he',
                welcome TEXT,
                welcome_enabled INTEGER DEFAULT 1,
                rules TEXT,
                locks TEXT DEFAULT '{}',
                filters TEXT DEFAULT '{}',
                blocklist TEXT DEFAULT '[]',
                antiflood INTEGER DEFAULT 0,
                flood_limit INTEGER DEFAULT 5,
                captcha INTEGER DEFAULT 0,
                captcha_time INTEGER DEFAULT 60,
                warns_limit INTEGER DEFAULT 3,
                staff TEXT DEFAULT '[]',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Chat history for AI
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                group_id INTEGER,
                message TEXT,
                response TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Notes table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER,
                name TEXT,
                content TEXT,
                file_id TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Filters table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS filters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER,
                keyword TEXT,
                response TEXT,
                file_id TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Warns table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS warns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                group_id INTEGER,
                reason TEXT,
                warned_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Captcha table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS captcha (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                group_id INTEGER,
                code TEXT,
                solved INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user from database"""
        self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                "user_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "username": row[3],
                "language": row[4],
                "warns": row[5],
                "notes": json.loads(row[6]),
                "notes_count": row[7],
                "is_blocked": row[8],
                "created_at": row[9],
            }
        return None
    
    def add_user(self, user_id: int, first_name: str, last_name: str = None, username: str = None):
        """Add new user to database"""
        self.cursor.execute("""
            INSERT OR IGNORE INTO users (user_id, first_name, last_name, username)
            VALUES (?, ?, ?, ?)
        """, (user_id, first_name, last_name, username))
        self.conn.commit()
    
    def update_user(self, user_id: int, **kwargs):
        """Update user data"""
        fields = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values()) + [user_id]
        self.cursor.execute(f"UPDATE users SET {fields} WHERE user_id = ?", values)
        self.conn.commit()
    
    def get_group(self, group_id: int) -> Optional[Dict]:
        """Get group from database"""
        self.cursor.execute("SELECT * FROM groups WHERE group_id = ?", (group_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                "group_id": row[0],
                "title": row[1],
                "username": row[2],
                "language": row[3],
                "welcome": row[4],
                "welcome_enabled": row[5],
                "rules": row[6],
                "locks": json.loads(row[7]),
                "filters": json.loads(row[8]),
                "blocklist": json.loads(row[9]),
                "antiflood": row[10],
                "flood_limit": row[11],
                "captcha": row[12],
                "captcha_time": row[13],
                "warns_limit": row[14],
                "staff": json.loads(row[15]),
                "created_at": row[16],
            }
        return None
    
    def add_group(self, group_id: int, title: str, username: str = None):
        """Add new group to database"""
        self.cursor.execute("""
            INSERT OR IGNORE INTO groups (group_id, title, username)
            VALUES (?, ?, ?)
        """, (group_id, title, username))
        self.conn.commit()
    
    def update_group(self, group_id: int, **kwargs):
        """Update group data"""
        for key, value in kwargs.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            self.cursor.execute(f"UPDATE groups SET {key} = ? WHERE group_id = ?", (value, group_id))
        self.conn.commit()
    
    def add_note(self, group_id: int, name: str, content: str, file_id: str = None, created_by: int = None):
        """Add a note to group"""
        self.cursor.execute("""
            INSERT INTO notes (group_id, name, content, file_id, created_by)
            VALUES (?, ?, ?, ?, ?)
        """, (group_id, name, content, file_id, created_by))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_note(self, group_id: int, name: str) -> Optional[Dict]:
        """Get a note from group"""
        self.cursor.execute("SELECT * FROM notes WHERE group_id = ? AND name = ?", (group_id, name))
        row = self.cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "group_id": row[1],
                "name": row[2],
                "content": row[3],
                "file_id": row[4],
                "created_by": row[5],
                "created_at": row[6],
            }
        return None
    
    def get_notes(self, group_id: int) -> List[Dict]:
        """Get all notes in group"""
        self.cursor.execute("SELECT name, content FROM notes WHERE group_id = ?", (group_id,))
        return [{"name": row[0], "content": row[1]} for row in self.cursor.fetchall()]
    
    def delete_note(self, group_id: int, name: str):
        """Delete a note from group"""
        self.cursor.execute("DELETE FROM notes WHERE group_id = ? AND name = ?", (group_id, name))
        self.conn.commit()
    
    def add_filter(self, group_id: int, keyword: str, response: str, file_id: str = None, created_by: int = None):
        """Add a filter to group"""
        self.cursor.execute("""
            INSERT INTO filters (group_id, keyword, response, file_id, created_by)
            VALUES (?, ?, ?, ?, ?)
        """, (group_id, keyword, response, file_id, created_by))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_filter(self, group_id: int, keyword: str) -> Optional[Dict]:
        """Get a filter from group"""
        self.cursor.execute("SELECT * FROM filters WHERE group_id = ? AND keyword = ?", (group_id, keyword))
        row = self.cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "group_id": row[1],
                "keyword": row[2],
                "response": row[3],
                "file_id": row[4],
                "created_by": row[5],
                "created_at": row[6],
            }
        return None
    
    def get_filters(self, group_id: int) -> List[Dict]:
        """Get all filters in group"""
        self.cursor.execute("SELECT keyword, response FROM filters WHERE group_id = ?", (group_id,))
        return [{"keyword": row[0], "response": row[1]} for row in self.cursor.fetchall()]
    
    def delete_filter(self, group_id: int, keyword: str):
        """Delete a filter from group"""
        self.cursor.execute("DELETE FROM filters WHERE group_id = ? AND keyword = ?", (group_id, keyword))
        self.conn.commit()
    
    def add_warn(self, user_id: int, group_id: int, reason: str, warned_by: int):
        """Add a warning to user"""
        self.cursor.execute("""
            INSERT INTO warns (user_id, group_id, reason, warned_by)
            VALUES (?, ?, ?, ?)
        """, (user_id, group_id, reason, warned_by))
        self.conn.commit()
        
        # Update user warns count
        self.cursor.execute("SELECT warns FROM users WHERE user_id = ?", (user_id,))
        row = self.cursor.fetchone()
        if row:
            self.cursor.execute("UPDATE users SET warns = warns + 1 WHERE user_id = ?", (user_id,))
        else:
            self.cursor.execute("INSERT INTO users (user_id, warns) VALUES (?, 1)", (user_id,))
        self.conn.commit()
    
    def get_warns(self, user_id: int, group_id: int) -> int:
        """Get user warns count in group"""
        self.cursor.execute("SELECT COUNT(*) FROM warns WHERE user_id = ? AND group_id = ?", (user_id, group_id))
        return self.cursor.fetchone()[0]
    
    def clear_warns(self, user_id: int, group_id: int):
        """Clear all warns for user in group"""
        self.cursor.execute("DELETE FROM warns WHERE user_id = ? AND group_id = ?", (user_id, group_id))
        self.cursor.execute("UPDATE users SET warns = 0 WHERE user_id = ?", (user_id,))
        self.conn.commit()
    
    def get_warn_history(self, user_id: int, group_id: int) -> List[Dict]:
        """Get warn history for user in group"""
        self.cursor.execute("SELECT reason, warned_by, created_at FROM warns WHERE user_id = ? AND group_id = ?", (user_id, group_id))
        return [{"reason": row[0], "warned_by": row[1], "created_at": row[2]} for row in self.cursor.fetchall()]
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

# Global database instance
db = Database()