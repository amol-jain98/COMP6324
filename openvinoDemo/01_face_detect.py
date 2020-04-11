import face_recognition
import cv2

video_capture = cv2.VideoCapture(0)
while True:
   ret, frame = video_capture.read()
   frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
   face_locations = face_recognition.face_locations(frame)
   for (top, right, bottom, left) in face_locations:
      cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)

   cv2.imshow('Video', frame)
   if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cv2.destroyAllWindows()


