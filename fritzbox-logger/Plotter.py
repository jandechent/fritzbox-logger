# coding: utf-8
#!/usr/bin/env python3
"""
    FRITZ!Box SmartHome Plotter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import datetime 
import time
import matplotlib.pyplot as plt
import glob
import logging

plog = logging.getLogger(__name__)

class Plotter(object):
    def parseFile(self, filename):
        plog.debug("Parsing file" + filename)
        f = open(filename,'r')
        timestamp=[]
        temperature=[]
        with open(filename) as f:
            mylist = f.read().splitlines()
        for line in mylist:
            line=line.split(";")
            try:
                temperature.append(float(line[1]))
                timestamp.append(datetime.datetime.strptime(line[0],"%Y-%m-%d %H:%M:%S"))
            except ValueError:
                plog.debug(line[1]+ " seems not to be a valid temperature, skipping line")               
        return [timestamp,temperature]

    def __init__(self,**options):
        if options.get("plotnow")==True:
            self.plot(options)

    def plot(self,options):
        if options.get("filter") is None:
            filter="*"
        else:
            filter=options.get("filter")

        if options.get("title") is None:
            title="Temperature Plot"
        else:
            title=options.get("title")

        if options.get("blocking") is None:
            blocking=True
        else:
            blocking=options("blocking")
                    
        plog.debug("Start plotting")
        plog.debug("Filter=" + str(filter))

        for file in glob.glob("LOG_"+filter+".txt"):
            plog.debug("processing file:" +str(file))
            data=self.parseFile(file)
            plt.plot(data[0],data[1],'o--',label=file[4:-4])
        plt.ylabel('temperature [°]')
        plt.title(title)
        plt.legend(loc='upper left');
        plt.gcf().autofmt_xdate()
        plt.ylim(16,26)
        if options.get("timeWindowInH") is not None:
            plt.xlim(datetime.datetime.today()-datetime.timedelta(hours=options.get("timeWindowInH")),datetime.datetime.today())
        plog.debug("Showing plot")
        plt.show(block=blocking)
        plog.debug("Closing plot")

if __name__ == '__main__':
    Plotter(plotnow=True,timeWindowInH=8)
