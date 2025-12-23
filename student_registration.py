import cv2
import face_recognition
import pickle
import os
import json
from datetime import datetime

class StudentRegistration:
    def __init__(self):
        self.faces_dir = "data/faces"
        self.students_file = "data/students.json"
        self.encodings_file = "data/face_encodings.pkl"
        self.ensure_directories()
        self.load_students()
        self.load_encodings()
    
    def ensure_directories(self):
        """Create necessary directories"""
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.faces_dir):
            os.makedirs(self.faces_dir)
    
    def load_students(self):
        """Load student information from JSON file"""
        if os.path.exists(self.students_file):
            with open(self.students_file, 'r') as f:
                self.students = json.load(f)
        else:
            self.students = {}
    
    def save_students(self):
        """Save student information to JSON file"""
        with open(self.students_file, 'w') as f:
            json.dump(self.students, f, indent=2)
    
    def load_encodings(self):
        """Load face encodings from pickle file"""
        if os.path.exists(self.encodings_file):
            with open(self.encodings_file, 'rb') as f:
                self.known_encodings = pickle.load(f)
        else:
            self.known_encodings = {}
    
    def save_encodings(self):
        """Save face encodings to pickle file"""
        with open(self.encodings_file, 'wb') as f:
            pickle.dump(self.known_encodings, f)
    
    def register_student_manual(self, student_id, name, email=""):
        """Register student manually without face capture"""
        self.students[student_id] = {
            'name': name,
            'email': email,
            'registration_date': datetime.now().isoformat(),
            'has_face_data': False
        }
        self.save_students()
        return True, f"Student {name} registered successfully"
    
    def capture_face_for_student(self, student_id):
        """Capture face data for an existing student"""
        if student_id not in self.students:
            return False, "Student not found. Please register student first."
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return False, "Could not access camera"
        
        print(f"Capturing face for {self.students[student_id]['name']}")
        print("Press SPACE to capture, ESC to cancel")
        
        face_captured = False
        encoding = None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Find faces in the frame
            face_locations = face_recognition.face_locations(rgb_frame)
            
            # Draw rectangles around faces
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, "Press SPACE to capture", (left, top-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            cv2.putText(frame, f"Registering: {self.students[student_id]['name']}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press SPACE to capture, ESC to cancel", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.imshow('Face Registration', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                break
            elif key == 32:  # SPACE key
                if face_locations:
                    # Get face encoding
                    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                    if face_encodings:
                        encoding = face_encodings[0]
                        face_captured = True
                        
                        # Save face image
                        face_image_path = os.path.join(self.faces_dir, f"{student_id}.jpg")
                        cv2.imwrite(face_image_path, frame)
                        
                        print(f"Face captured for {self.students[student_id]['name']}")
                        break
                else:
                    print("No face detected. Please position your face in the frame.")
        
        cap.release()
        cv2.destroyAllWindows()
        
        if face_captured:
            # Store encoding
            self.known_encodings[student_id] = encoding
            self.save_encodings()
            
            # Update student record
            self.students[student_id]['has_face_data'] = True
            self.save_students()
            
            return True, f"Face data captured for {self.students[student_id]['name']}"
        else:
            return False, "Face capture cancelled or failed"
    
    def register_student_with_face(self, student_id, name, email=""):
        """Register student and capture face in one step"""
        # First register student
        success, message = self.register_student_manual(student_id, name, email)
        if not success:
            return False, message
        
        # Then capture face
        return self.capture_face_for_student(student_id)
    
    def get_all_students(self):
        """Get list of all registered students"""
        return self.students
    
    def get_student_by_id(self, student_id):
        """Get student information by ID"""
        return self.students.get(student_id, None)
    
    def delete_student(self, student_id):
        """Delete a student and their face data"""
        if student_id not in self.students:
            return False, "Student not found"
        
        # Remove from students dict
        student_name = self.students[student_id]['name']
        del self.students[student_id]
        self.save_students()
        
        # Remove face encoding
        if student_id in self.known_encodings:
            del self.known_encodings[student_id]
            self.save_encodings()
        
        # Remove face image
        face_image_path = os.path.join(self.faces_dir, f"{student_id}.jpg")
        if os.path.exists(face_image_path):
            os.remove(face_image_path)
        
        return True, f"Student {student_name} deleted successfully"
    
    def get_known_encodings(self):
        """Get all known face encodings for recognition"""
        return self.known_encodings
