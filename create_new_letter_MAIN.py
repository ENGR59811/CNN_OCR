import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

class CharacterCreator:
    def __init__(self, master):
        self.master = master
        self.master.title("Character Creator")
        self.master.geometry("600x400")
        self.master.config(bg="#DAF0D3")

        # Create the drawing canvas
        self.canvas = tk.Canvas(self.master, width=400, height=280, bg="white")
        self.canvas.place(x=100, y=60)
        self.image = Image.new("RGB", (400, 280), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.bind("<B1-Motion>", self.paint)

        # Welcome message
        message = "WELCOME TO CHARACTER CREATOR. USE THIS PROGRAM TO POPULATE YOUR TRAINING AND REFERENCE SETS."
        self.label = tk.Label(self.master, text=message, font=("Arial", 10), bg="#FFE2BD", wraplength=500, justify="center")
        self.label.place(x=50, y=20, width=500, height=40)

        # Buttons for saving, ending the drawing session, and closing the application
        self.save_button = tk.Button(self.master, text="Save Drawing", font=("Arial", 14), bg="#4D72BD", fg="white", command=self.save_image)
        self.save_button.place(x=10, y=350, width=190, height=40)

        self.end_button = tk.Button(self.master, text="Clean", font=("Arial", 14), bg="#4D72BD", fg="white", command=self.end_drawing)
        self.end_button.place(x=205, y=350, width=190, height=40)

        self.close_button = tk.Button(self.master, text="Close", font=("Arial", 14), bg="#4D72BD", fg="white", command=self.master.destroy)
        self.close_button.place(x=400, y=350, width=190, height=40)

    def paint(self, event):
        # Draw on the canvas
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill="black", width=5)
        self.draw.ellipse([x1, y1, x2, y2], fill="black")

    def save_image(self):
        # Resize the image to 28x28 pixels and convert to grayscale before saving
        grayscale_image = self.image.convert('L').resize((28, 28), Image.Resampling.LANCZOS)
        file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png')])
        if file_path:
            grayscale_image.save(file_path, 'PNG')

    def end_drawing(self):
        # Clear the canvas and reset the image
        self.canvas.delete("all")
        self.image = Image.new("RGB", (400, 280), "white")
        self.draw = ImageDraw.Draw(self.image)

# Running the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = CharacterCreator(root)
    root.mainloop()
