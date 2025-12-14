#!/bin/sh

cd $(dirname $0)

export DJANGO_SETTINGS_MODULE="core.settings"

# Add a root dir for correct imports
export PYTHONPATH=..

# Test 1 -> Single create
python -m test_1

# Test 2 -> Batch create
python -m test_2

# Test 3 -> Bulk create
python -m test_3