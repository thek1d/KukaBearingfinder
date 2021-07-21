#!/usr/bin/bash

FILE=forces.csv
if [ -f "$FILE" ]; then
	rm forces.csv
fi

trap "exit" INT TERM ERR
trap "kill 0" EXIT

python3 Service_Force_Messurement.py &
python3 plotForces.py

wait

