# neurograph-framework // audit_logs_poller
# v0.379 // jan 14, 2024 // https://github.com/FlyingFathead
# https://github.com/FlyingFathead/neurograph-framework/

import re
import tkinter as tk
import os
import time
import shutil
from PIL import Image, ImageTk
import subprocess

# Set the variables for the project
log_directory = "./logs/"
graph_output_directory = "./__graphout/"
script_directory = "./"
project_root_directory = "./"
value_data_directory =  "./.valuedata/"

# set the root title
root_title = "neurograph"

# Set the name of the project or model
project_name = "my_model"

# Set the name of the image file
image_file = f"./__graphout/{project_name}_scatter_plot_inverted.png"

# timestamp
now = time.strftime('%Y-%m-%d %H:%M:%S')  # Get the current time

# Get the terminal width
width = shutil.get_terminal_size().columns

# Generate the dotted line
dotted_line = '-' * width

# startup
print(dotted_line)
print(f"[{now}] Neurograph poller started.")
print(dotted_line)

def get_setname(log_directory):
    latest = -float("inf")
    latest_file = None

    for file in os.listdir(log_directory):
        print(f"Found file: {file}")        
        file_path = os.path.join(log_directory, file)
        if file.startswith("gpt_train_") and os.path.getmtime(file_path) > latest:
            latest = os.path.getmtime(file_path)
            latest_file = file_path

    if latest_file is None:
        print(f"[{now}] No log files found in the directory.")
        return None

    print(f"[{now}] Latest log file is: {latest_file}")

    with open(latest_file, "r") as f:
        setname = next(line for line in f if line.startswith("::: Source dataset file name: "))
    setname = setname.replace("::: Source dataset file name: ", "")
    print(f"[{now}] [INFO] The following set name was found: {setname}")
    raw_setname = setname
    
    dataset_type = "unknown"  # Set a default value for dataset_type
    if os.path.isdir(raw_setname):
        dataset_type = "dir"
        setname = os.path.basename(os.path.normpath(raw_setname))
    elif os.path.isfile(raw_setname):
        dataset_type = "file"
        setname = os.path.basename(raw_setname).split(".")[0]
    if setname == "":
        print(f"[{now}] [WARN] {raw_setname} -- set name is empty!")

    return setname  # Return the modified setname variable

# Check if the file exists
if not os.path.exists(image_file):
    print(f"[{now}] Error: File '{image_file}' not found")
#    exit()

# Create the root window
root = tk.Tk()
root.title(root_title)

# Set the background color to black
root.configure(bg="black") 

# Set the window size
root.geometry("640x480")

# Create a label to display the image
label = tk.Label(root, bg="black")  # Set the background color of the label to black
label.pack()

def refresh_image():
    # Print start of refresh
    print(f"[{now}] Starting image refresh...")
    
    # Get the set name
    path = get_setname(log_directory)
    if path is None:
        print(f"[{now}] Error: No set name found.")
        return

    components = path.split("/")

    # Handling path based on its content
    components = path.split("/")
    if len(components) >= 2:
        final_string = components[-2]
    else:
        # If there's only one component, it's just a filename
        # So, we'll use the filename without extension
        final_string = os.path.splitext(components[0])[0]

    print(f"[{now}] Set is: {final_string}")
    
    # switch to dir
    os.chdir(script_directory)
    
    # Run the other script    
    print(f"[{now}] About to run audit_subprocess.py...")
    process = subprocess.Popen(["python3", "audit_subprocess.py", final_string])
    process.wait()
    print(f"[{now}] Finished running audit_subprocess.py.")

    # A hack to bypass tkinter's image caching
    cache_buster = "?" + str(time.time())
    updated_image_file = image_file + cache_buster
    
    # Read the image file
    image = Image.open(image_file)

    # Resize the image
    image = image.resize((640, 480), Image.Resampling.LANCZOS)

    # Convert the image to a PhotoImage object
    image = ImageTk.PhotoImage(image)

    # Update the image on the label
    label.configure(image=image)
    label.image = image

    print(f"[{now}] Our dataset name according to log is: {final_string}")

    # Call this function again after 20 seconds (increased from 10 seconds)
    root.after(20000, refresh_image)


# Call the refresh_image function for the first time
refresh_image()

# Run the Tkinter event loop
root.mainloop()
