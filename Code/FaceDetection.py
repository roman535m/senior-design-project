import cv2
import numpy as np
import dlib
import imutils
from imutils import face_utils

class FaceDetection(object):
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        self.fa = face_utils.FaceAligner(self.predictor)
        self.roi = None
        self.frame = None
        self.face_frame = None

    def face_detect(self, frame):
        resized_frame = imutils.resize(frame, height=800)
        self.frame = resized_frame

        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        face = self.detector(gray, 0)

        if len(face) > 0:
            (x, y, w, h) = face_utils.rect_to_bb(face[0])

            self.face_frame = self.frame[y-int((h * 0.6)):y+int((h * 1.2)), x-int((w*0.4)):x+w+int((w*0.4))]

            self.face_frame = imutils.resize(self.face_frame, height=500)

            grayf = cv2.cvtColor(self.face_frame, cv2.COLOR_BGR2GRAY)
            rectsf = self.detector(grayf, 0)

            if len(rectsf) > 0:
                shape = self.predictor(grayf, rectsf[0])

                # Convert it to the NumPy Array
                shape_np = np.zeros((68, 2), dtype=np.uint64)
                shape_np[19] = (shape.part(20).x, shape.part(20).y - (shape.part(20).y // 8))
                shape_np[24] = (shape.part(24).x, shape.part(24).y - (shape.part(24).y // 8))
                shape_np[37] = (shape.part(20).x, shape.part(20).y - (shape.part(20).y // 8) + (shape.part(27).y - shape.part(28).y) // 2)
                shape_np[44] = (shape.part(24).x, shape.part(24).y - (shape.part(24).y // 8) + (shape.part(27).y - shape.part(28).y) // 2)

                # Display the landmarks
                for i, (x, y) in enumerate(shape_np):
                    # Draw the circle to mark the keypoint
                    cv2.circle(self.face_frame, (x, y), 3, (0, 255, 0), -1)
                    # draw box for ROI
                    cv2.line(self.face_frame, shape_np[19], shape_np[24], (0, 255, 0), 1)
                    cv2.line(self.face_frame, shape_np[24], shape_np[44], (0, 255, 0), 1)
                    cv2.line(self.face_frame, shape_np[44], shape_np[37], (0, 255, 0), 1)
                    cv2.line(self.face_frame, shape_np[37], shape_np[19], (0, 255, 0), 1)
                self.roi = self.face_frame[shape_np[37][1]:shape_np[37][1] + shape_np[19][1] - shape_np[37][1],
                                           shape_np[37][0]:shape_np[37][0] + shape_np[44][0] - shape_np[37][0]]

            #cv2.imshow('Face Frame', self.face_frame)

            return self.face_frame, self.roi
