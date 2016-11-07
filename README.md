# fritzbox-logger
Intended for logging and plotting temperature from all actors connected to one fritzbox.
Tested with:
* FRITZ!Box 7490 
* FRITZ!DECT 200 (1x)
* Comet DECT Heizkörperthermostat (4x)

# How to use
The following code from the main.py starts logging the temperature every 15 minutes and plots this over time:
```
from Plotter import Plotter
from Logger import Logger

f=Logger("fritz.box", "smarthome","smarthome",delayInSeconds=15*60)
f.start();

while f.isAlive():
    p=Plotter(plotnow=True,timeWindowInH=8)
```

The components of the module are:
* fritzbox-logger/Logger.py is responsible for logging. The thread generates one file per actor (LOG_*name*.txt)
* fritzbox-logger/Plotter.py is responsible for plotting the temperature over time (LOG_*.txt). 

PS: Ideally the user *smarthome* with password *smarthome* has only accessrights to the smart home parts of the fritzbox.  

# Dependencies
Please pip-install the module: https://github.com/DerMitch/fritzbox-smarthome
