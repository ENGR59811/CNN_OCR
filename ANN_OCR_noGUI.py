# The City College of New York, City University of New York
# Written by Olga Chsherbakova
# October, 2023
from CNN_Train import CNN_Train
from CNN_Predict import CNN_Predict
import os
from tensorflow.keras import models
import tkinter as tk
from PIL import Image, ImageDraw
import tempfile
# Optical character recognition using a CNN

def char_recognition_MAIN_noGUI():
    # select training directory
    train_dir = 'TrainingSet'
    # select reference and output directories
    ref_dir = 'ReferenceSet'
    saved_cnns = 'Saved_CNNs'
    print('WELCOME TO USING CNN. MAKE YOUR SELECTION:')
    print('Enter 1 to train a new CNN')
    print('Enter 2 to load an existing CNN')
    user_entry = input('Enter your choice: ')
    if user_entry == '1':
        #train a new CNN:
        print('Be patient until statistics are displayed...')
        model = CNN_Train(train_dir)
        input('CNN is trained. Press enter to use the CNN\n')
    elif user_entry == '2':
        # use an existing CNN:
        cnn_file = input('Enter CNN name (include .h5 extension): ')
        try:
            # load the CNN and assign it to cnn_trained
            model = models.load_model(os.path.join(saved_cnns, 
                                                   cnn_file))
        except:
            print('Need a valid file name... Leaving... Bye')
            return
    else:
        print('Need a valid choice... Leaving... Bye')
        return
    
    # Now there is a trained CNN loaded (either a new one or 
    # an existing one). Use trained CNN to make predictions:
 
    # start drawing a character
    image_path = draw_tool()
    CNN_Predict(model, ref_dir, image_path)    
    print('Have a predictably nice day!')
    os.remove(image_path)

def draw_tool():
    root = tk.Tk()
    root.title("Draw a Character")

    canvas_width = 280
    canvas_height = 280

    # Create a canvas for drawing
    canvas = tk.Canvas(root, width=canvas_width, 
                       height=canvas_height, bg="white")
    canvas.pack(pady=20)

    # Variables to store the last x and y positions
    lastx, lasty = None, None
    # Create an image to save
    image = Image.new("RGB", (canvas_width, canvas_height), 
                      "white")
    draw = ImageDraw.Draw(image)
    
    # Define filepath here
    filepath = ""

    def on_button_press(event):
        nonlocal lastx, lasty
        lastx, lasty = canvas.canvasx(event.x), canvas.canvasy(event.y)

    def on_mouse_drag(event):
        nonlocal lastx, lasty
        x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)
        canvas.create_oval((lastx, lasty, x, y), 
                           fill="black", width=10)
        draw.line([lastx, lasty, x, y], fill="black", width=10)
        lastx, lasty = x, y

    def save_image():
        nonlocal filepath
        # Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, 
                                suffix='.png') as tmp_file:
            filepath = tmp_file.name
        image.save(filepath)
        root.destroy()

    # Bind events to the canvas
    canvas.bind("<Button-1>", on_button_press)
    canvas.bind("<B1-Motion>", on_mouse_drag)

    # Add a save button
    save_button = tk.Button(root, text=
            "Ckick here when finished", command=save_image, 
            bg="blue", fg="white")
    save_button.pack(pady=20)

    root.mainloop()
    return filepath

char_recognition_MAIN_noGUI()
