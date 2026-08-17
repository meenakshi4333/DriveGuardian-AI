import cv2
from face_detection import FaceDetector


MODEL_PATH = "../models/blaze_face_short_range.tflite"

detector = FaceDetector(MODEL_PATH)

camera = cv2.VideoCapture(0)

while True:

    success, frame = camera.read()

    if not success:
        print("Camera could not be opened")
        break

    result = detector.detect(frame)

    if result.detections:

        print("Face Detected")

        for detection in result.detections:

            bbox = detection.bounding_box

            x = bbox.origin_x
            y = bbox.origin_y
            w = bbox.width
            h = bbox.height

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

    else:

        print("No Face Detected")

    cv2.imshow(
        "DriveGuardian AI - Face Detection",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()