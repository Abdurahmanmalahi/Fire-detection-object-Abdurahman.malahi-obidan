
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
