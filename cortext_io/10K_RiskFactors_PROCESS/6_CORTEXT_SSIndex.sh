#!/bin/sh
# CORTEXT StraightShooter Index Generation Script
# This script executes the Python module that calculates and visualizes the StraightShooter indices
# The StraightShooter indices measure sentiment patterns across three dimensions:
# - Existence (positive/negative assertions about reality)
# - Expression (positive/negative ways of communicating)
# - Sentiment (positive/negative emotional content)
# The script generates 3D vector visualizations for both "Cold" and "Warm" interpretations

python3 StraightShooterIndex.py
