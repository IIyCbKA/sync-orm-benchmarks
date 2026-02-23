#!/bin/sh
set -e

cd $(dirname $0)

export DJANGO_SETTINGS_MODULE="core.settings"

# Add a root dir for correct imports
export PYTHONPATH=..

# db warm-up
python -m warmup

# Test 1 -> Single object creation
python -m test_1

# Test 2 -> Creation of objects in a transaction
python -m test_2

# Test 3 -> Bulk creation of objects
python -m test_3

# Test 4 -> Retrieval of all records
python -m test_4

# Test 5 -> Retrieval of the first record
python -m test_5

# Test 6 -> Retrieval by primary key
python -m test_6

# Test 7 -> Retrieval with limit including attributes of related record
python -m test_7

# Test 8 -> Filtered retrieval with offset pagination and sorting
python -m test_8

# Test 9 -> Single object update
python -m test_9

# Test 10 -> Update of objects in a transaction
python -m test_10

# Test 11 -> Bulk update of objects
python -m test_11

# Test 12 -> Single object deletion
python -m test_12

# Test 13 -> Deletion of objects in a transaction
python -m test_13

# Test 14 -> Bulk deletion of objects
python -m test_14
