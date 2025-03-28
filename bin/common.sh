#!/bin/bash

PYTHON=python3
if ! command $PYTHON --version &>/dev/null; then
    PYTHON=python
fi
if ! command $PYTHON --version &>/dev/null; then
    PYTHON=py
fi
if ! command $PYTHON --version &>/dev/null; then
    echo "Python is not installed. Please install Python to run this script."
    exit 1
fi
