import cv2
import streamlit as st
from datetime import datetime
import time

# Title displayed at the top of the Streamlit app
st.title('Timed Camera')

# --- REQUIRED: persist camera state across reruns ---
if "camera_on" not in st.session_state:
    st.session_state.camera_on = False

# Button the user clicks to start the webcam
col1, col2 = st.columns(2)
with col1:
    if st.button('Start Camera'):
        st.session_state.camera_on = True
with col2:
    if st.button('Close Camera'):
        st.session_state.camera_on = False


# Only run the camera loop after the button is pressed
if st.session_state.camera_on:
    # Placeholder in Streamlit where video frames will be continuously updated
    streamlit_image = st.image([])

    # Connect to the default webcam (0 = built-in camera)
    camera = cv2.VideoCapture(0)

    # Continuous loop to read and display frames from the camera
    while st.session_state.camera_on:
        # Read a single frame from the webcam
        check, frame = camera.read()
        if not check:
            break

        # Convert from OpenCV’s default BGR color format to RGB for Streamlit
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get the current date in readable format
        current_date = datetime.now().strftime("%A, %B %-d, %Y")

        # Get the current time in 12-hour format with AM/PM
        current_time = datetime.now().strftime("%I:%M:%S %p")

        # Draw the date text onto the video frame
        cv2.putText(
            img=frame,
            text=current_date,
            org=(50, 50),  # position (x, y)
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=3,
            color=(255, 255, 255),
            thickness=2,
            lineType=cv2.LINE_AA
        )

        # Draw the time text slightly below the date
        cv2.putText(
            img=frame,
            text=current_time,
            org=(50, 95),
            fontFace=cv2.FONT_HERSHEY_PLAIN,
            fontScale=2.5,
            color=(20, 200, 200),
            thickness=2,
            lineType=cv2.LINE_AA
        )

        # Push the updated frame to the Streamlit app
        streamlit_image.image(frame)

        # --- Small delay to reduce CPU usage and smooth the app ---
        time.sleep(0.03)

    # Release camera when stopped
    camera.release()