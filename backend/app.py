import os
import sys

from flask import Flask, send_from_directory, Response, jsonify


# ==========================================
# PROJECT ROOT
# ==========================================

project_root = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, project_root)


# ==========================================
# IMPORT CAMERA
# ==========================================

from backend.camera import Camera


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)


# ==========================================
# CAMERA
# ==========================================

camera = Camera()


# ==========================================
# MAIN WEBPAGE
# ==========================================

@app.route("/")
def home():

    return send_from_directory(
        os.path.join(project_root, "frontend"),
        "index.html"
    )


# ==========================================
# FRONTEND FILES
# ==========================================

@app.route("/<path:filename>")
def frontend_files(filename):

    return send_from_directory(
        os.path.join(project_root, "frontend"),
        filename
    )


# ==========================================
# START CAMERA
# ==========================================

@app.route("/api/start_camera", methods=["POST"])
def start_camera():

    print("\n========================================")
    print("START CAMERA API CALLED")
    print("========================================")

    try:

        print("Calling camera.start()...")

        success = camera.start()

        print(
            "camera.start() returned:",
            success
        )

        if success:

            print(
                "Camera started successfully."
            )

            return jsonify({
                "success": True,
                "message": "Camera started successfully"
            })

        else:

            print(
                "Camera could NOT be opened."
            )

            return jsonify({
                "success": False,
                "message": "Could not open webcam"
            }), 500

    except Exception as e:

        print(
            "ERROR while starting camera:"
        )

        print(
            repr(e)
        )

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ==========================================
# STOP CAMERA
# ==========================================

@app.route("/api/stop_camera", methods=["POST"])
def stop_camera():

    print("\n========================================")
    print("STOP CAMERA API CALLED")
    print("========================================")

    try:

        camera.stop()

        print(
            "Camera stopped successfully."
        )

        return jsonify({
            "success": True,
            "message": "Camera stopped successfully"
        })

    except Exception as e:

        print(
            "Camera stop error:",
            repr(e)
        )

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ==========================================
# VIDEO STREAM
# ==========================================

@app.route("/video_feed")
def video_feed():

    def generate_frames():

        while camera.is_running():

            frame = camera.get_frame()

            if frame is None:

                break

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame
                + b"\r\n"
            )

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# ==========================================
# DRIVER STATUS API
# ==========================================

@app.route("/api/driver_status")
def driver_status():

    return jsonify(
        camera.get_status()
    )


# ==========================================
# FACE STATUS API
# ==========================================

@app.route("/api/face_status")
def face_status():

    return jsonify({
        "face_detected":
            camera.is_face_detected()
    })


# ==========================================
# CAMERA STATUS API
# ==========================================

@app.route("/api/camera_status")
def camera_status():

    return jsonify({
        "running":
            camera.is_running()
    })


# ==========================================
# BASIC STATUS API
# ==========================================

@app.route("/api/status")
def status():

    return jsonify({
        "status": "success",
        "message":
            "DriveGuardian AI backend is running"
    })


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("DriveGuardian AI")
    print("Flask server starting...")
    print("=" * 50)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True
    )