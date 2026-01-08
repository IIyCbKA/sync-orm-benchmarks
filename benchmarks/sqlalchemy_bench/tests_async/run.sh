#!/bin/sh

cd $(dirname $0)

# Add a root dir for correct imports
export PYTHONPATH=..
python -m warmup
python -m test_1   # single create
python -m test_2   # batch create
python -m test_3   # bulk create
python -m test_4   # nested create
python -m test_5   # find all
python -m test_6   # find first
python -m test_7   # nested find first
python -m test_8   # find unique
python -m test_9   # nested find unique
python -m test_10  # filter, paginate & sort
python -m test_11  # update batch
python -m test_12  # update single
python -m test_13  # nested batch update
python -m test_14  # batch delete
python -m test_15
python -m test_16
python -m test_17