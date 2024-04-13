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

    def check_for_new_images(self):
        # get all images inside the diretory
        all_images = set(os.listdir(img_dir))
        # get filenames of the knonw images
        known_images = [os.path.basename(file) for file in self.images]
        # check for new images
        new_images = all_images.difference(known_images)
        # if at least one new image exist...
        if new_images:
            self.images.insert(self.index, os.path.join(img_dir, next(iter(new_images))))

    def show_next_image(self):
        # check, if the end of the images has been reached
        if self.index == len(self.images):
            # reset the index to restart
            self.index = 0
            # reload images
            self.images = [os.path.join(img_dir, file) for file in os.listdir(img_dir)
                           if file.endswith(('.jpg', '.jpeg', '.png'))]
        
        self.check_for_new_images()
        # load image
        img_path = self.images[self.index]
        img = Image.open(img_path)
        # resize image, if to width
        if img.width > self.window.winfo_screenwidth():
            resize_factor = self.window.winfo_screenwidth() / img.width
            img = img.resize((int(img.width * resize_factor), int(img.height * resize_factor)))
        # resize image, if to height
        if img.height > self.window.winfo_screenheight():
            resize_factor = self.window.winfo_screenheight() / img.height
            img = img.resize((int(img.width * resize_factor), int(img.height * resize_factor)))

        # display image
        photo = ImageTk.PhotoImage(img)
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

    # get screen size to center images
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    # set window size
    window.geometry(f"{screen_width}x{screen_height}")
    window.attributes("-fullscreen", True)

    # start Slideshow-App
    slideshow = SlideshowApp(window, images)

    # close the window, if it gets closed
    window.protocol("WM_DELETE_WINDOW", window.quit)

    # start Tkinter main loop
    window.mainloop()

if __name__ == "__main__":
    main()
