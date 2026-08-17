import cv2
import os

from modules.face_detection import FaceDetector
from modules.eye_detection import EyeDetector
from modules.drowsiness_detection import DrowsinessDetector
from modules.yawn_detection import YawnDetector
from modules.head_turn_detection import HeadTurnDetector
from modules.phone_detection import PhoneDetector
from modules.driver_monitor import DriverMonitor


class Camera:

    def __init__(self):

        # ==========================================
        # CAMERA
        # ==========================================

        self.camera = None
        self.running = False

        # ==========================================
        # PROJECT ROOT
        # ==========================================

        project_root = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        # ==========================================
        # MODEL PATHS
        # ==========================================

        face_model = os.path.join(
            project_root,
            "models",
            "blaze_face_short_range.tflite"
        )

        landmark_model = os.path.join(
            project_root,
            "models",
            "face_landmarker.task"
        )

        phone_model = os.path.join(
            project_root,
            "yolo11n.pt"
        )

        # ==========================================
        # INITIALIZE DETECTORS
        # ==========================================

        print("Loading Face Detector...")
        self.face_detector = FaceDetector(
            face_model
        )

        print("Loading Eye Detector...")
        self.eye_detector = EyeDetector(
            landmark_model
        )

        print("Loading Drowsiness Detector...")
        self.drowsiness_detector = (
            DrowsinessDetector(
                closed_time=2.0,
                grace_time=0.5
            )
        )

        print("Loading Yawn Detector...")
        self.yawn_detector = YawnDetector(
            landmark_model
        )

        print("Loading Head Turn Detector...")
        self.head_detector = HeadTurnDetector(
            landmark_model
        )

        print("Loading Phone Detector...")
        self.phone_detector = PhoneDetector(
            phone_model
        )

        print("Loading Driver Monitor...")
        self.driver_monitor = DriverMonitor()

        # ==========================================
        # CURRENT STATUS
        # ==========================================

        self.face_detected = False

        self.latest_status = (
            self.get_default_status()
        )

        print(
            "All detection modules loaded successfully."
        )

        print(
            "Camera is OFF. Press Start Detection to start."
        )

    # ==========================================
    # DEFAULT STATUS
    # ==========================================

    def get_default_status(self):

        return {

            "status": "SAFE",

            "risk_score": 0,

            "alerts": [],

            "yawn_count": 0,

            "head_direction": "Forward",

            "phone_detected": False,

            "face_detected": False,

            "eye_state": "Unknown",

            "drowsy": False
        }

    # ==========================================
    # RESET DETECTION STATE
    # ==========================================

    def reset_detection_state(self):

        print(
            "Resetting detection state..."
        )

        # ------------------------------------------
        # Reset Drowsiness Detector
        # ------------------------------------------

        self.drowsiness_detector.eye_closed_start = None

        self.drowsiness_detector.last_closed_time = None

        self.drowsiness_detector.drowsy = False

        # ------------------------------------------
        # Reset Driver Monitor
        # ------------------------------------------

        self.driver_monitor.yawn_count = 0

        self.driver_monitor.previous_yawning = False

        self.driver_monitor.previous_phone = False

        # ------------------------------------------
        # Reset Camera Status
        # ------------------------------------------

        self.face_detected = False

        self.latest_status = (
            self.get_default_status()
        )

        print(
            "Detection state reset successfully."
        )

    # ==========================================
    # START CAMERA
    # ==========================================

    def start(self):

        # ------------------------------------------
        # Already running
        # ------------------------------------------

        if self.running:

            print(
                "Camera is already running."
            )

            return True

        # ------------------------------------------
        # Fresh detection session
        # ------------------------------------------

        self.reset_detection_state()

        print(
            "Starting webcam..."
        )

        # ------------------------------------------
        # Open webcam
        # ------------------------------------------

        try:

            self.camera = cv2.VideoCapture(0)

        except Exception as e:

            print(
                "ERROR creating VideoCapture:",
                repr(e)
            )

            self.camera = None
            self.running = False

            return False

        # ------------------------------------------
        # Check webcam
        # ------------------------------------------

        if (
            self.camera is None
            or not self.camera.isOpened()
        ):

            print(
                "ERROR: Could not open webcam."
            )

            if self.camera is not None:

                self.camera.release()

            self.camera = None

            self.running = False

            return False

        # ------------------------------------------
        # Camera successfully opened
        # ------------------------------------------

        self.running = True

        print(
            "Webcam started successfully."
        )

        print(
            "New detection session started."
        )

        return True

    # ==========================================
    # STOP CAMERA
    # ==========================================

    def stop(self):

        print(
            "Stopping webcam..."
        )

        self.running = False

        if self.camera is not None:

            try:

                if self.camera.isOpened():

                    self.camera.release()

            except Exception as e:

                print(
                    "Camera release error:",
                    repr(e)
                )

        self.camera = None

        self.reset_detection_state()

        print(
            "Webcam stopped."
        )

        print(
            "Detection session completely reset."
        )

    # ==========================================
    # CAMERA RUNNING STATUS
    # ==========================================

    def is_running(self):

        return self.running

    # ==========================================
    # GET CAMERA FRAME
    # ==========================================

    def get_frame(self):

        if (
            not self.running
            or self.camera is None
        ):

            return None

        success, frame = (
            self.camera.read()
        )

        if not success:

            print(
                "ERROR: Could not read frame from camera"
            )

            self.stop()

            return None

        try:

            # ======================================
            # FACE DETECTION
            # ======================================

            face_result = (
                self.face_detector.detect(frame)
            )

            self.face_detected = bool(
                face_result.detections
            )

            # ======================================
            # DEFAULT RESULTS
            # ======================================

            eye_result = {

                "face_detected": False,

                "eyes": "Unknown",

                "left_ratio": 0,

                "right_ratio": 0
            }

            yawn_result = {

                "face_detected": False,

                "yawning": False,

                "mouth_ratio": 0
            }

            head_result = {

                "face_detected": False,

                "direction": "Unknown",

                "yaw": 0
            }

            phone_result = {

                "phone_detected": False,

                "detections": []
            }

            drowsiness_result = {

                "drowsy": False,

                "closed_duration": 0
            }

            # ======================================
            # FACE BASED DETECTION
            # ======================================

            if self.face_detected:

                eye_result = (
                    self.eye_detector.detect(
                        frame
                    )
                )

                drowsiness_result = (
                    self.drowsiness_detector.update(
                        eye_result["eyes"]
                    )
                )

                yawn_result = (
                    self.yawn_detector.detect(
                        frame
                    )
                )

                head_result = (
                    self.head_detector.detect(
                        frame
                    )
                )

            else:

                self.drowsiness_detector.eye_closed_start = None

                self.drowsiness_detector.last_closed_time = None

                self.drowsiness_detector.drowsy = False

            # ======================================
            # PHONE DETECTION
            # ======================================

            phone_result = (
                self.phone_detector.detect(
                    frame
                )
            )

            # ======================================
            # DROWSINESS TEXT
            # ======================================

            if drowsiness_result["drowsy"]:

                drowsiness_text = (
                    "DROWSINESS DETECTED"
                )

            else:

                drowsiness_text = (
                    "DRIVER NORMAL"
                )

            # ======================================
            # DRIVER MONITOR
            # ======================================

            self.latest_status = (
                self.driver_monitor.analyze(

                    drowsiness_text,

                    (
                        "YAWNING"
                        if yawn_result["yawning"]
                        else "NORMAL"
                    ),

                    head_result,

                    phone_result,

                    self.face_detected
                )
            )

            # ======================================
            # EXTRA STATUS
            # ======================================

            self.latest_status["eye_state"] = (
                eye_result["eyes"]
            )

            self.latest_status["drowsy"] = (
                drowsiness_result["drowsy"]
            )

            self.latest_status["face_detected"] = (
                self.face_detected
            )

            # ======================================
            # FACE BOX
            # ======================================

            if face_result.detections:

                for detection in (
                    face_result.detections
                ):

                    bbox = (
                        detection.bounding_box
                    )

                    x = int(
                        bbox.origin_x
                    )

                    y = int(
                        bbox.origin_y
                    )

                    w = int(
                        bbox.width
                    )

                    h = int(
                        bbox.height
                    )

                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x + w, y + h),
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        frame,
                        "Face Detected",
                        (
                            x,
                            max(y - 10, 20)
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

            else:

                cv2.putText(
                    frame,
                    "No Face Detected",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

            # ======================================
            # EYE STATUS
            # ======================================

            cv2.putText(
                frame,
                "Eyes: " +
                str(
                    eye_result["eyes"]
                ),
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            # ======================================
            # HEAD STATUS
            # ======================================

            cv2.putText(
                frame,
                "Head: " +
                str(
                    head_result["direction"]
                ),
                (20, 115),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            # ======================================
            # PHONE STATUS
            # ======================================

            cv2.putText(
                frame,
                "Phone: " +
                (
                    "Detected"
                    if phone_result[
                        "phone_detected"
                    ]
                    else "Not Detected"
                ),
                (20, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            # ======================================
            # RISK SCORE
            # ======================================

            cv2.putText(
                frame,
                "Risk Score: " +
                str(
                    self.latest_status.get(
                        "risk_score",
                        0
                    )
                ),
                (20, 185),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            # ======================================
            # DRIVER STATUS
            # ======================================

            cv2.putText(
                frame,
                "Status: " +
                str(
                    self.latest_status.get(
                        "status",
                        "SAFE"
                    )
                ),
                (20, 220),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            # ======================================
            # JPEG
            # ======================================

            success, buffer = (
                cv2.imencode(
                    ".jpg",
                    frame
                )
            )

            if not success:

                print(
                    "ERROR: Could not encode frame"
                )

                return None

            return buffer.tobytes()

        except Exception as e:

            print(
                "ERROR inside get_frame():",
                repr(e)
            )

            success, buffer = (
                cv2.imencode(
                    ".jpg",
                    frame
                )
            )

            if success:

                return buffer.tobytes()

            return None

    # ==========================================
    # FACE STATUS
    # ==========================================

    def is_face_detected(self):

        return self.face_detected

    # ==========================================
    # DRIVER STATUS
    # ==========================================

    def get_status(self):

        return self.latest_status

    # ==========================================
    # RELEASE CAMERA
    # ==========================================

    def release(self):

        self.stop()