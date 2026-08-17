import time


class DrowsinessDetector:

    def __init__(self, closed_time=2.0, grace_time=0.5):

        self.closed_time = closed_time
        self.grace_time = grace_time

        self.eye_closed_start = None
        self.last_closed_time = None

        self.drowsy = False

    # ==========================================
    # RESET DETECTION
    # ==========================================

    def reset(self):

        self.eye_closed_start = None
        self.last_closed_time = None
        self.drowsy = False

    # ==========================================
    # UPDATE
    # ==========================================

    def update(self, eye_state):

        current_time = time.time()

        # ==========================================
        # EYES CLOSED
        # ==========================================

        if eye_state == "Closed":

            if self.eye_closed_start is None:

                self.eye_closed_start = current_time

            self.last_closed_time = current_time

        # ==========================================
        # EYES OPEN
        # ==========================================

        elif eye_state == "Open":

            if self.eye_closed_start is not None:

                time_since_closed = (
                    current_time - self.last_closed_time
                )

                if time_since_closed > self.grace_time:

                    self.eye_closed_start = None
                    self.last_closed_time = None
                    self.drowsy = False

        # ==========================================
        # CALCULATE CLOSED DURATION
        # ==========================================

        if self.eye_closed_start is not None:

            closed_duration = (
                current_time - self.eye_closed_start
            )

            if closed_duration >= self.closed_time:

                self.drowsy = True

        else:

            closed_duration = 0
            self.drowsy = False

        return {
            "drowsy": self.drowsy,
            "closed_duration": closed_duration
        }