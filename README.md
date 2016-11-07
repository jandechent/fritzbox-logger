# fritzbox-logger
Intended for logging and plotting temperature from all actors connected to one fritzbox.
Tested with:
* FRITZ!Box 7490 
* FRITZ!DECT 200 (1x)
* Comet DECT Heizkörperthermostat (4x)

# How to use
Execute fritzbox-logger/Logger.py to start logging. The thread generates one file per actor (LOG_*name*.txt)

Execute fritzbox-logger/Plotter.py to plot the temperature over time (LOG_*.txt). 

PS: When not supplying credentials or server, the script attempts to connect to the adress *fritz.box* with the username *smarthome* and password *smarthome*. 

# Dependencies
Please pip-install the module: https://github.com/DerMitch/fritzbox-smarthome
