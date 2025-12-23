import csv
import sqlite3
import pandas as pd
from datetime import datetime
import os

class AttendanceManager:
    def __init__(self):
        self.csv_file = "data/attendance.csv"
        self.db_file = "data/attendance.db"
        self.ensure_data_directory()
        self.init_csv()
        self.init_database()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists("data/faces"):
            os.makedirs("data/faces")
    
    def init_csv(self):
        """Initialize CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Student_ID', 'Name', 'Date', 'Time', 'Mode'])
    
    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                mode TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def mark_attendance(self, student_id, name, mode="Face Recognition"):
        """Mark attendance for a student"""
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        # Check if already marked today
        if self.is_already_marked_today(student_id, date_str):
            return False, "Attendance already marked today"
        
        # Save to CSV
        with open(self.csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([student_id, name, date_str, time_str, mode])
        
        # Save to database
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO attendance (student_id, name, date, time, mode)
            VALUES (?, ?, ?, ?, ?)
        ''', (student_id, name, date_str, time_str, mode))
        conn.commit()
        conn.close()
        
        return True, f"Attendance marked for {name} at {time_str}"
    
    def is_already_marked_today(self, student_id, date_str):
        """Check if student attendance is already marked for today"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM attendance 
            WHERE student_id = ? AND date = ?
        ''', (student_id, date_str))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    
    def get_attendance_records(self, date_filter=None):
        """Get attendance records with optional date filter"""
        conn = sqlite3.connect(self.db_file)
        
        if date_filter:
            query = "SELECT * FROM attendance WHERE date = ? ORDER BY timestamp DESC"
            df = pd.read_sql_query(query, conn, params=(date_filter,))
        else:
            query = "SELECT * FROM attendance ORDER BY timestamp DESC"
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        return df
    
    def get_student_attendance_summary(self):
        """Get attendance summary by student"""
        conn = sqlite3.connect(self.db_file)
        query = '''
            SELECT student_id, name, COUNT(*) as total_days,
                   MAX(date) as last_attendance
            FROM attendance 
            GROUP BY student_id, name
            ORDER BY total_days DESC
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def export_to_excel(self, filename=None):
        """Export attendance data to Excel"""
        if not filename:
            filename = f"attendance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        df = self.get_attendance_records()
        df.to_excel(filename, index=False)
        return filename
    
    def get_attendance_stats(self):
        """Get basic attendance statistics"""
        conn = sqlite3.connect(self.db_file)
        
        # Total records
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM attendance")
        total_records = cursor.fetchone()[0]
        
        # Unique students
        cursor.execute("SELECT COUNT(DISTINCT student_id) FROM attendance")
        unique_students = cursor.fetchone()[0]
        
        # Today's attendance
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("SELECT COUNT(*) FROM attendance WHERE date = ?", (today,))
        today_attendance = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_records': total_records,
            'unique_students': unique_students,
            'today_attendance': today_attendance
        }
