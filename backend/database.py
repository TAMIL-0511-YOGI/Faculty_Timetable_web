import sqlite3
import os
from models import Teacher, Subject

DB_PATH = "timetable.db"

def init_db():
    """Initialize database with proper schema"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Teachers table
    c.execute('''CREATE TABLE IF NOT EXISTS teachers (
                    teacher_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL
                )''')
    
    # Subjects table
    c.execute('''CREATE TABLE IF NOT EXISTS subjects (
                    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    section TEXT NOT NULL,
                    hours_per_week INTEGER NOT NULL,
                    is_lab BOOLEAN DEFAULT 0,
                    lab_days TEXT DEFAULT '',
                    teacher_id TEXT NOT NULL,
                    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
                )''')
    
    # Timetable entries table
    c.execute('''CREATE TABLE IF NOT EXISTS timetable_entries (
                    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    teacher_id TEXT NOT NULL,
                    subject_name TEXT NOT NULL,
                    class_name TEXT NOT NULL,
                    day INTEGER NOT NULL,
                    period INTEGER NOT NULL,
                    entry_type TEXT DEFAULT 'Class',
                    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
                )''')
    
    conn.commit()
    conn.close()

def connect():
    """Connect to database"""
    return sqlite3.connect(DB_PATH)

def add_teacher(teacher_id, name):
    """Add a new teacher"""
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO teachers (teacher_id, name) VALUES (?, ?)", 
              (teacher_id, name))
    conn.commit()
    conn.close()

def add_subject(subject_name, year, section, hours_per_week, teacher_id, is_lab=0, lab_days=''):
    """Add a subject to a teacher"""
    conn = connect()
    c = conn.cursor()
    c.execute('''INSERT INTO subjects 
                 (name, year, section, hours_per_week, is_lab, lab_days, teacher_id) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', 
              (subject_name, year, section, hours_per_week, is_lab, lab_days, teacher_id))
    conn.commit()
    conn.close()

def get_all_teachers():
    """Get all teachers with their subjects"""
    conn = connect()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM teachers")
    teachers_data = c.fetchall()
    
    teachers = []
    for t in teachers_data:
        teacher = Teacher(t['teacher_id'], t['name'])
        
        # Get subjects for this teacher
        c.execute("SELECT * FROM subjects WHERE teacher_id = ?", (t['teacher_id'],))
        subjects_data = c.fetchall()
        
        for s in subjects_data:
            # Convert lab_days from string to list of integers
            if s['lab_days'] and s['lab_days'].strip():
                lab_days = [int(x.strip()) for x in s['lab_days'].split(',')]
            else:
                lab_days = []
            
            subject = Subject(
                name=s['name'],
                year=s['year'],
                section=s['section'],
                hours_per_week=s['hours_per_week'],
                is_lab=bool(s['is_lab']),
                lab_days=lab_days,
                subject_id=s['subject_id']
            )
            teacher.add_subject(subject)
        
        teachers.append(teacher)
    
    conn.close()
    return teachers

def delete_subject(subject_id):
    """Delete a specific subject by ID"""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM subjects WHERE subject_id = ?", (subject_id,))
    conn.commit()
    conn.close()

def update_subject(subject_id, subject_name, year, section, hours_per_week, is_lab=0):
    """Update a specific subject"""
    conn = connect()
    c = conn.cursor()
    c.execute('''UPDATE subjects 
                 SET name = ?, year = ?, section = ?, hours_per_week = ?, is_lab = ?
                 WHERE subject_id = ?''', 
              (subject_name, year, section, hours_per_week, is_lab, subject_id))
    conn.commit()
    conn.close()

def clear_all():
    """Clear all data from database"""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM timetable_entries")
    c.execute("DELETE FROM subjects")
    c.execute("DELETE FROM teachers")
    conn.commit()
    conn.close()

def save_timetable(timetable_dict):
    """Save generated timetable to database"""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM timetable_entries")  # Clear old entries
    
    for teacher_id, schedule in timetable_dict.items():
        for day_idx, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri"]):
            for period_idx, entry in enumerate(schedule[day]):
                # Only save Class and Lab entries, skip Free and Break
                if entry["type"] in ["Class", "Lab"] and entry.get("subject"):
                    c.execute('''INSERT INTO timetable_entries 
                                 (teacher_id, subject_name, class_name, day, period, entry_type)
                                 VALUES (?, ?, ?, ?, ?, ?)''',
                              (teacher_id, entry['subject'], entry.get('class', 'N/A'), day_idx, period_idx, entry['type']))
    
    conn.commit()
    conn.close()

# Initialize database on import
if not os.path.exists(DB_PATH):
    init_db()
