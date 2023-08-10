# neurograph-framework // audit_subprocess
# v0.378 // aug 10, 2023 // https://github.com/FlyingFathead

# imports
# image inverter
from PIL import Image, ImageOps

# other imports
import sys
import os
import glob
import re
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Shadow
import numpy as np
import shutil
import datetime
import time

# Set the name of the project or model
project_name = "my_project"

# Set the name of the scatter plot image file
scatterplot_imagefile = f"{project_name}_scatter_plot.png"

# Set the name of the scatter plot's overlay image file
scatterplot_imagefile_overlay = f"{project_name}_scatter_plot_overlay.png"

# Set the name of the output inverted image file
output_filename = f"./__graphout/{project_name}_scatter_plot_inverted.png"

# Log file directory
logs_dir_path = './logs/'

# Command line arguments
# Get the set name from command-line argument
setname = sys.argv[1] if len(sys.argv) > 1 else '<unknown set>'

# Get the logs directory path from command-line argument or use the default
dir_path = sys.argv[2] if len(sys.argv) > 2 else logs_dir_path

# Get the current timestamp
timestamp = datetime.datetime.now()
timestamp_formatted = timestamp.strftime("%m/%d/%Y %H:%M:%S")
# print(f"Timestamp: {timestamp_formatted}")

# timestamp
now = time.strftime('%Y-%m-%d %H:%M:%S')  # Get the current time

# Get the terminal width
width = shutil.get_terminal_size().columns

# Generate the dotted line
dotted_line = '-' * width

# Use glob to get a list of all text files in the directory
text_files = glob.glob(dir_path + '/*.txt')

# Sort the list of text files by modification time
text_files.sort(key=lambda x: os.path.getmtime(x))

# Get the latest text file (last modified text file)
latest_text_file = text_files[-1]

# Define a function to parse the log file
def parse_log(log_file):
  # Initialize variables to store the data
  iteration = []
  time = []
  loss = []
  avg = []

  # Compile the regular expression pattern
  pattern = re.compile(r"^\[(\d+) \| (\d+\.\d+)\] loss=(\d+\.\d+) avg=(\d+\.\d+)$")

  # Open the log file and read it line by line
  with open(log_file, 'r') as f:
    for line in f:
      # Match the line against the regular expression pattern
      match = pattern.match(line)
      if match is None:
        continue

      # Extract the data from the line and store it in the appropriate variable
      iteration.append(int(match.group(1)))
      time.append(float(match.group(2)))
      loss.append(float(match.group(3)))
      avg.append(float(match.group(4)))

  # Return the data as a tuple
  return (iteration, time, loss, avg)

### NEW CODE FOR POLLER
# '''
# Set the initial modification time of the text file
prev_mod_time = 0

# Parse the log file
iteration, time, loss, avg = parse_log(latest_text_file)

# Check if the data is empty
if not iteration:
    # If the data is empty in the latest file, try the second-to-latest file
    second_latest_text_file = text_files[-2]
    iteration, time, loss, avg = parse_log(second_latest_text_file)
    print(dotted_line)
    print(f"[{now}] Warning! The latest file '{latest_text_file}' didn't contain the expected data.")
    print(f"[{now}] Reverting to: '{second_latest_text_file}'")
    print(dotted_line)

    if not iteration:
        # Display a gray overlay with a red warning text for both files
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('0.85')  # Gray overlay

        ax.text(0.5, 0.5, "Outdated or missing data", transform=ax.transAxes, ha="center",
                fontsize=20, color='red')  # Red warning text
        
        # Add timestamp at the bottom center of the plot
        ax.text(0.5, -0.05, f'Timestamp: {timestamp_formatted}', transform=ax.transAxes, ha="center", color='black')

        ax.axis('off')  # Turn off axes

        # Save the plot as a PNG image with the overlay
        fig.savefig(scatterplot_imagefile_overlay, format='png', dpi=300)

        # Open the image file with the overlay
        image = Image.open(scatterplot_imagefile_overlay)
        image = image.convert('RGB')

        # Resize the image to 640x480 pixels
        resized_image = image.resize((640, 480))

        # Save the resized image with the overlay
        resized_image.save(output_filename)

else:

  # Print the data
  print("Iteration,Time,Loss,Avg")
  for i in range(len(iteration)):
    print(f"{iteration[i]},{time[i]},{loss[i]},{avg[i]}")

  # Create the plot
  fig, ax = plt.subplots()
  # ax.plot(iteration, loss, 'ro', alpha=0.3, markersize=1)  # plot loss data with semi-transparent red circular markers

  # Find the maximum and minimum values of the data
  max_val = max(avg)
  min_val = min(avg)

  # Find the x-coordinates at which the maximum and minimum values occur
  max_index = np.argmax(avg)
  min_index = np.argmin(avg)

  # Calculate the median value of the avg data
  median_val = np.median(avg)

  # Add annotations for the maximum and minimum values
  # MAX & MIN ONLY; NO IT. #
  ax.annotate(f'max: {max_val:.2f}', xy=(iteration[max_index], max_val), xytext=(iteration[max_index], max_val + 0.5),
              arrowprops=dict(facecolor='black', shrink=1, alpha=0.5, width=0.5), ha='center')
  ax.annotate(f'min: {min_val:.2f}', xy=(iteration[min_index], min_val), xytext=(iteration[min_index], min_val - 0.5),
              arrowprops=dict(facecolor='black', shrink=1, alpha=0.5, width=0.5), ha='center')

  # Get the latest iteration number and avg value
  latest_iteration = iteration[-1]
  latest_avg = avg[-1]

  # Add a text box with the latest iteration number and avg value
  ax.text(0.95, 0.95, f'latest #{latest_iteration}\navg: {latest_avg:.2f}',
          verticalalignment='top', horizontalalignment='right',
          transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.5))   

  # Add horizontal lines at the locations of the minimum and maximum values
  ax.axhline(y=min_val, color=(0/255, 128/255, 255/255), linestyle='--')
  ax.axhline(y=max_val, color=(0/255, 128/255, 255/255), linestyle='--')

  # Plotting the graph
  ax.scatter(iteration, loss, c='r', s=1, alpha=0.6)  # plot loss data as red markers of size 20
  ax.plot(iteration, avg, 'b--')  # plot avg data with blue dotted lines
  ax.plot(iteration, [median_val] * len(iteration), 'g--') # Plot the median curve

  # Disable scientific notation for the x-axis
  ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

  # Set the x-axis tick locations to the first and last values
  ax.set_xticks([iteration[0], iteration[-1]])

  # Set the x-axis tick labels to the first and last values
  ax.set_xticklabels([iteration[0], iteration[-1]])

  # Find the minimum values of the loss and avg data
  min_loss = min(loss)
  min_avg = min(avg)

  # Find the maximum values of the loss and avg data
  max_loss = max(loss)
  max_avg = max(avg)

  # Find the first iteration number
  first_iteration = iteration[0]

  # Add text on top of the graph box
  ax.text(0.5, 1.06, f"setname: {setname} | start: {first_iteration}", transform=ax.transAxes, ha="center", fontsize=10)
  ax.text(0.5, 1.01, f"min (avg): {min_avg:.2f} | max (avg): {max_avg:.2f} | min (single): {min_loss:.2f} | max (single): {max_loss:.2f}", transform=ax.transAxes, ha="center", fontsize=10)

  # Add a legend and labels
  ax.legend()
  latest_iteration = iteration[-1]
  #ax.set_xlabel(f'iteration (latest: {latest_iteration})')
  ax.set_xlabel(f'{timestamp_formatted}')
  ax.set_ylabel('entropy loss')

  # Set the figure size to 640x480 pixels
  # fig = plt.figure(figsize=(640/300, 480/300))

  # Save the plot as a PNG image with a resolution of 300 DPI
  fig.savefig(scatterplot_imagefile, format='png', dpi=300)

  # Save the plot as a PNG image with a size of 640x480 pixels
  #fig.savefig(scatterplot_imagefile, format='png', dpi=300,
  #            bbox_inches='tight', pad_inches=0,
  #            width=640, height=480)

  # Open the image file
  print(f"[{now}] Opening image file...")
  image = Image.open(scatterplot_imagefile)

  # Convert the image to the "RGB" mode to remove the alpha channel
  print(f"[{now}] Converting image to RGB mode...")
  image = image.convert('RGB')

  # Resize the image to 640x480 pixels
  print(f"[{now}] Resizing image to 640x480 pixels...")
  resized_image = image.resize((640, 480))

  # Invert the colors of the image
  print(f"[{now}] Inverting colors of image...")
  inverted_image = ImageOps.invert(resized_image)

  # Save the inverted image to a new file
  print(f"[{now}] Saving inverted image to file '{output_filename}'...")
  inverted_image.save(output_filename)

  print(f"[{now}] Done! Inverted image saved to '{output_filename}'.")
