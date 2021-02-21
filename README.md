Workshop: Introduction to Programming
=====================================

This repository contains the material used in the Intro to Python/C++ Programming workshop.

# Prerequisites

The python part requires Python 3 installed in the system, with a few additional packages.

## Option 1: install the required library in the system

```
sudo pip3 install -r requirements.txt
```
or to only install for the current user:
```
pip3 install -r requirements.txt --user
```

## Option 2: use a python vitrual environment

```
python3 -m venv --clear env
source env/bin/activate
pip install -r requirements.txt
```

