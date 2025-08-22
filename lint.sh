#!/bin/bash

echo "Running isort..."
isort --profile black .

echo "Running black..."
black .

echo "Running flake8..."
flake8 .

echo "Linting complete!"