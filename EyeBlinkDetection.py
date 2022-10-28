from datetime import datetime
from enum import Flag
from time import time
import cv2
import vlc
import time
from pygame import mixer



# Using 2 Cascades for face and eyes
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml")

first_read = True

cap = cv2.VideoCapture(0)
ret, image = cap.read()
first_datetime = datetime.now()

# Function required for sound alarm (VLC)
def sound():
    x = vlc.MediaPlayer("C:/Users/Faruk/Desktop/TezSon/alarm11.mp3")
    x.play()
    
    

while ret:
    first_read = False
    # Loop for camera
    ret, image = cap.read()
    # Convert image to gray
    gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Gri renk uzayı
    # Filter for details
    gray_scale = cv2.bilateralFilter(gray_scale, 5, 1, 1)
    # Using cascade for face and eyes
    faces = face_cascade.detectMultiScale(gray_scale, 1.3, 5, minSize=(200, 200)) 
    if len(faces) > 0: # Detect eyes if face 
        for (x, y, w, h) in faces:
            image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            eye_face = gray_scale[y:y + h, x:x + w]
            eye_face_clr = image[y:y + h, x:x + w]
            # Examine Eyes
            eyes = eyes_cascade.detectMultiScale(eye_face, 1.3, 5, minSize=(50, 50))
            if len(eyes) >= 2:
                if first_read:
                    cv2.putText(image, "Eyes Are Detected", (70, 70), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 255, 0), 2)
                else:
                    cv2.putText(image, "Eyes Not Found", (70, 70), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (255, 255, 255), 2)

                    first_datetime = datetime.now()
                    

                    

                   
            else:
                if first_read:
                    cv2.putText(image, "Eye not found", (70, 70), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (255, 255, 255), 2)
                else:
                    cv2.putText(image, "Blink Detected", (70, 70), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 255, 0), 2)
                    cv2.imshow('image',image)
                    # Counter identification after blink detection
                    second_datetime = datetime.now()

                    time = (second_datetime - first_datetime).seconds
                    print(time)

                    cv2.waitKey(1)
                    print("Blink Detected.....")
                    # Warning after 3 blink detections using counter
                    if time >= 3:
                        cv2.putText(image, "WARNING..SLEEP", (100, 100), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 0, 0), 2)
                        sound()
                        first_datetime = datetime.now()
                        
                   



    else:
        cv2.putText(image, "Face Not Detected.", (70, 70), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2)
    cv2.imshow('image', image)
    a = cv2.waitKey(1)
    
    # Closing camera and window with "q"
    if a == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
