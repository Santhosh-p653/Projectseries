import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os

def analyze_uploaded_image(image_path):
    # 1. Load the selected image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not read the image file.")
        return

    output_image = image.copy()
    
    # 2. Preprocessing: Grayscale and blur to smooth out edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    
    # Adaptive thresholding to smoothly separate shapes from background
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # 3. Find outlines (contours)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    detected_count = 0
    print("\n--- Analyzing Image Objects ---")

    for cnt in contours:
        # Ignore tiny background noise fragments
        if cv2.contourArea(cnt) < 600:
            continue
            
        detected_count += 1

        # --- CALCULATE CENTER COORD (CENTROID) ---
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            # Fallback to a contour coordinate if division by zero occurs
            cX, cY = cnt[0][0][0], cnt[0][0][1]

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
            # Differentiate between regular squares and other 4-sided shapes (rectangles/trapezoids)
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

        # --- COLOR DETECTION (CENTER PIXEL METHOD) ---
        # Convert full image to HSV space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Pull the exact HSV values from the dead center pixel of the shape
        pixel_hsv = hsv[cY, cX]
        hue = pixel_hsv[0]
        sat = pixel_hsv[1]
        val = pixel_hsv[2]

        # Apply digital color threshold rules
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

        # --- DRAW LABELS AND ANNOTATIONS ---
        # Draw the tracking outline around the shape
        cv2.drawContours(output_image, [cnt], -1, (0, 255, 0), 2)
        
        # Place a dot directly on the sampled center pixel
        cv2.circle(output_image, (cX, cY), 3, (255, 255, 255), -1)
        
        # Overlay the final designation text
        label = f"{color} {shape}"
        cv2.putText(output_image, label, (cX - 45, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        print(f"Object {detected_count}: Detected a {label} [H:{int(hue)} S:{int(sat)} V:{int(val)}]")

    print(f"\nTotal objects identified: {detected_count}")
    
    # 4. Display the resulting processing window
    cv2.imshow("Identification Result", output_image)
    print("\n[!] Press ANY key while looking at the image window to close it.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Suppress empty tkinter pop-up window background frame
    root = tk.Tk()
    root.withdraw()

    print("Opening file explorer... Please select your 'shapes.png' image.")
    
    file_path = filedialog.askopenfilename(
        title="Select an Image for Shape & Color Analysis",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp")]
    )

    if file_path:
        print(f"Selected file: {file_path}")
        analyze_uploaded_image(file_path)
    else:
        print("No file was selected. Exiting.") 