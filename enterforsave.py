import cv2
import os
import requests


def detect_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')  # โหลดตัวตรวจจับใบหน้า
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))  # ตรวจจับใบหน้า
    return faces

cap = cv2.VideoCapture(0)

is_capturing = False  

webhook_url = 'https://discord.com/api/webhooks/1111321378357006357/d9obqaQDAbwsM8kJ-LtErptqmc7CKarLBFcZITVSiOVguy3h1bcwmlr7OYPjYU6zTieJ'  # ระบุ URL ของ webhook ที่คุณต้องการส่งข้อมูลไปยัง

while True:
    ret, frame = cap.read()  
    
    faces = detect_faces(frame)  
    

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    cv2.imshow('Face Detection', frame)  
    

    if cv2.waitKey(1) & 0xFF == ord('e'):
        break

    if cv2.waitKey(1) == 13:  
        if not is_capturing:
            name = input('Enter name: ')
            file_name = os.path.join('knownfaces', name + '.jpg')
            
            if not os.path.exists('knownfaces'):
                os.makedirs('knownfaces')
            
            face_image = frame[y:y+h, x:x+w]
            cv2.imwrite(file_name, face_image)
            print('Image saved')

            files = {'image': open(file_name, 'rb')}
            data = {'content': 'ผู้ใช้ตั้งชื่อว่า ' + name}
            response = requests.post(webhook_url, files=files, data=data)
            print('Webhook response:', response.text)

            
            is_capturing = True
    else:
        is_capturing = False

cap.release() 
cv2.destroyAllWindows()
