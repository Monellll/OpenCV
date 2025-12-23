import tkinter as tk
from tkinter import ttk, messagebox
import threading
from face_recognition_module import FaceRecognitionModule
from gesture_detection import GestureDetection
from student_registration import StudentRegistration
from dashboard import AttendanceDashboard
import sys
import os

class SmartAttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Attendance System 👩‍💻")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Initialize modules
        self.face_module = FaceRecognitionModule()
        self.gesture_module = GestureDetection()
        self.student_reg = StudentRegistration()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Main title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=100)
        title_frame.pack(fill='x', pady=20)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="Smart Attendance System", 
                              font=('Arial', 24, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(title_frame, text="Face Recognition & Gesture Detection", 
                                 font=('Arial', 12), fg='#bdc3c7', bg='#2c3e50')
        subtitle_label.pack()
        
        # Main menu frame
        menu_frame = tk.Frame(self.root, bg='#34495e', relief='raised', bd=2)
        menu_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Menu title
        menu_title = tk.Label(menu_frame, text="🎯 Select Mode", 
                             font=('Arial', 18, 'bold'), fg='white', bg='#34495e')
        menu_title.pack(pady=30)
        
        # Button frame
        button_frame = tk.Frame(menu_frame, bg='#34495e')
        button_frame.pack(expand=True, fill='both', padx=50, pady=20)
        
        # Mode buttons
        self.create_mode_button(button_frame, "👤 Face Recognition Mode", 
                               "Automatic attendance via face detection", 
                               self.start_face_recognition, '#3498db', 0)
        
        self.create_mode_button(button_frame, "✋ Gesture Detection Mode", 
                               "Mark attendance by raising hand", 
                               self.start_gesture_detection, '#e74c3c', 1)
        
        self.create_mode_button(button_frame, "👥 Student Registration", 
                               "Register new students and manage data", 
                               self.open_registration, '#27ae60', 2)
        
        self.create_mode_button(button_frame, "📊 View Dashboard", 
                               "View attendance records and statistics", 
                               self.open_dashboard, '#f39c12', 3)
        
        self.create_mode_button(button_frame, "🧪 Test Gesture Detection", 
                               "Test hand gesture recognition", 
                               self.test_gesture, '#9b59b6', 4)
        
        # Status frame
        status_frame = tk.Frame(self.root, bg='#2c3e50', height=50)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Ready", 
                                    font=('Arial', 10), fg='#95a5a6', bg='#2c3e50')
        self.status_label.pack(expand=True)
    
    def create_mode_button(self, parent, title, description, command, color, row):
        """Create a mode selection button"""
        button_container = tk.Frame(parent, bg='#34495e')
        button_container.pack(fill='x', pady=10)
        
        button = tk.Button(button_container, text=title, font=('Arial', 14, 'bold'),
                          bg=color, fg='white', relief='flat', bd=0, pady=15,
                          command=command, cursor='hand2')
        button.pack(fill='x')
        
        desc_label = tk.Label(button_container, text=description, 
                             font=('Arial', 10), fg='#bdc3c7', bg='#34495e')
        desc_label.pack(pady=(5, 0))
        
        # Hover effects
        def on_enter(e):
            button.configure(bg=self.lighten_color(color))
        
        def on_leave(e):
            button.configure(bg=color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def lighten_color(self, color):
        """Lighten a hex color for hover effect"""
        color_map = {
            '#3498db': '#5dade2',
            '#e74c3c': '#ec7063',
            '#27ae60': '#58d68d',
            '#f39c12': '#f8c471',
            '#9b59b6': '#bb8fce'
        }
        return color_map.get(color, color)
    
    def update_status(self, message):
        """Update status message"""
        self.status_label.config(text=message)
        self.root.update()
    
    def start_face_recognition(self):
        """Start face recognition mode in a separate thread"""
        self.update_status("Starting Face Recognition Mode...")
        
        def run_face_recognition():
            try:
                success, message = self.face_module.start_face_recognition_mode()
                self.root.after(0, lambda: self.update_status(f"Face Recognition: {message}"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Face recognition failed: {e}"))
                self.root.after(0, lambda: self.update_status("Ready"))
        
        thread = threading.Thread(target=run_face_recognition, daemon=True)
        thread.start()
    
    def start_gesture_detection(self):
        """Start gesture detection mode in a separate thread"""
        self.update_status("Starting Gesture Detection Mode...")
        
        def run_gesture_detection():
            try:
                success, message = self.gesture_module.start_gesture_detection_mode()
                self.root.after(0, lambda: self.update_status(f"Gesture Detection: {message}"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Gesture detection failed: {e}"))
                self.root.after(0, lambda: self.update_status("Ready"))
        
        thread = threading.Thread(target=run_gesture_detection, daemon=True)
        thread.start()
    
    def test_gesture(self):
        """Test gesture detection in a separate thread"""
        self.update_status("Starting Gesture Test...")
        
        def run_gesture_test():
            try:
                success, message = self.gesture_module.test_gesture_detection()
                self.root.after(0, lambda: self.update_status(f"Gesture Test: {message}"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Gesture test failed: {e}"))
                self.root.after(0, lambda: self.update_status("Ready"))
        
        thread = threading.Thread(target=run_gesture_test, daemon=True)
        thread.start()
    
    def open_registration(self):
        """Open student registration window"""
        self.update_status("Opening Student Registration...")
        registration_window = StudentRegistrationGUI(self.root, self.student_reg)
    
    def open_dashboard(self):
        """Open attendance dashboard"""
        self.update_status("Opening Dashboard...")
        dashboard_window = tk.Toplevel(self.root)
        dashboard_app = AttendanceDashboard(dashboard_window)

class StudentRegistrationGUI:
    def __init__(self, parent, student_reg):
        self.parent = parent
        self.student_reg = student_reg
        
        self.window = tk.Toplevel(parent)
        self.window.title("Student Registration")
        self.window.geometry("600x500")
        self.window.configure(bg='#ecf0f1')
        
        self.setup_registration_ui()
    
    def setup_registration_ui(self):
        """Setup registration interface"""
        # Title
        title_frame = tk.Frame(self.window, bg='#3498db', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="👥 Student Registration", 
                              font=('Arial', 16, 'bold'), fg='white', bg='#3498db')
        title_label.pack(expand=True)
        
        # Registration form
        form_frame = tk.Frame(self.window, bg='white', relief='raised', bd=2)
        form_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(form_frame, text="Register New Student", font=('Arial', 14, 'bold'), 
                bg='white').pack(pady=15)
        
        # Form fields
        fields_frame = tk.Frame(form_frame, bg='white')
        fields_frame.pack(padx=30, pady=10)
        
        tk.Label(fields_frame, text="Student ID:", bg='white').grid(row=0, column=0, sticky='w', pady=5)
        self.id_entry = tk.Entry(fields_frame, width=30)
        self.id_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(fields_frame, text="Full Name:", bg='white').grid(row=1, column=0, sticky='w', pady=5)
        self.name_entry = tk.Entry(fields_frame, width=30)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(fields_frame, text="Email:", bg='white').grid(row=2, column=0, sticky='w', pady=5)
        self.email_entry = tk.Entry(fields_frame, width=30)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Register Only", command=self.register_only,
                 bg='#95a5a6', fg='white', width=15).pack(side='left', padx=10)
        tk.Button(button_frame, text="Register + Capture Face", command=self.register_with_face,
                 bg='#27ae60', fg='white', width=20).pack(side='left', padx=10)
        
        # Students list
        list_frame = tk.Frame(self.window, bg='white', relief='raised', bd=2)
        list_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        tk.Label(list_frame, text="📋 Registered Students", font=('Arial', 14, 'bold'), 
                bg='white').pack(pady=10)
        
        # Students table
        columns = ('ID', 'Name', 'Email', 'Face Data')
        self.students_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.students_tree.yview)
        self.students_tree.configure(yscrollcommand=scrollbar.set)
        
        self.students_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        # Action buttons
        action_frame = tk.Frame(list_frame, bg='white')
        action_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Button(action_frame, text="Capture Face for Selected", command=self.capture_face_selected,
                 bg='#3498db', fg='white').pack(side='left', padx=5)
        tk.Button(action_frame, text="Delete Selected", command=self.delete_selected,
                 bg='#e74c3c', fg='white').pack(side='left', padx=5)
        tk.Button(action_frame, text="Refresh", command=self.refresh_students,
                 bg='#f39c12', fg='white').pack(side='left', padx=5)
        
        self.refresh_students()
    
    def register_only(self):
        """Register student without face capture"""
        student_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not student_id or not name:
            messagebox.showerror("Error", "Student ID and Name are required")
            return
        
        success, message = self.student_reg.register_student_manual(student_id, name, email)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.refresh_students()
        else:
            messagebox.showerror("Error", message)
    
    def register_with_face(self):
        """Register student and capture face"""
        student_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not student_id or not name:
            messagebox.showerror("Error", "Student ID and Name are required")
            return
        
        success, message = self.student_reg.register_student_with_face(student_id, name, email)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.refresh_students()
        else:
            messagebox.showerror("Error", message)
    
    def capture_face_selected(self):
        """Capture face for selected student"""
        selection = self.students_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a student")
            return
        
        item = self.students_tree.item(selection[0])
        student_id = item['values'][0]
        
        success, message = self.student_reg.capture_face_for_student(student_id)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_students()
        else:
            messagebox.showerror("Error", message)
    
    def delete_selected(self):
        """Delete selected student"""
        selection = self.students_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a student")
            return
        
        item = self.students_tree.item(selection[0])
        student_id = item['values'][0]
        student_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Delete student {student_name}?"):
            success, message = self.student_reg.delete_student(student_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.refresh_students()
            else:
                messagebox.showerror("Error", message)
    
    def refresh_students(self):
        """Refresh students list"""
        # Clear existing data
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        # Load students
        students = self.student_reg.get_all_students()
        
        for student_id, student_info in students.items():
            self.students_tree.insert('', 'end', values=(
                student_id,
                student_info['name'],
                student_info.get('email', ''),
                'Yes' if student_info.get('has_face_data', False) else 'No'
            ))
    
    def clear_form(self):
        """Clear form fields"""
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

def main():
    # Check if required directories exist
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("data/faces"):
        os.makedirs("data/faces")
    
    root = tk.Tk()
    app = SmartAttendanceSystem(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApplication closed by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
