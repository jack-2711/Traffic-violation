from ultralytics import YOLO
import cv2
import pandas as pd
import os, time

# ----------------------------
# Setup
# ----------------------------
MODEL_PATH = "runs/detect/train5/weights/best.pt"
VIOLATION_DIR = "violations"
LOG_FILE = "logs/violations.csv"

os.makedirs(VIOLATION_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Initialize YOLOv8 model
model = YOLO(MODEL_PATH)

# Initialize CSV log
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=["Time", "Violation Type", "Frame No", "Image Path"]).to_csv(LOG_FILE, index=False)

# ----------------------------
# Helper function to log violations
# ----------------------------
def log_violation(violation_type, frame_no, frame):
    timestamp = time.strftime("%H:%M:%S")
    img_path = os.path.join(VIOLATION_DIR, f"{violation_type}_{int(time.time())}.jpg")
    cv2.imwrite(img_path, frame)

    log_entry = pd.DataFrame([[timestamp, violation_type, frame_no, img_path]],
                             columns=["Time", "Violation Type", "Frame No", "Image Path"])
    log_entry.to_csv(LOG_FILE, mode='a', header=False, index=False)
    print(f"🚨 {violation_type} at {timestamp}, saved {img_path}")

# ----------------------------
# Detection logic
# ----------------------------
def detect_violations(video_source=0):
    cap = cv2.VideoCapture(video_source)
    frame_no = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_no += 1

        results = model(frame, verbose=False)
        detections = results[0].boxes
        labels = [model.names[int(cls)] for cls in detections.cls]

        # ---- Violation Rules ----
        violation_detected = False

        if "helmet" not in labels:
            cv2.putText(frame, "Helmet Violation!", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            log_violation("Helmet Violation", frame_no, frame)
            violation_detected = True

        if "seatbelt" not in labels:
            cv2.putText(frame, "Seatbelt Violation!", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            log_violation("Seatbelt Violation", frame_no, frame)
            violation_detected = True

        # Draw bounding boxes
        annotated_frame = results[0].plot()

        # Display
        cv2.imshow("Smart Detection", annotated_frame)
        if cv2.waitKey(1) & 0xFF == 27:  # press ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    # Replace 0 with your video path for pre-recorded video
    detect_violations(video_source=0)
