import os
import cv2

# 1. Define and create the target directory if it doesn't exist
save_path = os.path.join("assets", "images")
if not os.path.exists(save_path):
    os.makedirs(save_path)
    print(f"Created directory: {save_path}")

# 2. Initialize the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open the webcam.")
    exit()

print("\n--- Webcam Control Panel ---")
print("Press 'Space' to capture and save an image.")
print("Press 'ESC' to exit.")
print("----------------------------\n")

img_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    # Show live preview
    cv2.imshow('Webcam Live Preview', frame)

    # Listen for key presses
    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        # ESC pressed
        print("Closing application...")
        break
        
    elif key == 32:
        # SPACE pressed
        img_name = f"opencv_frame_{img_counter}.png"
        
        # Combine the folder path and file name (e.g., assets/images/opencv_frame_0.png)
        full_output_path = os.path.join(save_path, img_name)
        
        # Save the image to the specific folder
        cv2.imwrite(full_output_path, frame)
        print(f"Successfully saved to: {full_output_path}")
        
        img_counter += 1

# 3. Clean up resources
cap.release()
cv2.destroyAllWindows()