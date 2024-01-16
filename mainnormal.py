import cv2 as cv
import face_recognition
import glob
import os
import datetime

cap = cv.VideoCapture(0)
face_model = cv.CascadeClassifier('model_face.xml')

known_images = []
known_face_encodings = []

image_files = glob.glob(r"C:\Users\Draft\Downloads\image ddetection\knownfaces\*.jpg")

for file in image_files:
    known_image = face_recognition.load_image_file(file)
    known_face_encoding = face_recognition.face_encodings(known_image)[0]
    known_images.append(known_image)
    known_face_encodings.append(known_face_encoding)

if not cap.isOpened():
    print("Unable to open the camera")
    exit()

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_model.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        face_image = frame[y:y+h, x:x+w]
        face_image_bgr = cv.cvtColor(face_image, cv.COLOR_BGR2RGB)
        face_encoding = face_recognition.face_encodings(face_image_bgr)
        
        if len(face_encoding) > 0:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding[0])
            
            if True in matches:
                matched_index = matches.index(True)
                known_image_file = os.path.basename(image_files[matched_index])
                
                cv.putText(frame, known_image_file[:-4], (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    
    cv.imshow('Camera', frame)
    
    if cv.waitKey(1) == ord('e'):
        break

cap.release()
cv.destroyAllWindows()
