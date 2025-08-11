import cv2
from tkinter import *
from PIL import ImageTk, Image
import time

class Scan:
    def __init__(self, label):
        self.result = ""
        self.label = label
        self.run_loop = True
        self.cap = None
        self.time_start = time.perf_counter()

    def get_result(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # initialize the cv2 QRCode detector
        detector = cv2.QRCodeDetector()

        while self.run_loop:
            _, img = self.cap.read()

            # End loop if nothing scanned within 30 seconds
            if time.perf_counter() - self.time_start > 30:
                break

            # Convert image to Tkinter and update the label on the parent form
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_update = ImageTk.PhotoImage(Image.fromarray(img))
            self.label.configure(image=img_update)
            self.label.image = img_update
            self.label.update()

            # detect and decode
            data, bbox, _ = detector.detectAndDecode(img)
            # check if there is a QRCode in the image
            if data:
                self.result = data
                break

        self.close_scanner()
        return self.result

    def close_scanner(self):
        self.cap.release()
        cv2.destroyAllWindows()
