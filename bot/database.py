"""
Database module using SQLite
Handles warns, locks, user stats, and game states
"""
import aiosqlite
import json
from typing import Optional, List, Dict, Any


class Database:
    def __init__(self, db_path: str = "bot_data.db"):
        self.db_path = db_path
        self.conn: Optional[aiosqlite.Connection] = None

    async def init(self):
        """Initialize database and create tables"""
        self.conn = await aiosqlite.connect(self.db_path)
        await self._create_tables()

    async def _create_tables(self):
        """Create required tables"""
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS warns (
                user_id INTEGER,
                chat_id INTEGER,
                reason TEXT,
                warned_by INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, chat_id, timestamp)
            )
        """)
        
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS locks (
                chat_id INTEGER PRIMARY KEY,
                locked_types TEXT DEFAULT '[]'
            )
        """)
        
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS user_stats (
                user_id INTEGER,
                chat_id INTEGER,
                messages INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, chat_id)
            )
        """)
        
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS game_states (
                chat_id INTEGER,
                game_type TEXT,
                state TEXT,
                PRIMARY KEY (chat_id, game_type)
            )
        """)
        
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS music_queue (
                chat_id INTEGER,
                queue TEXT DEFAULT '[]',
                current_index INTEGER DEFAULT 0,
                PRIMARY KEY (chat_id)
            )
        """)
        
        await self.conn.commit()

    # Warn methods
    async def add_warn(self, user_id: int, chat_id: int, reason: str, warned_by: int) -> int:
        """Add a warn and return total warn count"""
        await self.conn.execute(
            "INSERT INTO warns (user_id, chat_id, reason, warned_by) VALUES (?, ?, ?, ?)",
            (user_id, chat_id, reason, warned_by)
        )
        await self.conn.commit()
        return await self.get_warn_count(user_id, chat_id)

    async def get_warn_count(self, user_id: int, chat_id: int) -> int:
        """Get warn count for a user in a chat"""
        cursor = await self.conn.execute(
            "SELECT COUNT(*) FROM warns WHERE user_id = ? AND chat_id = ?",
            (user_id, chat_id)
        )
        row = await cursor.fetchone()
        return row[0] if row else 0

    async def get_warns(self, user_id: int, chat_id: int) -> List[Dict]:
        """Get all warns for a user in a chat"""
        cursor = await self.conn.execute(
            "SELECT reason, warned_by, timestamp FROM warns WHERE user_id = ? AND chat_id = ?",
            (user_id, chat_id)
        )
        rows = await cursor.fetchall()
        return [{"reason": r[0], "warned_by": r[1], "timestamp": r[2]} for r in rows]

    async def remove_warn(self, user_id: int, chat_id: int) -> bool:
        """Remove the latest warn for a user"""
        cursor = await self.conn.execute(
            "DELETE FROM warns WHERE user_id = ? AND chat_id = ? AND timestamp = (SELECT MAX(timestamp) FROM warns WHERE user_id = ? AND chat_id = ?)",
            (user_id, chat_id, user_id, chat_id)
        )
        await self.conn.commit()
        return cursor.rowcount > 0

    async def clear_warns(self, user_id: int, chat_id: int):
        """Clear all warns for a user in a chat"""
        await self.conn.execute(
            "DELETE FROM warns WHERE user_id = ? AND chat_id = ?",
            (user_id, chat_id)
        )
        await self.conn.commit()

    # Lock methods
    async def get_locks(self, chat_id: int) -> List[str]:
        """Get locked types for a chat"""
        cursor = await self.conn.execute(
            "SELECT locked_types FROM locks WHERE chat_id = ?",
            (chat_id,)
        )
        row = await cursor.fetchone()
        return json.loads(row[0]) if row else []

    async def add_lock(self, chat_id: int, lock_type: str):
        """Add a lock type"""
        locks = await self.get_locks(chat_id)
        if lock_type not in locks:
            locks.append(lock_type)
        await self.conn.execute(
            "INSERT OR REPLACE INTO locks (chat_id, locked_types) VALUES (?, ?)",
            (chat_id, json.dumps(locks))
        )
        await self.conn.commit()

    async def remove_lock(self, chat_id: int, lock_type: str):
        """Remove a lock type"""
        locks = await self.get_locks(chat_id)
        if lock_type in locks:
            locks.remove(lock_type)
        await self.conn.execute(
            "INSERT OR REPLACE INTO locks (chat_id, locked_types) VALUES (?, ?)",
            (chat_id, json.dumps(locks))
        )
        await self.conn.commit()

    # Game state methods
    async def get_game_state(self, chat_id: int, game_type: str) -> Optional[Dict]:
        """Get game state for a chat"""
        cursor = await self.conn.execute(
            "SELECT state FROM game_states WHERE chat_id = ? AND game_type = ?",
            (chat_id, game_type)
        )
        row = await cursor.fetchone()
        return json.loads(row[0]) if row else None

    async def set_game_state(self, chat_id: int, game_type: str, state: Dict):
        """Set game state for a chat"""
        await self.conn.execute(
            "INSERT OR REPLACE INTO game_states (chat_id, game_type, state) VALUES (?, ?, ?)",
            (chat_id, game_type, json.dumps(state))
        )
        await self.conn.commit()

    async def clear_game_state(self, chat_id: int, game_type: str):
        """Clear game state"""
        await self.conn.execute(
            "DELETE FROM game_states WHERE chat_id = ? AND game_type = ?",
            (chat_id, game_type)
        )
        await self.conn.commit()

    # Music queue methods
    async def get_queue(self, chat_id: int) -> List[Dict]:
        """Get music queue for a chat"""
        cursor = await self.conn.execute(
            "SELECT queue FROM music_queue WHERE chat_id = ?",
            (chat_id,)
        )
        row = await cursor.fetchone()
        return json.loads(row[0]) if row else []

    async def add_to_queue(self, chat_id: int, track: Dict):
        """Add track to queue"""
        queue = await self.get_queue(chat_id)
        queue.append(track)
        await self.conn.execute(
            "INSERT OR REPLACE INTO music_queue (chat_id, queue) VALUES (?, ?)",
            (chat_id, json.dumps(queue))
        )
        await self.conn.commit()

    async def clear_queue(self, chat_id: int):
        """Clear music queue"""
        await self.conn.execute(
            "DELETE FROM music_queue WHERE chat_id = ?",
            (chat_id,)
        )
        await self.conn.commit()


# Global database instance
db = Database()
