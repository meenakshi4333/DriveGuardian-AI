import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HeadTurnDetector:

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
                "direction": "Unknown",
                "yaw": 0
            }

        landmarks = result.face_landmarks[0]

        # Important face landmarks
        nose = landmarks[1]
        left_cheek = landmarks[234]
        right_cheek = landmarks[454]

        # Calculate the horizontal position
        # of the nose relative to the face.
        face_width = (
            right_cheek.x - left_cheek.x
        )

        if face_width == 0:

            return {
                "face_detected": True,
                "direction": "Forward",
                "yaw": 0
            }

        nose_position = (
            nose.x - left_cheek.x
        ) / face_width

        # Determine head direction
        if nose_position < 0.35:

            direction = "Looking Left"

        elif nose_position > 0.65:

            direction = "Looking Right"

        else:

            direction = "Forward"

        return {
            "face_detected": True,
            "direction": direction,
            "yaw": nose_position
        }