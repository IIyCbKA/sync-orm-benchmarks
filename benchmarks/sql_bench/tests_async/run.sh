#!/bin/sh

cd $(dirname $0)

# Add a root dir for correct imports
export PYTHONPATH=..

python -m warmup

# Test 1 -> Single create
python -m test_1

# Test 2 -> Batch create
python -m test_2

# Test 3 -> Bulk create
python -m test_3

# Test 4 -> Nested create
python -m test_4

# Test 5 -> Find all
python -m test_5

# Test 6 -> Find first
python -m test_6

# Test 7 -> Nested find first
python -m test_7

# Test 8 -> Find unique
python -m test_8

# Test 9 -> Nested find unique
python -m test_9

# Test 10 -> Filter, paginate & sort
python -m test_10

# Test 11 -> Batch update
python -m test_11

# Test 12 -> Single update
python -m test_12

# Test 13 -> Nested batch update
python -m test_13

# Test 14 -> Batch delete
python -m test_14

python -m test_15

python -m test_16

python -m test_17