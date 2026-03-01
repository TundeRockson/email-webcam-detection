import os
import cv2
import time
import glob
from emailing import send_email
from threading import Thread

# Open the default webcam
video = cv2.VideoCapture(0)

# Small warm-up so the camera sensor can adjust
time.sleep(1)

# Baseline frame for motion comparison
first_frame = None

# Tracks recent motion status (used to detect motion stop event)
status_list = []

# Counter for saved images
count = 1


# --- Helper: delete all captured images ---
def clean_folder():
    print("Started cleaning images folder")

    # Get all PNG files in the images folder
    images = glob.glob("images/*.png")

    # Remove each image file
    for image in images:
        os.remove(image)

    print("Finished cleaning images folder")


# --- Main motion detection loop ---
while True:
    status = 0  # 0 = no motion, 1 = motion detected

    # Read frame from webcam
    check, frame = video.read()

    # Convert frame to grayscale (simplifies motion detection)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise and false positives
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # Store the very first frame as the reference background
    if first_frame is None:
        first_frame = gray_frame_gau

    # Compute absolute difference between background and current frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # Threshold the difference to highlight motion areas
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]

    # Dilate to fill in holes and strengthen detected regions
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Show the processed motion mask
    cv2.imshow("My video", dil_frame)

    # Find contours (moving objects) in the mask
    contours, check = cv2.findContours(
        dil_frame,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # --- Inspect detected contours ---
    for contour in contours:
        # Ignore small movements/noise
        if cv2.contourArea(contour) < 50000:
            continue

        # Draw bounding box around detected motion
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            3
        )

        # If a rectangle was drawn, mark motion detected
        if rectangle.any():
            status = 1

            # Save current frame as evidence image
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1

            # Choose the middle image from the capture burst
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    # --- Track motion state transitions ---
    status_list.append(status)

    # Keep only the last two states
    status_list = status_list[-2:]

    # Trigger when motion stops (transition from motion -> no motion)
    if status_list == [1, 0]:
        # Send email in background thread
        email_thread = Thread(target=send_email, args=(image_with_object,))
        email_thread.daemon = True

        # Clean images folder in background
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        email_thread.start()

    # Show the live camera feed with rectangles
    cv2.imshow("My video", frame)

    key = cv2.waitKey(1)

    # Press q to quit
    if key == ord("q"):
        break

# Final cleanup pass
clean_thread.start()

# Release webcam when finished
video.release()

