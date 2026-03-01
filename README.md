# Motion Detection Email Alert System

## Overview

This project is a real-time motion detection system built with Python and OpenCV. It monitors a webcam feed, detects significant motion, captures evidence images, and automatically sends an email alert with the captured image attached.

The system is designed to demonstrate practical computer vision, automation, and background task handling using threads.

---

## Features

- Real-time webcam monitoring  
- Motion detection using frame differencing  
- Automatic image capture when motion is detected  
- Email alert with image attachment  
- Background threading for non-blocking email sending  
- Automatic cleanup of stored images  
- Secure credential handling via `.env`  

---

## How It Works

### 1. Camera Initialization

The system opens the default webcam using OpenCV and captures frames continuously.

The very first frame is stored as the **baseline background** for motion comparison.

---

### 2. Motion Detection Pipeline

Each new frame goes through the following steps:

- Convert to grayscale  
- Apply Gaussian blur to reduce noise  
- Compute difference from the baseline frame  
- Apply thresholding to isolate motion  
- Dilate the image to strengthen motion regions  
- Find contours representing moving objects  

Small contours are ignored to reduce false positives.

---

### 3. Motion Trigger Logic

When a large enough contour is detected:

- A green rectangle is drawn around the object  
- The frame is saved to the `images/` folder  
- The system tracks motion state transitions  

An email is triggered **only when motion stops** (transition from `[1, 0]`).  
This prevents excessive email spam during continuous movement.

---

### 4. Email Notification

When motion ends:

- The middle image from the capture burst is selected  
- An email is sent with the image attached  
- Email sending runs in a background thread  
- The images folder is cleaned afterward  

---

## Project Structure

```
project/
│
├── main.py              # Motion detection loop
├── emailing.py          # Email sending logic
├── images/              # Temporary captured frames
├── .env                 # Environment variables (not committed)
├── requirements.txt
└── README.md
```

---

## Environment Variables

Create a `.env` file in the project root:

```
GMAIL_APP_PASSWORD=your_app_password_here
```

### Important

- This must be a **Gmail App Password**, not your regular password  
- Requires 2-Factor Authentication enabled on the Google account  

---

## Installation

### 1. Clone the repository

```
git clone <your-repo-url>
cd <your-repo>
```

### 2. Create virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## Required Packages

Core dependencies:

- opencv-python  
- python-dotenv  
- filetype  

Example `requirements.txt`:

```
opencv-python
python-dotenv
filetype
```

---

## Usage

Run the motion detector:

```
python main.py
```

### Controls

- Webcam window will open  
- Press **q** to quit  

---

## Email Behavior

An email is sent when:

- Motion is detected  
- Motion then stops  

This design avoids sending dozens of emails during continuous movement.
