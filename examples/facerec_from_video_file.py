import face_recognition
import cv2
from moviepy.editor import *
# This is a demo of running face recognition on a video file and saving the results to a new video file.
#
# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Open the input movie file
input_movie = cv2.VideoCapture("examples/example.mp4")
parent_clip = VideoFileClip('examples/example.mp4', audio=True)
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
# width = input_movie.get(cv2.CAP_PROP_FRAME_WIDTH)
# print(width)
# height = input_movie.get(cv2.CAP_PROP_FRAME_HEIGHT)

# Create an output movie file (make sure resolution/frame rate matches input video!)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
output_movie = cv2.VideoWriter('examples/output2-rose.avi', fourcc, 29.97, (1920, 1080))

# Load some sample pictures and learn how to recognize them.
jisoo_image = face_recognition.load_image_file("examples/jisoo.jpg")
jisoo_face_encoding = face_recognition.face_encodings(jisoo_image)[0]

rose_image = face_recognition.load_image_file("examples/rose.jpg")
rose_face_encoding = face_recognition.face_encodings(rose_image)[0]

known_faces = [
    jisoo_face_encoding,
    rose_face_encoding
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
videoclip=[]
audioclip=[]
frame_number = 0
start_time = 0
finish_time = 0
while True:
    # Grab a single frame of video
    ret, frame = input_movie.read()
    second = input_movie.get(cv2.CAP_PROP_FPS)
    print(length)
    frame_number += 1

    # Quit when the input video file ends
    if not ret:
        print("break")
        break

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    face_names = []
    flag= True
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.43)

        # If you had more than 2 faces, you could make this logic a lot prettier
        # but I kept it simple for the demo
        name = None

        if match[0]:
            flag = True
            print("와 지수다")
            name = "jisu"
        elif match[1]:
            print(" 와 로제다")
            name = "rose"
        else:
            flag = False
            print('아무도 없다')


        face_names.append(name)

    # Label the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            continue

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Write the resulting image to the output video file
    print("Writing frame {} / {}".format(frame_number, length))
    start_time = (frame_number-1) * (1 / second)
    finish_time = start_time + (1/second)
    if flag:
        videoclip.append(
            parent_clip.subclip(start_time, finish_time)
        )
        print('Nice!') 
    else:
        continue

# All done!
final_clip = concatenate_videoclips(videoclip)
final_clip.write_videofile("examples/moviepy.mp4",  codec='libx264', 
                     audio_codec='aac', 
                     temp_audiofile='temp-audio.m4a', 
                     remove_temp=True)

input_movie.release()
cv2.destroyAllWindows()
