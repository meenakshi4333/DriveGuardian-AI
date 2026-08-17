import cv2

from phone_detection import PhoneDetector


detector = PhoneDetector()

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


    if result["phone_detected"]:

        status = "PHONE DETECTED"
        color = (0, 0, 255)

        for detection in result["detections"]:

            print(
                "Phone detected | Confidence:",
                round(
                    detection["confidence"],
                    2
                )
            )

    else:

        status = "NO PHONE DETECTED"
        color = (0, 255, 0)


    cv2.putText(
        frame,
        status,
        (30, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        color,
        2
    )


    cv2.imshow(
        "DriveGuardian AI - Phone Detection",
        frame
    )


    key = cv2.waitKey(1) & 0xFF


    if key == ord("q"):

        break


camera.release()

cv2.destroyAllWindows()