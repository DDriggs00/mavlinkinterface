# Contributing

If you want to add a feature, make a new Mavlink message available, or integrate a new sensor package, this guide will show you how to do that.

## General Information

If you are unfamiliar with git and GitHub, check out [this guide](http://git.huit.harvard.edu/guide/).

If you are unfamiliar with contributing to open source projects, check out [this guide](https://akrabat.com/the-beginners-guide-to-contributing-to-a-github-project/).

## Bug Reports

To file a bug report, create a new Issue with the following information:

1. Steps to replicate the bug
2. All relevant logs

## General guidelines

- Always perform logging using `from mavlinkinterface.logger import getLogger`. Logging levels are:
  - trace: for progress messages not useful to the user
  - debug: for information useful in debugging, but not important to user
  - rdata: When a function returns data, log the data with this before returning
  - info: for progress data useful to the user. This, and levels below this, are printed to the console when using the 'main' logger.
  - warn: For issues that are easily corrected without causing the program to stop.
  - error: for errors
- If a new function is made, use [type-hinting](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html#functions) for both parameters and return values.
- Always include a docstring at the beginning of functions
- Functions that cause the drone to take physical action must support all 4 execution modes
- All new functions must have a markdown file in the documentation folder, which must be linked in the appropriate section of [functions.md](functions.md)
  - A short description of the function
  - All parameters of the function
  - The return value of the function
  - at least one example
  - If JSON is returned, an example output

## Adding a New Mavlink Message

Not all mavlink messages are read by default due to the computation cost (and therefore power cost).  
If a message is needed, but not read, add it to the list as follows:

In mavlinkInterface class `__init__` function in `main.py`, go to the 'Set Messages to be Read' section, add the full message name to the `self.readMessages` definition

## Adding a new sensor

Because most attached sensors behave in different ways, most of this will be unique to your sensor, but there are several things that make it easier.

- If the sensor has its own python interface, consider creating a class for it (like how Sonar is implemented).
- All returned sensor data must be converted to the SI unit that makes the most sense
