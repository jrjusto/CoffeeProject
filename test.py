from picamera2 import Picamera2
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

#from camera_capture import CameraCapture

class CameraCapture:
    def __init__(self):
        self.camera = Picamera2()
        
        self.camera.configure(self.camera.create_video_configuration())
        self.camera.start()
    
    def get_frame(self):
        frame = self.camera.capture_array()
        return frame

    def stop(self):
        self.camera.stop_recording()
        self.camera.close()



class VideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PiCamera2 Video Feed")

        self.label = Label(root)
        self.label.pack()

        self.camera = CameraCapture()

        self.update_frame()

    def update_frame(self):
        frame = self.camera.get_frame()
        image = Image.fromarray(frame)
        image = ImageTk.PhotoImage(image)

        self.label.configure(image=image)
        self.label.image = image

        self.root.after(1, self.update_frame)  # Update every 30ms

    def on_close(self):
        self.camera.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
