#!/usr/bin/bash

cd /opt/program
export PYTHONPATH=$PYTHONPATH:/opt/program/src/
/usr/bin/bash -c "source activate state-of-indices-env && exec python src/main.py local"
