from driver_monitor import DriverMonitor


monitor = DriverMonitor()


# -----------------------------------------
# Test 1: Normal driver
# -----------------------------------------

result = monitor.analyze(

    drowsiness_result="DRIVER NORMAL",

    yawn_result="NORMAL",

    head_result={
        "direction": "Forward"
    },

    phone_result={
        "phone_detected": False
    },

    face_detected=True
)

print("\nTEST 1")
print(result)


# -----------------------------------------
# Test 2: Drowsiness
# -----------------------------------------

result = monitor.analyze(

    drowsiness_result="DROWSINESS DETECTED",

    yawn_result="NORMAL",

    head_result={
        "direction": "Forward"
    },

    phone_result={
        "phone_detected": False
    },

    face_detected=True
)

print("\nTEST 2")
print(result)


# -----------------------------------------
# Test 3: Phone + head turn
# -----------------------------------------

result = monitor.analyze(

    drowsiness_result="DRIVER NORMAL",

    yawn_result="NORMAL",

    head_result={
        "direction": "Looking Right"
    },

    phone_result={
        "phone_detected": True
    },

    face_detected=True
)

print("\nTEST 3")
print(result)