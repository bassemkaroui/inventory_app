#!/usr/bin/env bash

# Run coverage tests for app
pytest --cov=app tests/

# Generate coverage report
coverage report -m

# Run coverage tests for sample_requests
pytest --cov=sample_requests tests/

# Generate coverage report
coverage report -m
