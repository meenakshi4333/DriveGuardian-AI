// ==========================================
// DriveGuardian AI
// Complete Frontend JavaScript
// Risk Score Improved Version
// ==========================================


// ==========================================
// VARIABLES
// ==========================================

let detectionRunning = false;

let startTime = null;

let durationTimer = null;

let statusTimer = null;

let previousAlerts = new Set();

let previousEyeState = "Unknown";

let previousHeadDirection = "Forward";

let previousPhoneDetected = false;


// ==========================================
// HTML ELEMENTS
// ==========================================

const startBtn =
    document.getElementById("startBtn");

const stopBtn =
    document.getElementById("stopBtn");

const cameraStatus =
    document.getElementById("cameraStatus");

const videoFeed =
    document.getElementById("videoFeed");

const cameraMessage =
    document.getElementById("cameraMessage");

const driverStatus =
    document.getElementById("driverStatus");

const statusText =
    document.getElementById("statusText");

const statusMessage =
    document.getElementById("statusMessage");

const riskScore =
    document.getElementById("riskScore");

const riskProgress =
    document.getElementById("riskProgress");

const faceStatus =
    document.getElementById("faceStatus");

const eyeStatus =
    document.getElementById("eyeStatus");

const drowsinessStatus =
    document.getElementById("drowsinessStatus");

const yawnCountElement =
    document.getElementById("yawnCount");

const headStatus =
    document.getElementById("headStatus");

const phoneStatus =
    document.getElementById("phoneStatus");

const tripDuration =
    document.getElementById("tripDuration");

const eyeEventsElement =
    document.getElementById("eyeEvents");

const headEventsElement =
    document.getElementById("headEvents");

const phoneEventsElement =
    document.getElementById("phoneEvents");

const alertContainer =
    document.getElementById("alertContainer");

const clearAlerts =
    document.getElementById("clearAlerts");


// ==========================================
// STATISTICS
// ==========================================

let eyeEvents = 0;

let headEvents = 0;

let phoneEvents = 0;

let yawnCount = 0;


// ==========================================
// INITIAL PAGE STATE
// ==========================================

if (videoFeed) {
    videoFeed.style.display = "none";
}

if (cameraMessage) {
    cameraMessage.style.display = "block";
}

if (cameraStatus) {

    cameraStatus.textContent =
        "Camera Offline";

    cameraStatus.style.background =
        "#fee2e2";

    cameraStatus.style.color =
        "#b91c1c";
}

if (drowsinessStatus) {
    drowsinessStatus.textContent =
        "Normal";
}


// Initial driver status

setDriverStatus(
    "safe",
    "STOPPED",
    "Driver monitoring has stopped"
);


// ==========================================
// START DETECTION
// ==========================================

if (startBtn) {

    startBtn.addEventListener(
        "click",
        async function () {

            if (detectionRunning) {
                return;
            }


            startBtn.disabled = true;

            startBtn.textContent =
                "Starting Camera...";


            try {

                // ==========================================
                // START BACKEND CAMERA
                // ==========================================

                const response =
                    await fetch(
                        "/api/start_camera",
                        {
                            method: "POST"
                        }
                    );


                if (!response.ok) {

                    const errorText =
                        await response.text();

                    throw new Error(
                        "Camera start failed: " +
                        errorText
                    );
                }


                const data =
                    await response.json();


                if (!data.success) {

                    throw new Error(
                        data.message ||
                        "Could not start camera"
                    );
                }


                // ==========================================
                // CAMERA STARTED
                // ==========================================

                detectionRunning = true;

                startTime = new Date();


                // ==========================================
                // RESET SESSION VALUES
                // ==========================================

                eyeEvents = 0;

                headEvents = 0;

                phoneEvents = 0;

                yawnCount = 0;

                previousAlerts.clear();

                previousEyeState =
                    "Unknown";

                previousHeadDirection =
                    "Forward";

                previousPhoneDetected =
                    false;


                if (eyeEventsElement)
                    eyeEventsElement.textContent = "0";

                if (headEventsElement)
                    headEventsElement.textContent = "0";

                if (phoneEventsElement)
                    phoneEventsElement.textContent = "0";

                if (yawnCountElement)
                    yawnCountElement.textContent = "0";


                // ==========================================
                // RESET DASHBOARD
                // ==========================================

                if (faceStatus)
                    faceStatus.textContent =
                        "Not Detected";

                if (eyeStatus)
                    eyeStatus.textContent =
                        "Unknown";

                if (drowsinessStatus)
                    drowsinessStatus.textContent =
                        "Normal";

                if (headStatus)
                    headStatus.textContent =
                        "Forward";

                if (phoneStatus)
                    phoneStatus.textContent =
                        "Not Detected";


                // ==========================================
                // RESET RISK SCORE
                // ==========================================

                setRiskScore(0);


                // ==========================================
                // SHOW CAMERA
                // ==========================================

                if (videoFeed) {

                    videoFeed.src =
                        "/video_feed?time=" +
                        Date.now();

                    videoFeed.style.display =
                        "block";
                }


                if (cameraMessage) {

                    cameraMessage.style.display =
                        "none";
                }


                // ==========================================
                // CAMERA STATUS
                // ==========================================

                if (cameraStatus) {

                    cameraStatus.textContent =
                        "Camera Online";

                    cameraStatus.style.background =
                        "#dcfce7";

                    cameraStatus.style.color =
                        "#166534";
                }


                // ==========================================
                // DRIVER STATUS
                // ==========================================

                setDriverStatus(
                    "safe",
                    "MONITORING",
                    "Driver monitoring is active"
                );


                // ==========================================
                // TRIP TIMER
                // ==========================================

                durationTimer =
                    setInterval(
                        updateTripDuration,
                        1000
                    );


                // ==========================================
                // DRIVER STATUS TIMER
                // ==========================================

                statusTimer =
                    setInterval(
                        updateDriverStatus,
                        500
                    );


                // ==========================================
                // BUTTONS
                // ==========================================

                startBtn.textContent =
                    "▶ Detection Running";

                startBtn.disabled =
                    true;

                if (stopBtn)
                    stopBtn.disabled = false;


                console.log(
                    "Camera started successfully."
                );

            }


            catch (error) {

                console.error(
                    "Camera start error:",
                    error
                );


                alert(
                    "Unable to start the camera.\n\n" +
                    error.message
                );


                detectionRunning =
                    false;

                startBtn.disabled =
                    false;

                startBtn.textContent =
                    "▶ Start Detection";
            }

        }
    );

}


// ==========================================
// STOP DETECTION
// ==========================================

if (stopBtn) {

    stopBtn.addEventListener(
        "click",
        async function () {

            if (!detectionRunning) {
                return;
            }


            detectionRunning =
                false;


            clearInterval(
                durationTimer
            );

            clearInterval(
                statusTimer
            );


            durationTimer = null;

            statusTimer = null;


            try {

                // ==========================================
                // STOP BACKEND CAMERA
                // ==========================================

                const response =
                    await fetch(
                        "/api/stop_camera",
                        {
                            method: "POST"
                        }
                    );


                if (!response.ok) {

                    console.error(
                        "Backend camera stop failed."
                    );
                }


                // ==========================================
                // STOP VIDEO
                // ==========================================

                if (videoFeed) {

                    videoFeed.src = "";

                    videoFeed.style.display =
                        "none";
                }


                if (cameraMessage) {

                    cameraMessage.style.display =
                        "block";
                }


                // ==========================================
                // CAMERA STATUS
                // ==========================================

                if (cameraStatus) {

                    cameraStatus.textContent =
                        "Camera Offline";

                    cameraStatus.style.background =
                        "#fee2e2";

                    cameraStatus.style.color =
                        "#b91c1c";
                }


                // ==========================================
                // DRIVER STATUS
                // ==========================================

                setDriverStatus(
                    "safe",
                    "STOPPED",
                    "Driver monitoring has stopped"
                );


                // ==========================================
                // RESET VALUES
                // ==========================================

                if (faceStatus)
                    faceStatus.textContent =
                        "Not Detected";

                if (eyeStatus)
                    eyeStatus.textContent =
                        "Unknown";

                if (drowsinessStatus)
                    drowsinessStatus.textContent =
                        "Normal";

                if (headStatus)
                    headStatus.textContent =
                        "Forward";

                if (phoneStatus)
                    phoneStatus.textContent =
                        "Not Detected";


                setRiskScore(0);


                previousEyeState =
                    "Unknown";

                previousHeadDirection =
                    "Forward";

                previousPhoneDetected =
                    false;


                console.log(
                    "Camera stopped."
                );

            }


            catch (error) {

                console.error(
                    "Camera stop error:",
                    error
                );

            }


            finally {

                startBtn.disabled =
                    false;

                startBtn.textContent =
                    "▶ Start Detection";

                stopBtn.disabled =
                    false;
            }

        }
    );

}


// ==========================================
// DRIVER STATUS
// ==========================================

function setDriverStatus(
    type,
    title,
    message
) {

    if (!driverStatus) {
        return;
    }


    driverStatus.classList.remove(
        "safe",
        "warning",
        "critical"
    );


    driverStatus.classList.add(
        type
    );


    if (statusText) {

        statusText.textContent =
            title;
    }


    if (statusMessage) {

        statusMessage.textContent =
            message;
    }

}


// ==========================================
// SET RISK SCORE
// ==========================================

function setRiskScore(score) {

    score =
        Number(score) || 0;


    score =
        Math.max(
            0,
            Math.min(
                100,
                Math.round(score)
            )
        );


    if (riskScore) {

        riskScore.textContent =
            score;
    }


    if (riskProgress) {

        riskProgress.style.width =
            score + "%";
    }


    // ==========================================
    // SAFE
    // 0 - 30
    // ==========================================

    if (score <= 30) {

        if (riskProgress) {

            riskProgress.style.background =
                "#22c55e";
        }


        if (riskScore) {

            riskScore.style.color =
                "#16a34a";
        }


        setDriverStatus(
            "safe",
            "SAFE",
            "Driver condition is normal"
        );
    }


    // ==========================================
    // WARNING
    // 31 - 60
    // ==========================================

    else if (score <= 60) {

        if (riskProgress) {

            riskProgress.style.background =
                "#f59e0b";
        }


        if (riskScore) {

            riskScore.style.color =
                "#d97706";
        }


        setDriverStatus(
            "warning",
            "WARNING",
            "Driver attention required"
        );
    }


    // ==========================================
    // CRITICAL
    // 61 - 100
    // ==========================================

    else {

        if (riskProgress) {

            riskProgress.style.background =
                "#ef4444";
        }


        if (riskScore) {

            riskScore.style.color =
                "#dc2626";
        }


        setDriverStatus(
            "critical",
            "CRITICAL",
            "Immediate driver attention required"
        );
    }

}


// ==========================================
// CALCULATE RISK SCORE
// ==========================================

function calculateRiskScore(data) {

    let score = 0;


    // ==========================================
    // FACE
    // ==========================================

    if (!data.face_detected) {

        score += 20;
    }


    // ==========================================
    // EYES CLOSED
    // ==========================================

    const eyeState =
        String(
            data.eye_state || ""
        ).toLowerCase();


    if (
        eyeState === "closed" ||
        eyeState === "eyes closed"
    ) {

        score += 25;
    }


    // ==========================================
    // DROWSINESS
    // ==========================================

    if (data.drowsy === true) {

        score += 40;
    }


    // ==========================================
    // HEAD DIRECTION
    // ==========================================

    const headDirection =
        String(
            data.head_direction || "Forward"
        ).toLowerCase();


    if (
        headDirection.includes("left") ||
        headDirection.includes("right")
    ) {

        // Looking away from road is a
        // significant driving risk.

        score += 35;
    }


    // ==========================================
    // MOBILE PHONE
    // ==========================================

    if (data.phone_detected === true) {

        score += 50;
    }


    // ==========================================
    // YAWNING
    // ==========================================

    const yawns =
        Number(
            data.yawn_count || 0
        );


    if (yawns >= 1) {

        score += 10;
    }


    // ==========================================
    // EXTRA YAWNING RISK
    // ==========================================

    if (yawns >= 3) {

        score += 10;
    }


    // ==========================================
    // LIMIT SCORE
    // ==========================================

    score =
        Math.min(
            100,
            score
        );


    return score;
}


// ==========================================
// ADD ALERT
// ==========================================

function addAlert(message) {

    if (!alertContainer) {
        return;
    }


    const noAlert =
        alertContainer.querySelector(
            ".no-alert"
        );


    if (noAlert) {

        noAlert.remove();
    }


    let severity =
        "warning";

    let icon =
        "⚠️";


    const lowerMessage =
        message.toLowerCase();


    // ==========================================
    // CRITICAL
    // ==========================================

    if (
        lowerMessage.includes(
            "mobile phone"
        )
        ||
        lowerMessage.includes(
            "drowsiness"
        )
    ) {

        severity =
            "critical";

        icon =
            "🚨";
    }


    // ==========================================
    // HIGH RISK
    // ==========================================

    else if (
        lowerMessage.includes(
            "looking left"
        )
        ||
        lowerMessage.includes(
            "looking right"
        )
    ) {

        severity =
            "high";

        icon =
            "⚠️";
    }


    // ==========================================
    // FACE
    // ==========================================

    else if (
        lowerMessage.includes(
            "face not detected"
        )
    ) {

        severity =
            "warning";

        icon =
            "👤";
    }


    // ==========================================
    // YAWNING
    // ==========================================

    else if (
        lowerMessage.includes(
            "yawning"
        )
    ) {

        severity =
            "warning";

        icon =
            "🥱";
    }


    // ==========================================
    // CREATE ALERT
    // ==========================================

    const alertElement =
        document.createElement(
            "div"
        );


    alertElement.className =
        "alert alert-" +
        severity;


    const time =
        new Date().toLocaleTimeString();


    alertElement.innerHTML = `

        <span class="alert-icon">
            ${icon}
        </span>

        <span class="alert-time">
            ${time}
        </span>

        <span class="alert-message">
            ${message}
        </span>

    `;


    alertContainer.prepend(
        alertElement
    );


    // ==========================================
    // KEEP ONLY 10 ALERTS
    // ==========================================

    const alerts =
        alertContainer.querySelectorAll(
            ".alert"
        );


    if (alerts.length > 10) {

        alerts[
            alerts.length - 1
        ].remove();
    }

}


// ==========================================
// CLEAR ALERTS
// ==========================================

if (clearAlerts) {

    clearAlerts.addEventListener(
        "click",
        function () {

            alertContainer.innerHTML = `

                <div class="no-alert">
                    No alerts detected
                </div>

            `;


            previousAlerts.clear();

        }
    );

}


// ==========================================
// TRIP TIMER
// ==========================================

function updateTripDuration() {

    if (!startTime) {
        return;
    }


    const now =
        new Date();


    const difference =
        Math.floor(
            (now - startTime) / 1000
        );


    const hours =
        Math.floor(
            difference / 3600
        );


    const minutes =
        Math.floor(
            (difference % 3600) / 60
        );


    const seconds =
        difference % 60;


    if (tripDuration) {

        tripDuration.textContent =

            String(hours)
                .padStart(2, "0")

            + ":" +

            String(minutes)
                .padStart(2, "0")

            + ":" +

            String(seconds)
                .padStart(2, "0");
    }

}


// ==========================================
// GET DRIVER STATUS
// ==========================================

async function updateDriverStatus() {

    if (!detectionRunning) {
        return;
    }


    try {

        // ==========================================
        // GET BACKEND STATUS
        // ==========================================

        const response =
            await fetch(
                "/api/driver_status"
            );


        if (!response.ok) {

            throw new Error(
                "Could not get driver status"
            );
        }


        const data =
            await response.json();


        // ==========================================
        // FACE
        // ==========================================

        if (faceStatus) {

            faceStatus.textContent =
                data.face_detected
                    ? "Detected"
                    : "Not Detected";
        }


        // ==========================================
        // EYES
        // ==========================================

        if (eyeStatus) {

            eyeStatus.textContent =
                data.eye_state ||
                "Unknown";
        }


        // ==========================================
        // DROWSINESS
        // ==========================================

        if (drowsinessStatus) {

            if (data.drowsy) {

                drowsinessStatus.textContent =
                    "DROWSY";
            }

            else {

                drowsinessStatus.textContent =
                    "Normal";
            }
        }


        // ==========================================
        // YAWN COUNT
        // ==========================================

        if (
            data.yawn_count !== undefined
            &&
            yawnCountElement
        ) {

            yawnCountElement.textContent =
                data.yawn_count;
        }


        // ==========================================
        // HEAD POSITION
        // ==========================================

        const currentHeadDirection =
            data.head_direction ||
            "Forward";


        if (headStatus) {

            headStatus.textContent =
                currentHeadDirection;
        }


        // ==========================================
        // PHONE
        // ==========================================

        if (phoneStatus) {

            phoneStatus.textContent =
                data.phone_detected
                    ? "Detected"
                    : "Not Detected";
        }


        // ==========================================
        // CALCULATE RISK
        // ==========================================

        const calculatedRisk =
            calculateRiskScore(data);


        console.log(
            "Driver data:",
            data
        );

        console.log(
            "Calculated risk:",
            calculatedRisk
        );


        setRiskScore(
            calculatedRisk
        );


        // ==========================================
        // EYE EVENTS
        // ==========================================

        if (

            previousEyeState !==
            "Closed"

            &&

            data.eye_state ===
            "Closed"

        ) {

            eyeEvents++;


            if (eyeEventsElement) {

                eyeEventsElement.textContent =
                    eyeEvents;
            }
        }


        // ==========================================
        // HEAD EVENTS
        // ==========================================

        if (

            previousHeadDirection ===
            "Forward"

            &&

            currentHeadDirection !==
            "Forward"

            &&

            currentHeadDirection !==
            "Unknown"

        ) {

            headEvents++;


            if (headEventsElement) {

                headEventsElement.textContent =
                    headEvents;
            }
        }


        // ==========================================
        // PHONE EVENTS
        // ==========================================

        if (

            !previousPhoneDetected

            &&

            data.phone_detected

        ) {

            phoneEvents++;


            if (phoneEventsElement) {

                phoneEventsElement.textContent =
                    phoneEvents;
            }
        }


        // ==========================================
        // SAVE PREVIOUS VALUES
        // ==========================================

        previousEyeState =
            data.eye_state ||
            "Unknown";


        previousHeadDirection =
            currentHeadDirection;


        previousPhoneDetected =
            data.phone_detected ||
            false;


        // ==========================================
        // ALERTS
        // ==========================================

        if (data.alerts) {

            data.alerts.forEach(
                function (alert) {

                    if (
                        !previousAlerts.has(
                            alert
                        )
                    ) {

                        addAlert(
                            alert
                        );
                    }

                }
            );


            previousAlerts =
                new Set(
                    data.alerts
                );
        }

    }


    catch (error) {

        console.error(
            "Driver status error:",
            error
        );
    }

}