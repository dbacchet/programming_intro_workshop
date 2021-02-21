Workshop: Introduction to Programming
=====================================

This repository contains the material used in the Intro to Python/C++ Programming workshop.

# Prerequisites

The python part requires Python 3 installed in the system, with a few additional packages.
The recommended way to install the dependencies is using `pip`. See [here](https://pip.pypa.io/en/stable/installing/) for instructions on how to install `pip`.

### Option 1: install the required libraries in the system

```
sudo python3 -m pip install -r requirements.txt
```
or to install for the current user only:
```
python3 -m pip install -r requirements.txt --user
```

### Option 2: use a python virtual environment

```
python3 -m venv --clear env
source env/bin/activate
pip install -r requirements.txt
```
then when you want to use the virtual environment with the installed dependencies, just run 
```
source env/bin/activate
```
in the terminal you are using.

### Test if all the required packages are installed

from the terminal:
```
python3 python_step0/renderer.py
```
If you see a window with a grid, then you are good to go.

# Content

## Step 0: setup the environment

The folder `python_step0` contains a sample program that just opens a 3D window to check if the environment has all the required dependencies

In this part we will cover the basics of Python, explaining:

* basic syntax
* type system
* documentation

## Step 1: basic 2D vector class

In this part we will create a basic 2D vector class. We will explore:

* object-oriented programming
* creating a simple class
* implementing unit tests
* implementing operators

The final code for this section is in the folder `python_step1_vector`.

## Step 2: create a simple 2D physics system

In this part we will use the `Vector2d` class as starting point to create a simple Physics System, with support for collisions and integration of the dynamics.
We will explore:

* creating more complex objects
* using collections
* algorithmic complexity

The final code for this section is in the folder `python_step2_physics`.

At the end of this section, we'll have an app like the following:
![sample_physics](resources/sample_physics.gif)

