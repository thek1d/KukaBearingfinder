#!/usr/bin/bash

rm forces.csv
python3 Service_Force_Messurement.py &
python3 plotForces.py
