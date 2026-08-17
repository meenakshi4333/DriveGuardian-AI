from ultralytics import YOLO


class PhoneDetector:

    def __init__(
        self,
        model_path="yolo11n.pt"
    ):

        self.model = YOLO(
            model_path
        )

    def detect(self, frame):

        results = self.model(
            frame,
            verbose=False
        )

        phone_detected = False

        detections = []

        for result in results:

            for box in result.boxes:

                class_id = int(
                    box.cls[0]
                )

                confidence = float(
                    box.conf[0]
                )

                class_name = (
                    self.model.names[
                        class_id
                    ]
                )

                if (
                    class_name == "cell phone"
                    and confidence >= 0.50
                ):

                    phone_detected = True

                    detections.append({
                        "object": "cell phone",
                        "confidence": confidence
                    })

        return {
            "phone_detected":
                phone_detected,

            "detections":
                detections
        }