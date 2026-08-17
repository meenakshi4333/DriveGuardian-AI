import cv2
import mediapipe as mp
import math

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class EyeDetector:

    def __init__(self, model_path):

        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_faces=1
        )

        self.landmarker = vision.FaceLandmarker.create_from_options(
            options
        )

    def distance(self, p1, p2):

        return math.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2
        )

    def eye_ratio(self, landmarks, points):

        p1 = landmarks[points[0]]
        p2 = landmarks[points[1]]
        p3 = landmarks[points[2]]
        p4 = landmarks[points[3]]
        p5 = landmarks[points[4]]
        p6 = landmarks[points[5]]

        vertical_1 = self.distance(p2, p6)
        vertical_2 = self.distance(p3, p5)

        horizontal = self.distance(p1, p4)

        if horizontal == 0:
            return 0

        ratio = (
            vertical_1 + vertical_2
        ) / (2 * horizontal)

        return ratio

    def detect(self, frame):

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        result = self.landmarker.detect(mp_image)

        if not result.face_landmarks:

            return {
                "face_detected": False,
                "eyes": "Unknown",
                "left_ratio": 0,
                "right_ratio": 0
            }

        landmarks = result.face_landmarks[0]

        # Left eye
        left_eye = [
            33,
            160,
            158,
            133,
            153,
            144
        ]

        # Right eye
        right_eye = [
            362,
            385,
            387,
            263,
            373,
            380
        ]

        left_ratio = self.eye_ratio(
            landmarks,
            left_eye
        )

        right_ratio = self.eye_ratio(
            landmarks,
            right_eye
        )

        average_ratio = (
            left_ratio + right_ratio
        ) / 2

        # Eye classification
        if average_ratio < 0.20:

            eye_state = "Closed"

        else:

            eye_state = "Open"

        return {
            "face_detected": True,
            "eyes": eye_state,
            "left_ratio": left_ratio,
            "right_ratio": right_ratio
        }