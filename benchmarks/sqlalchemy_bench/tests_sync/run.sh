#!/bin/sh
set -e

cd $(dirname $0)

# Add a root dir for correct imports
export PYTHONPATH=..

# db warm-up
python -m warmup

# Test 1 -> Single create
python -m test_1

# Test 2 -> Transaction create
python -m test_2

# Test 3 -> Bulk create
python -m test_3

# Test 4 -> Find all
python -m test_4

# Test 5 -> Find first
python -m test_5

# Test 6 -> Find unique record
python -m test_6

# Test 7 -> Find with limit and include parent
python -m test_7

# Test 8 -> Find with filter, offset pagination and sort
python -m test_8

# Test 9 -> Single update
python -m test_9

# Test 10 -> Transaction update
python -m test_10

# Test 11 -> Bulk update
python -m test_11

# Test 12 -> Single delete
python -m test_12

# Test 13 -> Transaction delete
python -m test_13

# Test 14 -> Bulk delete
python -m test_14
