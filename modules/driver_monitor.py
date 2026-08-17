class DriverMonitor:

    def __init__(self):

        # ==========================================
        # COUNTERS
        # ==========================================

        self.yawn_count = 0

        # ==========================================
        # PREVIOUS STATES
        # ==========================================

        self.previous_yawning = False
        self.previous_phone = False
        self.previous_drowsy = False
        self.previous_face_detected = True
        self.previous_head_direction = "Forward"

    # ==========================================
    # RESET DETECTION STATE
    # ==========================================

    def reset(self):

        self.yawn_count = 0

        self.previous_yawning = False
        self.previous_phone = False
        self.previous_drowsy = False
        self.previous_face_detected = True
        self.previous_head_direction = "Forward"

    # ==========================================
    # ANALYZE DRIVER
    # ==========================================

    def analyze(
        self,
        drowsiness_result,
        yawn_result,
        head_result,
        phone_result,
        face_detected
    ):

        # ==========================================
        # START RISK CALCULATION
        # ==========================================

        risk_score = 0

        alerts = []

        # ==========================================
        # CURRENT STATES
        # ==========================================

        current_drowsy = (
            drowsiness_result ==
            "DROWSINESS DETECTED"
        )

        current_yawning = (
            yawn_result ==
            "YAWNING"
        )

        current_phone = phone_result.get(
            "phone_detected",
            False
        )

        direction = head_result.get(
            "direction",
            "Unknown"
        )

        # ==========================================
        # FACE DETECTION
        # ==========================================

        if not face_detected:

            risk_score += 20

            # Alert only when face disappears
            if self.previous_face_detected:

                alerts.append(
                    "Face not detected"
                )

        # ==========================================
        # DROWSINESS
        # ==========================================

        if current_drowsy:

            risk_score += 70

            # Alert only when drowsiness starts
            if not self.previous_drowsy:

                alerts.append(
                    "Drowsiness detected"
                )

        # ==========================================
        # YAWNING
        # ==========================================

        if current_yawning:

            risk_score += 20

            # Count only when yawning starts
            if not self.previous_yawning:

                self.yawn_count += 1

                alerts.append(
                    "Yawning detected"
                )

        # ==========================================
        # HEAD TURN
        # ==========================================

        if direction == "Looking Left":

            risk_score += 20

            # Alert only when changing
            # from another direction to left

            if (
                self.previous_head_direction
                !=
                "Looking Left"
            ):

                alerts.append(
                    "Driver looking left"
                )

        elif direction == "Looking Right":

            risk_score += 20

            # Alert only when changing
            # from another direction to right

            if (
                self.previous_head_direction
                !=
                "Looking Right"
            ):

                alerts.append(
                    "Driver looking right"
                )

        # ==========================================
        # MOBILE PHONE
        # ==========================================

        if current_phone:

            # Mobile phone is critical
            risk_score += 70

            # Alert only when phone appears
            if not self.previous_phone:

                alerts.append(
                    "Mobile phone detected"
                )

        # ==========================================
        # SAVE CURRENT STATES
        # ==========================================

        self.previous_yawning = (
            current_yawning
        )

        self.previous_phone = (
            current_phone
        )

        self.previous_drowsy = (
            current_drowsy
        )

        self.previous_face_detected = (
            face_detected
        )

        self.previous_head_direction = (
            direction
        )

        # ==========================================
        # LIMIT RISK SCORE
        # ==========================================

        risk_score = min(
            risk_score,
            100
        )

        # ==========================================
        # DRIVER STATUS
        # ==========================================

        if risk_score <= 30:

            status = "SAFE"

        elif risk_score <= 60:

            status = "WARNING"

        else:

            status = "CRITICAL"

        # ==========================================
        # RETURN STATUS
        # ==========================================

        return {

            "status": status,

            "risk_score": risk_score,

            "alerts": alerts,

            "yawn_count":
                self.yawn_count,

            "head_direction":
                direction,

            "phone_detected":
                current_phone,

            "face_detected":
                face_detected
        }