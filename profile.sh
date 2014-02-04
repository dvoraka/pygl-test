#! /bin/bash

python -O -m cProfile -s 'cumulative' gltest.py > `date '+%Y%m%d-%H%M'`".prof"

exit 0
