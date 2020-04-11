from PIL import Image, ImageDraw
import face_recognition
import cv2

webcam = cv2.VideoCapture(0) # webcam 0
check, image = webcam.read()
rgb_image = image[:, :, ::-1] # BGR to RGB

# Find all facial features in all the faces in the image
face_landmarks_list = face_recognition.face_landmarks(rgb_image)

pil_image = Image.fromarray(rgb_image)
d = ImageDraw.Draw(pil_image)
for face_landmarks in face_landmarks_list:
    for facial_feature in face_landmarks.keys():
      d.line(face_landmarks[facial_feature], width=1)

# Show the picture
pil_image.show()

webcam.release()
cv2.destroyAllWindows()

