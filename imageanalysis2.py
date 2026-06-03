import cv2
import numpy as np
import time  # Imported to manage logging cooldowns

def analyze_realtime_with_logs():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Dictionary to keep track of when a specific label was last logged
    # Structure: {"Color Shape": timestamp}
    logged_objects = {}
    LOG_COOLDOWN = 2.0  # Time in seconds to wait before logging the same object again

    print("--- Starting Real-Time Object Analysis with Logging ---")
    print("[!] Press 'q' on your keyboard to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        output_frame = frame.copy()
        current_time = time.time()  # Get the current timestamp for this frame
        
        # Preprocessing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width, _ = hsv.shape

        for cnt in contours:
            if cv2.contourArea(cnt) < 1000:
                continue

            # --- CENTROID ---
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = cnt[0][0][0], cnt[0][0][1]

            cX = max(0, min(cX, width - 1))
            cY = max(0, min(cY, height - 1))

            # --- SHAPE DETECTION ---
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
            vertices = len(approx)

            shape = "Unknown"
            if vertices == 3:
                shape = "Triangle"
            elif vertices == 4:
                (x, y, w, h) = cv2.boundingRect(approx)
                ar = w / float(h)
                if 0.95 <= ar <= 1.05:
                    shape = "Square"
                else:
                    shape = "Rectangle/Trapezoid"
            elif vertices == 5:
                shape = "Pentagon"
            elif vertices == 6:
                shape = "Hexagon"
            elif vertices == 8:
                shape = "Octagon"
            elif vertices > 6:
                shape = "Circle"

            # --- COLOR DETECTION ---
            pixel_hsv = hsv[cY, cX]
            hue, sat, val = pixel_hsv[0], pixel_hsv[1], pixel_hsv[2]

            if val < 45:
                color = "Black"
            elif sat < 35 and val > 180:
                color = "White"
            elif sat < 35:
                color = "Gray"
            else:
                if (0 <= hue < 12) or (155 <= hue <= 180):
                    color = "Red"
                elif 12 <= hue < 25:
                    color = "Orange"
                elif 25 <= hue < 35:
                    color = "Yellow"
                elif 35 <= hue < 85:
                    color = "Green"
                elif 85 <= hue < 130:
                    color = "Blue"
                elif 130 <= hue < 155:
                    color = "Purple"
                else:
                    color = "Unknown"

            label = f"{color} {shape}"

            # --- SMART LOGGING LOGIC ---
            # If the item is new, or the cooldown period has expired, log it!
            if label not in logged_objects or (current_time - logged_objects[label]) > LOG_COOLDOWN:
                print(f"[LOG] Identified: {label} | HSV: [{int(hue)}, {int(sat)}, {int(val)}]")
                logged_objects[label] = current_time  # Update the last logged time

            # --- DRAW LABELS ---
            cv2.drawContours(output_frame, [cnt], -1, (0, 255, 0), 2)
            cv2.circle(output_frame, (cX, cY), 3, (255, 255, 255), -1)
            cv2.putText(output_frame, label, (cX - 45, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Real-Time Identification & Logging", output_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Camera feed closed.")

if __name__ == "__main__":
    analyze_realtime_with_logs()