from __future__ import division
import os
import cv2
import dlib
from .calibration import Calibration
import time


class BlinkTracking(object):
    def __init__(self, blink_threshold=1, required_blink_count=2, blink_timeout=100):
        self.frame = None
        self.left_eye = None
        self.right_eye = None
        self.prev_left_eye_dist = None
        self.prev_right_eye_dist = None

        self.blink_threshold = blink_threshold
        self.blink_count = 0
        self.first_blink_time = None
        self.last_blink_time = None
        self.left_blinking = False
        self.right_blinking = False

        self.calibration = Calibration()

        self.blink_threshold = blink_threshold
        self.required_blink_count = required_blink_count
        self.blink_timeout = blink_timeout
        self.blink_count = 0
        self.first_blink_time = None
        self.last_blink_time = 0

        self._face_detector = dlib.get_frontal_face_detector()
        cwd = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.abspath(os.path.join(cwd, "trained_models/shape_predictor_68_face_landmarks.dat"))
        self._predictor = dlib.shape_predictor(model_path)
        self.eye_color = (0, 0, 255)  # Red by default

    def _analyze(self):
        """Detects the position of the eyes"""
        frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_detector(frame_gray)

        for face in faces:
            landmarks = self._predictor(frame_gray, face)
            left_eye_coords = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)]
            right_eye_coords = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)]

            self.left_eye = left_eye_coords
            self.right_eye = right_eye_coords

            for coords in left_eye_coords + right_eye_coords:
                cv2.circle(self.frame, coords, 2, self.eye_color, -1)

    @staticmethod
    def _calculate_eye_distance(eye_coords, upper_index, lower_index):
        """Calculate the vertical distance between specified points of the eye"""
        return eye_coords[lower_index][1] - eye_coords[upper_index][1]

    def _check_blink(self):
        left_eye_upper_index, left_eye_lower_index = 1, 5
        right_eye_upper_index, right_eye_lower_index = 2, 4

        if self.left_eye and self.right_eye:
            left_eye_dist = self._calculate_eye_distance(self.left_eye, left_eye_upper_index, left_eye_lower_index)
            right_eye_dist = self._calculate_eye_distance(self.right_eye, right_eye_upper_index, right_eye_lower_index)

            if self.prev_left_eye_dist is not None:
                blink_occurred = abs(left_eye_dist - self.prev_left_eye_dist) > self.blink_threshold

                if blink_occurred and time.time() - self.last_blink_time > 0.3:
                    self.left_blinking = not self.left_blinking
                    self.right_blinking = not self.right_blinking

                    self.eye_color = (255, 255, 255) if self.left_blinking or self.right_blinking else (0, 0, 255)

                    self.last_blink_time = time.time()

                    if self.left_blinking or self.right_blinking:
                        self.blink_count += 1
                        self.last_blink_time = time.time()

                        if self.blink_count == 1:
                            self.first_blink_time = time.time()
                elif self.blink_count > 0 and time.time() - self.last_blink_time > 0.5:
                    self.left_blinking = False
                    self.right_blinking = False
                    self.eye_color = (0, 0, 255)
                    self.blink_count = 0

            self.prev_left_eye_dist = left_eye_dist
            self.prev_right_eye_dist = right_eye_dist

        return self.left_blinking, self.right_blinking

    def has_required_blinks_in_timeout(self):
        """Returns True if the required number of blinks occurred within the specified timeout."""
        current_time = time.time()

        if self.blink_count >= self.required_blink_count and current_time - self.first_blink_time < self.blink_timeout:
            self.blink_count = 0
            self.first_blink_time = None
            return True
        else:
            return False

    def refresh(self, frame):
        """Refreshes the frame and analyzes it."""
        self.frame = frame
        self._analyze()
        self._check_blink()

    def annotated_frame(self):
        """Returns the main frame with the eyes highlighted"""
        frame = self.frame.copy()

        if self.left_eye:
            for coords in self.left_eye:
                cv2.circle(frame, coords, 2, self.eye_color, -1)

        if self.right_eye:
            for coords in self.right_eye:
                cv2.circle(frame, coords, 2, self.eye_color, -1)

        return frame


class NoseTracking(object):
    def __init__(self):
        self.frame = None
        self.nose = None
        self.calibration = Calibration()
        self._face_detector = dlib.get_frontal_face_detector()
        cwd = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.abspath(os.path.join(cwd, "trained_models/shape_predictor_68_face_landmarks.dat"))
        self._predictor = dlib.shape_predictor(model_path)
        self.nose_located = False

    def _analyze(self):
        """Detects the position of the nose"""
        frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_detector(frame_gray)

        for face in faces:
            landmarks = self._predictor(frame_gray, face)
            nose_tip = (landmarks.part(30).x, landmarks.part(30).y)

            self.nose = nose_tip
            self.nose_located = True

            cv2.circle(self.frame, nose_tip, 3, (0, 255, 0), -1)

    def refresh(self, frame):
        """Refreshes the frame and analyzes it."""
        self.frame = frame
        self._analyze()

    def nose_coords(self):
        if self.nose_located:
            return self.nose

    def annotated_frame(self):
        """Returns the main frame with the nose tip highlighted"""
        frame = self.frame.copy()

        if self.nose:
            x_nose, y_nose = self.nose
            cv2.circle(frame, (x_nose, y_nose), 5, (0, 0, 255), -1)

        return frame
