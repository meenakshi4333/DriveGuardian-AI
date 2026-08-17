import cv2

from eye_detection import EyeDetector
from drowsiness_detection import DrowsinessDetector


MODEL_PATH = "models/face_landmarker.task"


eye_detector = EyeDetector(MODEL_PATH)

drowsiness_detector = DrowsinessDetector(
    closed_time=2.0
)


camera = cv2.VideoCapture(0)


if not camera.isOpened():

    print("Could not open webcam")
    exit()


while True:

    success, frame = camera.read()

    if not success:

        print("Could not read camera")
        break


    # Detect eyes
    eye_result = eye_detector.detect(frame)


    if eye_result["face_detected"]:

        eye_state = eye_result["eyes"]


        # Check drowsiness
        drowsiness_result = (
            drowsiness_detector.update(
                eye_state
            )
        )


        if drowsiness_result["drowsy"]:

            status = "DROWSINESS DETECTED"

            color = (0, 0, 255)

        else:

            status = "DRIVER NORMAL"

            color = (0, 255, 0)


        cv2.putText(
            frame,
            "Eyes: " + eye_state,
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )


        cv2.putText(
            frame,
            status,
            (30, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )


        print(
    "Eyes:",
    eye_state,
    "| Closed for:",
    round(
        drowsiness_result["closed_duration"],
        1
    ),
    "seconds |",
    status
)


    else:

         cv2.putText(
    frame,
    "Closed: " + str(
        round(
            drowsiness_result["closed_duration"],
            1
        )
    ) + " sec",
    (30, 130),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    color,
    2
)


    cv2.imshow(
        "DriveGuardian AI - Drowsiness Test",
        frame
    )


    key = cv2.waitKey(1) & 0xFF


    if key == ord("q"):

        break


camera.release()

cv2.destroyAllWindows()