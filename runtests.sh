#!/bin/bash
# Runs all unit tests

export PYTHONPATH=$(pwd)/combatant
python3 -m unittest discover tests
