import cv2

from yawn_detection import YawnDetector


MODEL_PATH = "models/face_landmarker.task"


detector = YawnDetector(MODEL_PATH)

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

        mouth_ratio = result["mouth_ratio"]

        if result["yawning"]:

            status = "YAWNING"
            color = (0, 0, 255)

        else:

            status = "NORMAL"
            color = (0, 255, 0)

        cv2.putText(
            frame,
            "Mouth Ratio: " + str(
                round(mouth_ratio, 2)
            ),
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
            0.9,
            color,
            2
        )

        print(
            "Mouth Ratio:",
            round(mouth_ratio, 3),
            "|",
            status
        )

    else:

        cv2.putText(
            frame,
            "Face Not Detected",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

        print("Face Not Detected")

    cv2.imshow(
        "DriveGuardian AI - Yawn Detection",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):

        break


camera.release()
cv2.destroyAllWindows()