# neurograph-framework

![neurograph-framework](https://github.com/FlyingFathead/neurograph-framework/scatter_plot_inverted.png)

**neurograph-framework** is a versatile tool designed to help you visualize entropy loss in TensorFlow-based neural network training. It generates insightful scatter plots with annotations to aid in understanding and analyzing your training progress.

## Features

- Creates scatter plots that display entropy loss over training iterations.
- Annotations for minimum and maximum loss values as well as per-iteration scatter.
- Indication of the latest iteration number and average loss value.
- Overlay warnings in case of missing or outdated data.
- Customizable to suit various types of iteration data, suitable for all kinds of visualization purposes.
- Intended to visualize entropy losses as effectively as possible (min/max lines, median, per-it. scatter etc).

## Usage

1. Clone this repository to your local machine:
```
git clone https://github.com/FlyingFathead/neurograph-framework/
```
2. Navigate to the cloned directory:
```
cd neurograph-framework/
```
3. Install the PyPi requirements with `pip install -r requirements.txt`

(these are):
```
matplotlib>=3.5.1
Pillow>=9.1.0
numpy>=1.23.5
```

4. Run the audit_subprocess.py script to start visualizing your neural network training data:
```
python audit_subprocess.py setname logs_directory
```

The plotter graphs are updated every 20 seconds by default.

Happy training and analyzing with neurograph-framework! 📊🧠
