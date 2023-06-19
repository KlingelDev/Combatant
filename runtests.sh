#!/bin/bash
# Runs all unit tests

export PYTHONPATH=$(pwd)
python3 -m unittest discover tests
