"""
Description:
  Graphical user interface that displays the official artwork for a
  user-specified Pokemon, which can be set as the desktop background image.

Usage:
  python poke_image_viewer.py
"""

from tkinter import *
from tkinter import ttk
import os
import poke_api

# Get the script and images directory
script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, 'images')

# Create the images directory if it does not exist
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

# Create the main window
root = Tk()
root.title("Pokemon Viewer")

# Set the icon
icon_path = os.path.join(script_dir, 'icon.ico')
print(f"Icon path: {icon_path}")

try:
    root.iconbitmap(icon_path)
except TclError as e:
    print(f"Error setting icon: {e}")

# Create frames
frame_top = Frame(root)
frame_top.pack(padx=10, pady=10)

frame_bottom = Frame(root)
frame_bottom.pack(padx=10, pady=10)

# Function to update the image and enable the button when a Pokemon is selected
def on_pokemon_select(event):
    selected_pokemon = combobox.get()
    image_path = poke_api.download_pokemon_image(selected_pokemon, images_dir)
    
    if image_path:
        img = PhotoImage(file=image_path)
        image_label.config(image=img)
        image_label.image = img
        set_desktop_button.config(state=NORMAL)

# Function to set the selected Pokemon image as the desktop background
def set_as_desktop():
    selected_pokemon = combobox.get()
    image_path = os.path.join(images_dir, f"{selected_pokemon.capitalize()}.png")
    
    if os.name == 'nt':  # Windows
        import ctypes
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)

# Create a combobox with Pokemon names
pokemon_list = poke_api.get_pokemon_list()
combobox = ttk.Combobox(frame_top, values=pokemon_list)
combobox.bind('<<ComboboxSelected>>', on_pokemon_select)
combobox.pack(side=LEFT, padx=10, pady=10)

# Create a label to display the Pokemon image
image_label = Label(frame_top)
image_label.pack(side=LEFT, padx=10, pady=10)

# Create the "Set as Desktop Image" button
set_desktop_button = Button(frame_bottom, text="Set as Desktop Image", command=set_as_desktop, state=DISABLED)
set_desktop_button.pack(pady=10)

# Run the application
root.mainloop()