import cv2
import mediapipe as mp
import numpy as np
from attendance_manager import AttendanceManager
from student_registration import StudentRegistration
import tkinter as tk
from tkinter import simpledialog

class GestureDetection:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.attendance_mgr = AttendanceManager()
        self.student_reg = StudentRegistration()
        
    def is_hand_raised(self, landmarks):
        """Check if hand is raised (palm facing camera, fingers up)"""
        if not landmarks:
            return False
        
        # Get landmark positions
        wrist = landmarks[0]
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        # Check if fingers are extended (tips above their respective MCP joints)
        thumb_extended = thumb_tip.y < landmarks[3].y
        index_extended = index_tip.y < landmarks[6].y
        middle_extended = middle_tip.y < landmarks[10].y
        ring_extended = ring_tip.y < landmarks[14].y
        pinky_extended = pinky_tip.y < landmarks[18].y
        
        # Hand is raised if at least 3 fingers are extended and hand is above wrist level
        fingers_up = sum([thumb_extended, index_extended, middle_extended, ring_extended, pinky_extended])
        hand_raised = fingers_up >= 3 and index_tip.y < wrist.y
        
        return hand_raised
    
    def detect_raised_hand(self, frame):
        """Detect raised hand gesture in frame"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        raised_hands = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if self.is_hand_raised(hand_landmarks.landmark):
                    raised_hands.append(hand_landmarks)
        
        return raised_hands, results
    
    def draw_hand_landmarks(self, frame, results):
        """Draw hand landmarks on frame"""
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
        return frame
    
    def get_student_id_input(self):
        """Get student ID input from user"""
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        student_id = simpledialog.askstring(
            "Student ID", 
            "Hand gesture detected!\nEnter your Student ID:",
            parent=root
        )
        
        root.destroy()
        return student_id
    
    def start_gesture_detection_mode(self):
        """Start gesture detection attendance mode"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return False, "Could not access camera"
        
        print("Gesture Detection Mode Started")
        print("Raise your hand to mark attendance")
        print("Press 'q' to quit")
        
        gesture_detected = False
        gesture_frames = 0
        required_frames = 15  # Require gesture for 15 consecutive frames
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Detect raised hands
            raised_hands, results = self.detect_raised_hand(frame)
            
            # Draw hand landmarks
            frame = self.draw_hand_landmarks(frame, results)
            
            # Check for raised hand gesture
            if raised_hands:
                gesture_frames += 1
                cv2.putText(frame, f"Hand Raised! ({gesture_frames}/{required_frames})", 
                           (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Draw bounding box around raised hands
                for hand_landmarks in raised_hands:
                    h, w, c = frame.shape
                    x_coords = [int(lm.x * w) for lm in hand_landmarks.landmark]
                    y_coords = [int(lm.y * h) for lm in hand_landmarks.landmark]
                    
                    x_min, x_max = min(x_coords), max(x_coords)
                    y_min, y_max = min(y_coords), max(y_coords)
                    
                    cv2.rectangle(frame, (x_min-20, y_min-20), (x_max+20, y_max+20), (0, 255, 0), 3)
                
                # If gesture detected for required frames, prompt for student ID
                if gesture_frames >= required_frames and not gesture_detected:
                    gesture_detected = True
                    
                    # Get student ID
                    student_id = self.get_student_id_input()
                    
                    if student_id:
                        # Get student info
                        student = self.student_reg.get_student_by_id(student_id)
                        
                        if student:
                            # Mark attendance
                            success, message = self.attendance_mgr.mark_attendance(
                                student_id, student['name'], "Gesture Detection"
                            )
                            print(f"{'✓' if success else '⚠'} {message}")
                        else:
                            print(f"⚠ Student ID {student_id} not found")
                    else:
                        print("⚠ No student ID entered")
                    
                    # Reset gesture detection
                    gesture_frames = 0
                    gesture_detected = False
            else:
                gesture_frames = 0
                gesture_detected = False
            
            # Add instructions
            cv2.putText(frame, "Gesture Detection Mode - Raise hand to mark attendance", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to quit", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.imshow('Smart Attendance - Gesture Detection', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return True, "Gesture detection mode ended"
    
    def test_gesture_detection(self):
        """Test gesture detection without attendance marking"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return False, "Could not access camera"
        
        print("Testing Gesture Detection - Press 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            raised_hands, results = self.detect_raised_hand(frame)
            frame = self.draw_hand_landmarks(frame, results)
            
            if raised_hands:
                cv2.putText(frame, "HAND RAISED DETECTED!", 
                           (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            
            cv2.putText(frame, "Test Mode - Raise your hand", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Gesture Test', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return True, "Gesture test completed"
