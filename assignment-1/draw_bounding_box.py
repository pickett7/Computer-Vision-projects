import cv2
import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk  # Import the Image and ImageTk classes

def draw_rectangle(event):
    global image, drawing, start_x, start_y, current_x, current_y 

    # Check if an image is loaded
    if image is None:
        return

    # Start drawing
    if not drawing:
        start_x, start_y = event.x, event.y
        drawing = True

    # Draw the rectangle on the image
    if drawing:
        current_x, current_y = event.x, event.y
        cv2.rectangle(image, (start_x, start_y), (current_x, current_y), (0, 255, 0), 2)

        
        update_image()

def release_rectangle(event):
    global drawing
    drawing = False

def update_image():
    # Convert the OpenCV image to a PhotoImage object
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(image_rgb)
    img = ImageTk.PhotoImage(image=img)

    # Update the Tkinter canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=img)
    canvas.image = img

def getBoundingBox(image_from_video):
    global image, canvas
    
    image = image_from_video
  
    # Create the main window
    root = tk.Tk()
    root.title("Draw Rectangle on Image")

    # Create a canvas to display the image
    canvas = Canvas(root, width=image.shape[1], height=image.shape[0])
    canvas.pack()

    # Bind mouse events to the canvas
    canvas.bind("<ButtonPress-1>", draw_rectangle)
    canvas.bind("<B1-Motion>", draw_rectangle)
    canvas.bind("<ButtonRelease-1>", release_rectangle)

    # Display the initial image
    update_image()

    # Start the GUI
    root.mainloop() # Stops when the window is closed
    print("Co-ordinates of the bounding box: ",start_x, start_y,current_x, current_y)
    return start_x, start_y,current_x, current_y

canvas = None
image = None
drawing = False
start_x, start_y = -1, -1
current_x, current_y = -1, -1
