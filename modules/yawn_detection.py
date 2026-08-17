import cv2
import mediapipe as mp
import math

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class YawnDetector:

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
                "yawning": False,
                "mouth_ratio": 0
            }

        landmarks = result.face_landmarks[0]

        # Mouth landmarks
        top_lip = landmarks[13]
        bottom_lip = landmarks[14]

        left_mouth = landmarks[78]
        right_mouth = landmarks[308]

        vertical = self.distance(
            top_lip,
            bottom_lip
        )

        horizontal = self.distance(
            left_mouth,
            right_mouth
        )

        if horizontal == 0:

            mouth_ratio = 0

        else:

            mouth_ratio = vertical / horizontal

        # Yawn threshold
        if mouth_ratio > 0.35:

            yawning = True

        else:

            yawning = False

        return {
            "face_detected": True,
            "yawning": yawning,
            "mouth_ratio": mouth_ratio
        }