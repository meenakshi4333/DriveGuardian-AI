import cv2
from eye_detection import EyeDetector


MODEL_PATH = "models/face_landmarker.task"

detector = EyeDetector(MODEL_PATH)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Could not open webcam")
    exit()


while True:

    success, frame = camera.read()

    if not success:
        print("Could not read camera")
        break

    result = detector.detect(frame)

    if result["face_detected"]:

        eye_state = result["eyes"]

        cv2.putText(
            frame,
            "Eyes: " + eye_state,
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        print(
            "Face Detected | Eyes:",
            eye_state,
            "| Left:",
            round(result["left_ratio"], 3),
            "| Right:",
            round(result["right_ratio"], 3)
        )

    else:

        cv2.putText(
            frame,
            "Face Not Detected",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        print("Face Not Detected")

    cv2.imshow(
        "DriveGuardian AI - Eye Detection",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()