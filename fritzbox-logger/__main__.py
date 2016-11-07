# coding: utf-8
"""
    FRITZ!Box SmartHome Logger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import logging

from Plotter import Plotter
from Logger import Logger

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)
    logging.getLogger("Logger").setLevel(logging.INFO)

    f=Logger("fritz.box", "smarthome","smarthome",delayInSeconds=15*60)
    f.start();

    while f.isAlive():
        p=Plotter(plotnow=True,timeWindowInH=8)
