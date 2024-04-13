import os
import tkinter as tk
from PIL import Image, ImageTk

# path to the images
img_dir = "C:\\Users\\Jan\\Documents\\Python Scripts\\DynamicSlideshow\\Images"

#timeout to switch to the next image (in ms)
timeout = 5000

class SlideshowApp:
    def __init__(self, window, images):
        self.window = window
        self.images = images
        self.index = 0

        # set background to black
        self.window.configure(bg="black")

        # frame for the image
        self.img_frame = tk.Frame(window, bg="black")
        self.img_frame.pack(expand=True)

        # label for the image
        self.image_label = tk.Label(self.img_frame, bg="black")
        self.image_label.pack(expand=True)

        # start the slide show
        self.show_next_image()

    def show_next_image(self):
        # check, if the end of the images has been reached
        if self.index == len(self.images):
            # reset the index to restart
            self.index = 0

        # load and display the image
        img_path = self.images[self.index]
        photo = ImageTk.PhotoImage(Image.open(img_path))
        self.image_label.configure(image=photo)
        self.image_label.image = photo

        # wait for 5 seconds and show next image
        self.index += 1
        self.window.after(timeout, self.show_next_image)

def main():
    # list of all images in the directory
    images = [os.path.join(img_dir, file) for file in os.listdir(img_dir)
              if file.endswith(('.jpg', '.jpeg', '.png'))]

    # create Tkinter window
    window = tk.Tk()
    window.title("Slideshow")
    window.configure(bg="black")

    # start Slideshow-App
    slideshow = SlideshowApp(window, images)

    # close the window, if it gets closed
    window.protocol("WM_DELETE_WINDOW", window.quit)

    # start Tkinter main loop
    window.mainloop()

if __name__ == "__main__":
    main()
