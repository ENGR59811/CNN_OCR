import numpy as np
import os
from PIL import Image
from tensorflow.keras.preprocessing import image as keras_image
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
# this GUI shows prediction for the character drawn by the user 

def display_images_tkinter(model,char_img_path, ref_image_path):
    root = tk.Tk()
    root.title("Character Recognition Using CNN")

    # Load the images
    char_img = Image.open(char_img_path).convert('L')
    ref_img = Image.open(ref_image_path).convert('L')
    
    # Resize the prediction image
    ref_img = ref_img.resize((250,250))

    char_img_tk = ImageTk.PhotoImage(char_img)
    ref_img_tk = ImageTk.PhotoImage(ref_img)

    # Create labels for the images
    char_label = tk.Label(root, image=char_img_tk)
    char_label.pack(side=tk.LEFT, padx=10)

    ref_label = tk.Label(root, image=ref_img_tk)
    ref_label.pack(side=tk.LEFT, padx=10)
    
    def save_and_quit():
        file_name = filedialog.asksaveasfilename(defaultextension=".h5",\
                                filetypes=[("H5 files", "*.h5")])
        if file_name:
            model.save(file_name)
        # root.mainloop()
        root.destroy()
        
    
    def quit_root():
        root.destroy()
        
    # Button to save the model and quit
    save_quit_button = tk.Button(root, text="Save Model and Exit", \
                                 command=save_and_quit)
    save_quit_button.pack(pady=20)
    save_quit_button = tk.Button(root, text="Exit", command=quit_root)
    save_quit_button.pack(pady=20)

    root.mainloop()
    
def CNN_Predict(model, ref_path, char_img_path):
    # Load and preprocess the image
    char_img = keras_image.load_img(char_img_path, target_size=(28, 28),\
                                    color_mode='grayscale')
    char_img_array = keras_image.img_to_array(char_img)
    char_img_array = np.expand_dims(char_img_array, axis=0)
    char_img_array /= 255.0

    # Make a prediction
    predictions = model.predict(char_img_array)
    predicted_class = np.argmax(predictions[0])
    class_names = sorted(os.listdir(ref_path))
    predicted_class_name = class_names[predicted_class]

    # Retrieve the appropriate reference image for prediction
    ref_image_path = os.path.join(ref_path, predicted_class_name, \
                os.listdir(os.path.join(ref_path, predicted_class_name))[0])
    
    display_images_tkinter(model,char_img_path, ref_image_path)