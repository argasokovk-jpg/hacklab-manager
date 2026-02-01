import sqlite3
import os

class ActionLogger:
    def __init__(self, user_id=1):
        self.user_id = user_id
        self.db_path = os.path.expanduser('~/.hacklab/data.db')
        
    def log_action(self, lab_id, action_type, tool_used, target=""):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO user_actions (user_id, lab_id, action_type, tool_used, target)
        VALUES (?, ?, ?, ?, ?)
        ''', (self.user_id, lab_id, action_type, tool_used, target))
        
        conn.commit()
        conn.close()
