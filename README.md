# <u>Force/Torque- measurement</u>

- <i> Service_Log_Measurement_Data.py </i> should be running as a service. This service is requesting data via MQTT and logs in into a <i>Measurement_Data.cvs</i> file.
- <i> Plot_Measurement_Data.py </i> is plotting the data as a live graph in 40msec intervalls.

Example:
![Test](img/Testlauf_13_7_21.png)

## How To: <br>
First run the service which is logging the data like this
- python3 Service_Log_Measurement_Data.py

Afterwards run

- python3 Plot_Measurement_Data.py

or by just executing the script "<i>Plot_Measurement_Data.sh</i>"

Now you should see an empty plot, for getting data you need to enable logging via publishing following to the topic <i>BearingFinder/EnableDBLogging</i>

- {"enable" : "true"}

![enable](img/enable_logging.png)

This can be done by any MQTT Client or an MQTT tool like <i>MQTT Explorer</i> 

## Stopping plotting

This can be done by publishing a message to the same topic where enabling it <i>BearingFinder/EnableDBLogging</i>


- {"enable" : "false"}

If you want want to make a complete new plot delete the forces.cvs file
Hit <i>Crtl + C</i> for stopping the <i>Service_Log_Measurement_Data.py</i> and <i>Plot_Measurement_Data.py</i> and start them again.

## Update
Starting and Stopping plots can now be done with executing "<i>./plotForces.sh</i>" in the src folder. This also stops the background process (Service_Log_Measurement_Data.py). You just have enable the logging via any MQTT Explorer after jo run this script.