import cv2

from head_turn_detection import HeadTurnDetector


MODEL_PATH = "models/face_landmarker.task"


detector = HeadTurnDetector(MODEL_PATH)

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

        direction = result["direction"]

        if direction == "Forward":

            status = "LOOKING FORWARD"
            color = (0, 255, 0)

        else:

            status = direction
            color = (0, 0, 255)

        cv2.putText(
            frame,
            status,
            (30, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            color,
            2
        )

        print(
            "Head:",
            direction
        )

    else:

        cv2.putText(
            frame,
            "FACE NOT DETECTED",
            (30, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            2
        )

        print("Face Not Detected")

    cv2.imshow(
        "DriveGuardian AI - Head Turn Detection",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):

        break


camera.release()
cv2.destroyAllWindows()