#!/usr/bin/env python3
"""
Training script for collecting thumbs up gesture data
Captures hand landmarks when user presses SPACE, saves to CSV for analysis
"""

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import ImageFormat
import csv
import os
import sys
import numpy as np
from datetime import datetime

# Import the detector to use same model
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_hand_gestures import HandGestureDetector

class ThumbsUpTrainer:
    def __init__(self, camera_device=0, output_file='thumbs_up_training_data.csv'):
        self.detector = HandGestureDetector(camera_device=camera_device)
        self.output_file = output_file
        self.samples_collected = 0
        
        # Initialize CSV file with headers
        if not os.path.exists(output_file):
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                # Write header: 21 landmarks * 3 coordinates (x, y, z) = 63 columns + gesture label
                header = ['gesture'] + [f'lm_{i}_{coord}' for i in range(21) for coord in ['x', 'y', 'z']]
                writer.writerow(header)
    
    def save_sample(self, landmarks, gesture_label='THUMBS_UP'):
        """Save a single sample to CSV"""
        row = [gesture_label]
        for lm in landmarks:
            row.extend([lm.x, lm.y, lm.z])
        
        with open(self.output_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        
        self.samples_collected += 1
        return self.samples_collected
    
    def run(self):
        """Main training loop"""
        print("="*80)
        print("THUMBS UP GESTURE TRAINING")
        print("="*80)
        print(f"Output file: {self.output_file}")
        print("\nInstructions:")
        print("  - Show thumbs up gesture to camera")
        print("  - Press SPACE to capture sample")
        print("  - Press 'q' to quit")
        print("  - Press 'r' to reset counter")
        print(f"\nStarting collection...\n")
        
        cap = cv2.VideoCapture(self.detector.camera_device if isinstance(self.detector.camera_device, int) else 0)
        
        if not cap.isOpened():
            print(f"ERROR: Could not open camera {self.detector.camera_device}")
            return
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                frame = cv2.flip(frame, 1)
                
                # Get frame dimensions (needed for drawing)
                h, w, _ = frame.shape
                
                # Convert to RGB for MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=ImageFormat.SRGB, data=rgb_frame)
                
                # Detect hands
                detection_result = self.detector.hand_landmarker.detect(mp_image)
                
                # Draw landmarks and detect gesture
                if detection_result.hand_landmarks:
                    for hand_landmarks in detection_result.hand_landmarks:
                        landmark_points = []
                        
                        for landmark in hand_landmarks:
                            x = int(landmark.x * w)
                            y = int(landmark.y * h)
                            landmark_points.append((x, y))
                            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                        
                        # Detect gesture
                        class Landmark:
                            def __init__(self, x, y, z):
                                self.x = x
                                self.y = y
                                self.z = z
                        
                        landmarks_list = [Landmark(lm.x, lm.y, lm.z) for lm in hand_landmarks]
                        gesture = self.detector.detect_gesture(landmarks_list)
                        
                        # Draw gesture text
                        if gesture:
                            cv2.putText(frame, f"GESTURE: {gesture}", (10, 30),
                                      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        # Draw sample count
                        cv2.putText(frame, f"Samples: {self.samples_collected}", (10, 70),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                # Instructions
                cv2.putText(frame, "SPACE: Capture | Q: Quit | R: Reset", (10, h - 20),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                cv2.imshow('Thumbs Up Training', frame)
                
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    break
                elif key == ord(' '):  # SPACE to capture
                    if detection_result.hand_landmarks:
                        for hand_landmarks in detection_result.hand_landmarks:
                            class Landmark:
                                def __init__(self, x, y, z):
                                    self.x = x
                                    self.y = y
                                    self.z = z
                            
                            landmarks_list = [Landmark(lm.x, lm.y, lm.z) for lm in hand_landmarks]
                            count = self.save_sample(landmarks_list, 'THUMBS_UP')
                            print(f"Sample {count} saved!")
                    else:
                        print("No hand detected - sample not saved")
                elif key == ord('r'):
                    self.samples_collected = 0
                    print("Counter reset")
        
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.detector.hand_landmarker.close()
            print(f"\nTraining complete! Collected {self.samples_collected} samples")
            print(f"Data saved to: {self.output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Collect thumbs up gesture training data')
    parser.add_argument('--camera', default=0, type=int,
                       help='Camera device index (default: 0)')
    parser.add_argument('--output', default='thumbs_up_training_data.csv',
                       help='Output CSV file (default: thumbs_up_training_data.csv)')
    
    args = parser.parse_args()
    
    trainer = ThumbsUpTrainer(camera_device=args.camera, output_file=args.output)
    trainer.run()
