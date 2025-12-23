import cv2
import face_recognition
import numpy as np
from student_registration import StudentRegistration
from attendance_manager import AttendanceManager

class FaceRecognitionModule:
    def __init__(self):
        self.student_reg = StudentRegistration()
        self.attendance_mgr = AttendanceManager()
        self.known_encodings = self.student_reg.get_known_encodings()
        self.students = self.student_reg.get_all_students()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
    def refresh_data(self):
        """Refresh student and encoding data"""
        self.known_encodings = self.student_reg.get_known_encodings()
        self.students = self.student_reg.get_all_students()
    
    def recognize_faces(self, frame):
        """Recognize faces in the given frame"""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find face locations and encodings
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        recognized_faces = []
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare with known faces
            matches = []
            face_distances = []
            
            if self.known_encodings:
                known_ids = list(self.known_encodings.keys())
                known_encodings_list = list(self.known_encodings.values())
                
                matches = face_recognition.compare_faces(known_encodings_list, face_encoding, tolerance=0.6)
                face_distances = face_recognition.face_distance(known_encodings_list, face_encoding)
            
            name = "Unknown"
            student_id = None
            confidence = 0
            
            if matches and True in matches:
                # Find the best match
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    student_id = known_ids[best_match_index]
                    name = self.students[student_id]['name']
                    confidence = 1 - face_distances[best_match_index]
            
            recognized_faces.append({
                'student_id': student_id,
                'name': name,
                'location': face_location,
                'confidence': confidence
            })
        
        return recognized_faces
    
    def draw_face_boxes(self, frame, recognized_faces):
        """Draw bounding boxes and labels on faces"""
        for face in recognized_faces:
            top, right, bottom, left = face['location']
            
            # Choose color based on recognition
            if face['student_id']:
                color = (0, 255, 0)  # Green for recognized
                label = f"{face['name']} ({face['confidence']:.2f})"
            else:
                color = (0, 0, 255)  # Red for unknown
                label = "Unknown"
            
            # Draw rectangle
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Draw label background
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            
            # Draw label text
            cv2.putText(frame, label, (left + 6, bottom - 6), 
                       cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def start_face_recognition_mode(self):
        """Start face recognition attendance mode"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return False, "Could not access camera"
        
        print("Face Recognition Mode Started")
        print("Press 'q' to quit, 'r' to refresh student data")
        
        # Track recently marked students to avoid duplicate marking
        recently_marked = set()
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Process every 5th frame for performance
            if frame_count % 5 == 0:
                recognized_faces = self.recognize_faces(frame)
                
                # Mark attendance for recognized faces
                for face in recognized_faces:
                    if face['student_id'] and face['confidence'] > 0.5:
                        if face['student_id'] not in recently_marked:
                            success, message = self.attendance_mgr.mark_attendance(
                                face['student_id'], face['name'], "Face Recognition"
                            )
                            if success:
                                print(f"✓ {message}")
                                recently_marked.add(face['student_id'])
                            else:
                                print(f"⚠ {message}")
            else:
                # Use previous recognition results for display
                if 'recognized_faces' in locals():
                    pass
                else:
                    recognized_faces = []
            
            # Draw face boxes and labels
            frame = self.draw_face_boxes(frame, recognized_faces)
            
            # Add instructions
            cv2.putText(frame, "Face Recognition Mode - Press 'q' to quit", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Students registered: {len(self.known_encodings)}", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Clear recently marked every 300 frames (about 10 seconds at 30fps)
            if frame_count % 300 == 0:
                recently_marked.clear()
            
            cv2.imshow('Smart Attendance - Face Recognition', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                print("Refreshing student data...")
                self.refresh_data()
                recently_marked.clear()
            
            frame_count += 1
        
        cap.release()
        cv2.destroyAllWindows()
        return True, "Face recognition mode ended"
    
    def detect_faces_simple(self, frame):
        """Simple face detection using Haar cascades (faster alternative)"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        detected_faces = []
        for (x, y, w, h) in faces:
            # Convert to face_recognition format (top, right, bottom, left)
            face_location = (y, x + w, y + h, x)
            detected_faces.append({
                'student_id': None,
                'name': 'Detected Face',
                'location': face_location,
                'confidence': 0.8
            })
        
        return detected_faces
