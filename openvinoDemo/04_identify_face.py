import face_recognition
import cv2
import numpy as np
from imutils.video import FPS
from os import listdir
from os.path import isfile, join, splitext

FACES_FOLDER = "./faces/"

video_capture = cv2.VideoCapture(0) # webcam 0
scale_frame = True

set_path = FACES_FOLDER
test_set = [f for f in listdir(set_path) if isfile(join(set_path, f))]

print(test_set)

known_face_encodings = []
known_face_names = []
i = 0
for f in test_set:
    image = face_recognition.load_image_file(FACES_FOLDER + "//" + f)
    image_encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(image_encoding)
    known_face_names.append(splitext(f)[0])
    i = i + 1

print (known_face_names)

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

fps = FPS().start()
while True:
    ret, frame = video_capture.read() # get a frame
    if (scale_frame == True):
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5) # resize frame 1/4 size
        rgb_frame = small_frame[:, :, ::-1] # BGR to RGB
    else:
        rgb_frame = frame[:, :, ::-1] # BGR to RGB

    if process_this_frame:
        # Find all the faces
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if (scale_frame == True):
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 1)
        #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 255, 0), 1)
        
    fps.update()
    cv2.imshow('Video - Press Q to exit', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
fps.stop()
print("approx FPS: {: .2f}".format(fps.fps()))

video_capture.release()
cv2.destroyAllWindows()

