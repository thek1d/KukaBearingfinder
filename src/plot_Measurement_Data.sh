#!/usr/bin/bash

FILE=Measurement_Data.csv
if [ -f "$FILE" ]; then
	rm Measurement_Data.csv
fi

trap "exit" INT TERM ERR
trap "kill 0" EXIT

python3 Service_Log_Measurement_Data.py &
python3 plot_Measurement_Data.py

wait

