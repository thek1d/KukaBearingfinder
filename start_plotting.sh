#!/usr/bin/bash

FILE=forces.csv
if [ -f "$FILE" ]; then
	rm forces.csv
fi
python3 Service_Force_Messurement.py &
python3 plotForces.py
