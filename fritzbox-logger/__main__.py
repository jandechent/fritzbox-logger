# coding: utf-8
"""
    FRITZ!Box SmartHome Logger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import logging
logging.basicConfig(level=logging.WARN)

from Plotter import Plotter
from Logger import Logger

f=Logger("fritz.box", "smarthome","smarthome",delayInSeconds=15*60)
f.start();

while f.isAlive():
    p=Plotter(plotnow=True,timeWindowInH=8)
