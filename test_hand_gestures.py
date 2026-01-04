#!/usr/bin/env python3
"""
Local Hand Gesture Detection Test Script
Uses MediaPipe Hands to detect hand landmarks and gestures on Camera 1
Prints landmarks and detected gestures (OK, Peace, Stop, Fist)

This is a LOCAL TEST ONLY - not integrated with OBS yet
"""

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import ImageFormat
import sys
import os
import numpy as np

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

class HandGestureDetector:
    def __init__(self, camera_device='/dev/elp_1'):
        """
        Initialize hand gesture detector
        
        Args:
            camera_device: Path to camera device or numeric index (default: /dev/elp_1)
                          Use 0 for default laptop camera on macOS/Windows
        """
        # Convert string "0" to integer 0 for easier handling
        if isinstance(camera_device, str) and camera_device.isdigit():
            self.camera_device = int(camera_device)
        else:
            self.camera_device = camera_device
        
        # MediaPipe 0.10.x uses tasks-based API
        # Try to find model in script directory first (for local use), then project root
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = None
        
        # Check in script directory (for local standalone use)
        local_model = os.path.join(script_dir, 'hand_landmarker.task')
        if os.path.exists(local_model):
            model_path = local_model
        else:
            # Check in project models directory
            project_model = os.path.join(project_root, 'models', 'hand_landmarker.task')
            if os.path.exists(project_model):
                model_path = project_model
            else:
                # Try to download it to script directory
                print("Model not found. Downloading hand_landmarker.task...")
                import urllib.request
                model_url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
                try:
                    os.makedirs(script_dir, exist_ok=True)
                    urllib.request.urlretrieve(model_url, local_model)
                    model_path = local_model
                    print(f"Downloaded model to: {local_model}")
                except Exception as e:
                    print(f"ERROR: Could not download model: {e}")
                    print(f"Please manually download from: {model_url}")
                    print(f"Save it as: {local_model}")
                    raise FileNotFoundError(f"Model file not found and could not be downloaded")
        
        if not model_path or not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.hand_landmarker = vision.HandLandmarker.create_from_options(options)
        
        # Hand landmark indices (MediaPipe uses 21 landmarks)
        # https://google.github.io/mediapipe/solutions/hands.html
        self.LANDMARK_NAMES = [
            'WRIST', 'THUMB_CMC', 'THUMB_MCP', 'THUMB_IP', 'THUMB_TIP',
            'INDEX_FINGER_MCP', 'INDEX_FINGER_PIP', 'INDEX_FINGER_DIP', 'INDEX_FINGER_TIP',
            'MIDDLE_FINGER_MCP', 'MIDDLE_FINGER_PIP', 'MIDDLE_FINGER_DIP', 'MIDDLE_FINGER_TIP',
            'RING_FINGER_MCP', 'RING_FINGER_PIP', 'RING_FINGER_DIP', 'RING_FINGER_TIP',
            'PINKY_MCP', 'PINKY_PIP', 'PINKY_DIP', 'PINKY_TIP'
        ]
    
    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two 3D points"""
        return ((point1.x - point2.x)**2 + (point1.y - point2.y)**2 + (point1.z - point2.z)**2)**0.5
    
    def is_finger_extended(self, landmarks, finger_indices):
        """
        Check if a finger is extended
        
        Args:
            landmarks: MediaPipe hand landmarks
            finger_indices: List of 4 indices [MCP, PIP, DIP, TIP] for the finger
        
        Returns:
            True if finger is extended, False otherwise
        """
        # For thumb, check if tip is to the right (or left) of IP joint
        if finger_indices[0] == 1:  # Thumb
            return landmarks[finger_indices[3]].x > landmarks[finger_indices[2]].x
        else:
            # For other fingers, check if tip is above PIP joint
            return landmarks[finger_indices[3]].y < landmarks[finger_indices[1]].y
    
    def detect_gesture(self, landmarks):
        """
        Detect hand gesture from landmarks
        
        Returns:
            String name of detected gesture or None
        """
        if not landmarks:
            return None
        
        # Finger tip indices
        THUMB_TIP = 4
        INDEX_TIP = 8
        MIDDLE_TIP = 12
        RING_TIP = 16
        PINKY_TIP = 20
        
        # Finger base indices
        THUMB_IP = 3
        INDEX_PIP = 6
        MIDDLE_PIP = 10
        RING_PIP = 14
        PINKY_PIP = 18
        
        # Check finger states
        thumb_extended = landmarks[THUMB_TIP].x > landmarks[THUMB_IP].x
        index_extended = landmarks[INDEX_TIP].y < landmarks[INDEX_PIP].y
        middle_extended = landmarks[MIDDLE_TIP].y < landmarks[MIDDLE_PIP].y
        ring_extended = landmarks[RING_TIP].y < landmarks[RING_PIP].y
        pinky_extended = landmarks[PINKY_TIP].y < landmarks[PINKY_PIP].y
        
        # OK gesture: Thumb and index finger form a circle, others closed
        thumb_index_distance = self.calculate_distance(landmarks[THUMB_TIP], landmarks[INDEX_TIP])
        if thumb_index_distance < 0.05 and not middle_extended and not ring_extended and not pinky_extended:
            return "OK"
        
        # Peace gesture: Index and middle extended, others closed
        if index_extended and middle_extended and not thumb_extended and not ring_extended and not pinky_extended:
            return "PEACE"
        
        # Stop gesture: All fingers extended, palm facing camera
        if index_extended and middle_extended and ring_extended and pinky_extended:
            return "STOP"
        
        # Fist: All fingers closed
        if not index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return "FIST"
        
        return None
    
    def print_landmarks_new(self, landmarks_list, hand_landmarks):
        """Print all hand landmarks in a readable format (MediaPipe 0.10.x format)"""
        if not hand_landmarks:
            return
        
        print("\n" + "="*80)
        print("HAND LANDMARKS DETECTED")
        print("="*80)
        
        for idx, landmark in enumerate(landmarks_list):
            name = self.LANDMARK_NAMES[idx] if idx < len(self.LANDMARK_NAMES) else f"LANDMARK_{idx}"
            print(f"{name:20s} | X: {landmark.x:7.4f} | Y: {landmark.y:7.4f} | Z: {landmark.z:7.4f}")
        
        # Detect and print gesture
        gesture = self.detect_gesture(landmarks_list)
        if gesture:
            print(f"\n>>> DETECTED GESTURE: {gesture} <<<")
        else:
            print("\n>>> No recognized gesture detected <<<")
        
        print("="*80 + "\n")
    
    def run(self):
        """Main loop: capture from camera and detect hand gestures"""
        print(f"Starting hand gesture detection on {self.camera_device}")
        print("Press 'q' to quit")
        print("Gestures to test: OK, Peace, Stop, Fist\n")
        
        # Try to open camera device
        # Cross-platform support: try device path, then try as index, then try default (0)
        cap = None
        devices_to_try = []
        
        # Add the specified device first
        devices_to_try.append(self.camera_device)
        
        # On Linux, try common video device paths
        if sys.platform == 'linux':
            devices_to_try.extend(['/dev/video0', '/dev/video2', '/dev/video1'])
        
        # Also try as numeric index (for macOS/Windows or if path doesn't work)
        try:
            # Try to extract number from device path
            if 'video' in self.camera_device or 'elp' in self.camera_device.lower():
                import re
                numbers = re.findall(r'\d+', self.camera_device)
                if numbers:
                    devices_to_try.append(int(numbers[0]))
        except:
            pass
        
        # Always try default camera (index 0) as fallback
        devices_to_try.append(0)
        
        for device in devices_to_try:
            try:
                # Try as integer index first (works on all platforms)
                if isinstance(device, int):
                    cap = cv2.VideoCapture(device)
                # Try as device path (Linux)
                elif isinstance(device, str) and os.path.exists(device):
                    # If it's a symlink, try to resolve
                    if os.path.islink(device):
                        device_path = os.readlink(device)
                        if 'video' in device_path:
                            device_index = int(device_path.replace('video', ''))
                            cap = cv2.VideoCapture(device_index)
                        else:
                            continue
                    elif 'video' in device:
                        # Extract video device number
                        try:
                            device_index = int(device.replace('/dev/video', '').replace('/dev/elp_', ''))
                            cap = cv2.VideoCapture(device_index)
                        except:
                            # Try direct path
                            cap = cv2.VideoCapture(device)
                    else:
                        cap = cv2.VideoCapture(device)
                else:
                    continue
                
                if cap and cap.isOpened():
                    # Test if we can actually read a frame
                    ret, test_frame = cap.read()
                    if ret and test_frame is not None:
                        device_name = f"index {device}" if isinstance(device, int) else device
                        print(f"Opened camera: {device_name}")
                        break
                    else:
                        if cap:
                            cap.release()
                        cap = None
            except Exception as e:
                if cap:
                    cap.release()
                    cap = None
                continue
        
        if not cap or not cap.isOpened():
            print("ERROR: Could not open camera device")
            print(f"Tried: {devices_to_try}")
            print("\nTip: On macOS/Windows, try: python3 test_hand_gestures.py --camera 0")
            return
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        frame_count = 0
        last_gesture = None
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Failed to read frame from camera")
                    break
                
                frame_count += 1
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Convert BGR to RGB (MediaPipe requires RGB)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert to MediaPipe Image format
                mp_image = mp.Image(image_format=ImageFormat.SRGB, data=rgb_frame)
                
                # Process frame with MediaPipe 0.10.x API
                detection_result = self.hand_landmarker.detect(mp_image)
                
                # Draw hand landmarks on frame
                if detection_result.hand_landmarks:
                    for hand_landmarks in detection_result.hand_landmarks:
                        # Convert MediaPipe landmarks to drawing format
                        # MediaPipe 0.10.x returns normalized coordinates
                        h, w, _ = frame.shape
                        landmark_points = []
                        for landmark in hand_landmarks:
                            x = int(landmark.x * w)
                            y = int(landmark.y * h)
                            landmark_points.append((x, y))
                            # Draw landmark point
                            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                        
                        # Draw connections (simplified - draw key connections)
                        connections = [
                            (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
                            (0, 5), (5, 6), (6, 7), (7, 8),  # Index
                            (0, 9), (9, 10), (10, 11), (11, 12),  # Middle
                            (0, 13), (13, 14), (14, 15), (15, 16),  # Ring
                            (0, 17), (17, 18), (18, 19), (19, 20),  # Pinky
                            (5, 9), (9, 13), (13, 17)  # Base connections
                        ]
                        for start_idx, end_idx in connections:
                            if start_idx < len(landmark_points) and end_idx < len(landmark_points):
                                cv2.line(frame, landmark_points[start_idx], landmark_points[end_idx], (255, 0, 0), 2)
                        
                        # Detect gesture (convert to old format for compatibility)
                        # Create a simple landmark-like object
                        class Landmark:
                            def __init__(self, x, y, z):
                                self.x = x
                                self.y = y
                                self.z = z
                        
                        landmarks_list = [Landmark(lm.x, lm.y, lm.z) for lm in hand_landmarks]
                        gesture = self.detect_gesture(landmarks_list)
                        
                        # Print landmarks and gesture (only when gesture changes or every 30 frames)
                        if gesture != last_gesture or frame_count % 30 == 0:
                            self.print_landmarks_new(landmarks_list, hand_landmarks)
                            last_gesture = gesture
                        
                        # Draw gesture text on frame
                        if gesture:
                            cv2.putText(frame, f"GESTURE: {gesture}", (10, 30),
                                      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    # No hand detected
                    if frame_count % 60 == 0:
                        print("No hand detected in frame")
                
                # Display frame
                cv2.imshow('Hand Gesture Detection - Camera 1', frame)
                
                # Check for quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.hand_landmarker.close()
            print("\nHand gesture detection stopped")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test hand gesture detection on Camera 1')
    parser.add_argument('--camera', default='/dev/elp_1',
                       help='Camera device path or index (default: /dev/elp_1, use 0 for default laptop camera)')
    
    args = parser.parse_args()
    
    detector = HandGestureDetector(camera_device=args.camera)
    detector.run()
