#!/usr/bin/env sh

# -m unittest: Runs the unittest module as a script
# discover: Search for test files
# -s src: Look inside the 'src' directory
python3 -m unittest discover -s src
