
# Object Detection with Alarm and Email Notification

## Description
This project is designed to detect objects, specifically faces, using OpenCV in real-time through the computer’s webcam. When a face is detected, an alarm sound is played, and an email notification is sent to a designated recipient. The project employs Haar Cascade Classifier for face detection and threading to handle the alarm and email functions concurrently without interrupting the video feed.

## Features
- **Real-time Object Detection**: Detects faces in real-time using your device’s camera.
- **Alarm Sound**: Plays an alarm sound when a face is detected.
- **Email Notification**: Sends an alert email when a face is detected.
- **Multithreading**: Uses threading to handle the alarm sound and email notification without affecting object detection.

## Prerequisites

Before running the project, ensure you have the following installed:

- **Python 3.x**
- Required Python libraries:
  - OpenCV (`cv2`)
  - Playsound (`playsound`)
  - Smtplib (included in Python)
  - Threading (included in Python)

### Installation

To install the required Python libraries, use:

```bash
pip install opencv-python
pip install playsound
```

## Files Needed

- **`haarcascade_frontalface_default.xml`**: This is the Haar Cascade file used to detect faces. You can download it from [here](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml).
- **Alarm Sound File**: A `.mp3` file for the alarm sound. The example in the code uses `police-operation-siren-144229.mp3`. Place this file in the same directory as your Python script.

## How to Use

### 1. Download Haar Cascade File

Download the `haarcascade_frontalface_default.xml` file from [here](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml) and place it in the same directory as your Python script.

### 2. Set Up the Alarm Sound

Place an `.mp3` file (e.g., `police-operation-siren-144229.mp3`) in the same directory as the Python script.

### 3. Modify Email Information

In the script, update the email credentials and the recipient's email address as shown below:

```python
server.login("YOUR_EMAIL@gmail.com", 'YOUR_PASSWORD')  # Use your email and app password
recipientmail = "RECIPIENT_EMAIL@gmail.com"  # Update with recipient's email
```

> **Important**: If you're using Gmail, ensure that you enable "Less Secure Apps" or generate an [App Password](https://support.google.com/accounts/answer/185833) for sending emails.

### 4. Run the Program

To run the program, use the command:

```bash
python your_script_name.py
```

### 5. Quit the Program

Press the `q` key to stop the video feed and quit the program.

## Code Explanation

Here is a breakdown of the main parts of the code:

1. **Object Detection**: Uses OpenCV’s Haar Cascade Classifier to detect faces in real-time through the webcam. The video stream is captured, converted to grayscale, and processed for object (face) detection.

2. **Alarm Trigger**: When a face is detected, an alarm sound is played using the `playsound` library. This is done on a separate thread to ensure the detection process isn't blocked.

3. **Email Notification**: When a face is detected, an email is sent to a specified recipient via `smtplib`. This also runs in a separate thread to prevent delays in the detection process.

4. **Multithreading**: The project uses threads to run both the alarm and the email functions simultaneously without interrupting the video processing.

### Full Code

```python
import cv2  # Library for OpenCV
import threading  # Library for threading
import playsound  # Library for alarm sound
import smtplib  # Library for email sending

# Load the Haar Cascade file for face detection
object_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Start the camera (0 for built-in, 1 for USB attached camera)
vid = cv2.VideoCapture(0)
runOnce = False  # To ensure the alarm and email are only triggered once

# Function to play the alarm sound using threading
def play_alarm_sound_function():
    # Play the alarm sound (MP3 file provided)
    playsound.playsound('police-operation-siren-144229.mp3')
    print("Object detection alarm end")  # Print when alarm ends

# Function to send email upon object detection using threading
def send_mail_function():
    recipientmail = "joneadoed9@gmail.com"  # Recipient's email
    recipientmail = recipientmail.lower()  # Ensure lowercase email

    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use the correct SMTP server and port
        server.ehlo()
        server.starttls()

        # Login with sender's email ID and password
        server.login("abdulmlikobidan200@gmail.com", 'yemennet')  # Sender's email credentials

        # Send email with subject and message
        server.sendmail('abdulmlikobidan200@gmail.com', recipientmail, "Warning: Object detected!")
        
        # Print confirmation message in console
        print(f"Alert mail sent successfully to {recipientmail}")

        # Close the SMTP server
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Main loop for capturing video and detecting objects
while True:
    ret, frame = vid.read()  # Capture video frame-by-frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale
    objects = object_cascade.detectMultiScale(gray, 1.1, 4)  # Detect faces in the frame

    for (x, y, w, h) in objects:
        # Draw rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # If the object is detected and the alarm hasn't been triggered yet
        if not runOnce:
            # Trigger alarm and email using threads
            threading.Thread(target=play_alarm_sound_function).start()
            threading.Thread(target=send_mail_function).start()
            runOnce = True  # Ensure this only happens once

    # Display the video with the detection box
    cv2.imshow('Object Detection', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all OpenCV windows
vid.release()
cv2.destroyAllWindows()
```

## Notes
- Ensure that your camera is working correctly before running the code. You can switch to an external camera by changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` if necessary.
- Ensure you have the required `.xml` and `.mp3` files in the correct directory.
- If you're using Gmail, consider using [app-specific passwords](https://support.google.com/accounts/answer/185833) for security reasons.

## License
This project is licensed under the MIT License.
