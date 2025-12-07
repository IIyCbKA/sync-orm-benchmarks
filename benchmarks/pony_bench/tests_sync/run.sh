#!/bin/sh

cd $(dirname $0)

# Add a root dir for correct imports
export PYTHONPATH=..

# Test 1 -> Insert
python -m test_1

# Test 2 -> Transaction Insert
python -m test_2

# Test 3 -> Bulk Insert
python -m test_3

# Test 4 -> Filter large
python -m test_4
