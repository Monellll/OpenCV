import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import datetime, date
from attendance_manager import AttendanceManager
from student_registration import StudentRegistration
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AttendanceDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Attendance System - Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        self.attendance_mgr = AttendanceManager()
        self.student_reg = StudentRegistration()
        
        self.setup_ui()
        self.refresh_data()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', padx=10, pady=(10, 0))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="📊 Smart Attendance Dashboard", 
                              font=('Arial', 18, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_overview_tab()
        self.create_attendance_tab()
        self.create_students_tab()
        self.create_reports_tab()
    
    def create_overview_tab(self):
        """Create overview tab with statistics"""
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="📈 Overview")
        
        # Statistics frame
        stats_frame = tk.Frame(overview_frame, bg='white', relief='raised', bd=2)
        stats_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(stats_frame, text="📊 Quick Statistics", font=('Arial', 14, 'bold'), 
                bg='white').pack(pady=10)
        
        # Stats display
        self.stats_frame = tk.Frame(stats_frame, bg='white')
        self.stats_frame.pack(fill='x', padx=20, pady=10)
        
        # Today's attendance frame
        today_frame = tk.Frame(overview_frame, bg='white', relief='raised', bd=2)
        today_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(today_frame, text="📅 Today's Attendance", font=('Arial', 14, 'bold'), 
                bg='white').pack(pady=10)
        
        # Today's attendance table
        columns = ('Student ID', 'Name', 'Time', 'Mode')
        self.today_tree = ttk.Treeview(today_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.today_tree.heading(col, text=col)
            self.today_tree.column(col, width=150)
        
        scrollbar_today = ttk.Scrollbar(today_frame, orient='vertical', command=self.today_tree.yview)
        self.today_tree.configure(yscrollcommand=scrollbar_today.set)
        
        self.today_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar_today.pack(side='right', fill='y', pady=10)
    
    def create_attendance_tab(self):
        """Create attendance records tab"""
        attendance_frame = ttk.Frame(self.notebook)
        self.notebook.add(attendance_frame, text="📋 Attendance Records")
        
        # Filter frame
        filter_frame = tk.Frame(attendance_frame, bg='white', relief='raised', bd=2)
        filter_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(filter_frame, text="🔍 Filter Records", font=('Arial', 12, 'bold'), 
                bg='white').pack(pady=5)
        
        filter_controls = tk.Frame(filter_frame, bg='white')
        filter_controls.pack(pady=10)
        
        tk.Label(filter_controls, text="Date:", bg='white').grid(row=0, column=0, padx=5)
        self.date_var = tk.StringVar()
        date_entry = tk.Entry(filter_controls, textvariable=self.date_var, width=12)
        date_entry.grid(row=0, column=1, padx=5)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        tk.Button(filter_controls, text="Filter", command=self.filter_attendance,
                 bg='#3498db', fg='white').grid(row=0, column=2, padx=10)
        tk.Button(filter_controls, text="Show All", command=self.show_all_attendance,
                 bg='#95a5a6', fg='white').grid(row=0, column=3, padx=5)
        
        # Attendance table
        table_frame = tk.Frame(attendance_frame, bg='white', relief='raised', bd=2)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Student ID', 'Name', 'Date', 'Time', 'Mode')
        self.attendance_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        for col in columns:
            self.attendance_tree.heading(col, text=col)
            if col == 'ID':
                self.attendance_tree.column(col, width=50)
            else:
                self.attendance_tree.column(col, width=120)
        
        scrollbar_att = ttk.Scrollbar(table_frame, orient='vertical', command=self.attendance_tree.yview)
        self.attendance_tree.configure(yscrollcommand=scrollbar_att.set)
        
        self.attendance_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar_att.pack(side='right', fill='y', pady=10)
    
    def create_students_tab(self):
        """Create students management tab"""
        students_frame = ttk.Frame(self.notebook)
        self.notebook.add(students_frame, text="👥 Students")
        
        # Students table
        table_frame = tk.Frame(students_frame, bg='white', relief='raised', bd=2)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(table_frame, text="👥 Registered Students", font=('Arial', 14, 'bold'), 
                bg='white').pack(pady=10)
        
        columns = ('Student ID', 'Name', 'Email', 'Registration Date', 'Has Face Data', 'Total Attendance')
        self.students_tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        for col in columns:
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=150)
        
        scrollbar_std = ttk.Scrollbar(table_frame, orient='vertical', command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=scrollbar_std.set)
        
        self.students_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar_std.pack(side='right', fill='y', pady=10)
    
    def create_reports_tab(self):
        """Create reports and export tab"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="📊 Reports")
        
        # Export frame
        export_frame = tk.Frame(reports_frame, bg='white', relief='raised', bd=2)
        export_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(export_frame, text="📤 Export Data", font=('Arial', 14, 'bold'), 
                bg='white').pack(pady=10)
        
        export_buttons = tk.Frame(export_frame, bg='white')
        export_buttons.pack(pady=10)
        
        tk.Button(export_buttons, text="Export to Excel", command=self.export_excel,
                 bg='#27ae60', fg='white', width=15).pack(side='left', padx=10)
        tk.Button(export_buttons, text="Export to CSV", command=self.export_csv,
                 bg='#e74c3c', fg='white', width=15).pack(side='left', padx=10)
        
        # Summary frame
        summary_frame = tk.Frame(reports_frame, bg='white', relief='raised', bd=2)
        summary_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(summary_frame, text="📈 Attendance Summary", font=('Arial', 14, 'bold'), 
                bg='white').pack(pady=10)
        
        # Summary table
        summary_columns = ('Student ID', 'Name', 'Total Days', 'Last Attendance')
        self.summary_tree = ttk.Treeview(summary_frame, columns=summary_columns, show='headings')
        
        for col in summary_columns:
            self.summary_tree.heading(col, text=col)
            self.summary_tree.column(col, width=150)
        
        scrollbar_sum = ttk.Scrollbar(summary_frame, orient='vertical', command=self.summary_tree.yview)
        self.summary_tree.configure(yscrollcommand=scrollbar_sum.set)
        
        self.summary_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar_sum.pack(side='right', fill='y', pady=10)
    
    def refresh_data(self):
        """Refresh all data in the dashboard"""
        self.update_statistics()
        self.update_today_attendance()
        self.update_attendance_records()
        self.update_students_list()
        self.update_summary()
    
    def update_statistics(self):
        """Update statistics display"""
        stats = self.attendance_mgr.get_attendance_stats()
        
        # Clear previous stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Create stat boxes
        stat_items = [
            ("Total Records", stats['total_records'], "#3498db"),
            ("Registered Students", stats['unique_students'], "#27ae60"),
            ("Today's Attendance", stats['today_attendance'], "#e74c3c")
        ]
        
        for i, (label, value, color) in enumerate(stat_items):
            stat_box = tk.Frame(self.stats_frame, bg=color, relief='raised', bd=2)
            stat_box.pack(side='left', fill='x', expand=True, padx=10, pady=5)
            
            tk.Label(stat_box, text=str(value), font=('Arial', 24, 'bold'), 
                    fg='white', bg=color).pack(pady=5)
            tk.Label(stat_box, text=label, font=('Arial', 10), 
                    fg='white', bg=color).pack(pady=(0, 10))
    
    def update_today_attendance(self):
        """Update today's attendance table"""
        # Clear existing data
        for item in self.today_tree.get_children():
            self.today_tree.delete(item)
        
        # Get today's records
        today = datetime.now().strftime("%Y-%m-%d")
        records = self.attendance_mgr.get_attendance_records(today)
        
        for _, record in records.iterrows():
            self.today_tree.insert('', 'end', values=(
                record['student_id'], record['name'], record['time'], record['mode']
            ))
    
    def update_attendance_records(self):
        """Update attendance records table"""
        # Clear existing data
        for item in self.attendance_tree.get_children():
            self.attendance_tree.delete(item)
        
        # Get all records
        records = self.attendance_mgr.get_attendance_records()
        
        for _, record in records.iterrows():
            self.attendance_tree.insert('', 'end', values=(
                record['id'], record['student_id'], record['name'], 
                record['date'], record['time'], record['mode']
            ))
    
    def update_students_list(self):
        """Update students list"""
        # Clear existing data
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        students = self.student_reg.get_all_students()
        summary = self.attendance_mgr.get_student_attendance_summary()
        
        for student_id, student_info in students.items():
            # Get attendance count
            student_summary = summary[summary['student_id'] == student_id]
            total_days = student_summary['total_days'].iloc[0] if not student_summary.empty else 0
            
            self.students_tree.insert('', 'end', values=(
                student_id,
                student_info['name'],
                student_info.get('email', ''),
                student_info['registration_date'][:10],
                'Yes' if student_info.get('has_face_data', False) else 'No',
                total_days
            ))
    
    def update_summary(self):
        """Update attendance summary"""
        # Clear existing data
        for item in self.summary_tree.get_children():
            self.summary_tree.delete(item)
        
        summary = self.attendance_mgr.get_student_attendance_summary()
        
        for _, record in summary.iterrows():
            self.summary_tree.insert('', 'end', values=(
                record['student_id'], record['name'], 
                record['total_days'], record['last_attendance']
            ))
    
    def filter_attendance(self):
        """Filter attendance by date"""
        date_filter = self.date_var.get()
        
        # Clear existing data
        for item in self.attendance_tree.get_children():
            self.attendance_tree.delete(item)
        
        try:
            records = self.attendance_mgr.get_attendance_records(date_filter)
            
            for _, record in records.iterrows():
                self.attendance_tree.insert('', 'end', values=(
                    record['id'], record['student_id'], record['name'], 
                    record['date'], record['time'], record['mode']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Invalid date format: {e}")
    
    def show_all_attendance(self):
        """Show all attendance records"""
        self.update_attendance_records()
    
    def export_excel(self):
        """Export attendance data to Excel"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            
            if filename:
                exported_file = self.attendance_mgr.export_to_excel(filename)
                messagebox.showinfo("Success", f"Data exported to {exported_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
    
    def export_csv(self):
        """Export attendance data to CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                records = self.attendance_mgr.get_attendance_records()
                records.to_csv(filename, index=False)
                messagebox.showinfo("Success", f"Data exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")

def main():
    root = tk.Tk()
    app = AttendanceDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
