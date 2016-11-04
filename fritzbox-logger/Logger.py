# coding: utf-8
#!/usr/bin/env python3
"""
    FRITZ!Box SmartHome Logger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from fritzhome import fritz
from threading import Thread
import datetime 
import time
import glob
import signal
import logging

plog = logging.getLogger(__name__)

class Logger(fritz.FritzBox,Thread):
    def __init__(self, ip, username, password, **options):
        # define the delay in seconds that is added between two queries to the fritz.box
        self.delayInSeconds = 5*60 if options.get("delayInSeconds") is None else options.get("delayInSeconds")
        
        # how many requests shall be done? -1 is infinite number. 
        self.numberOfRepeats= -1 if options.get("numberOfRepeats") is None else options.get("numberOfRepeats")    
        plog.debug("numberOfRepeats=" + str(self.numberOfRepeats))

        use_tls = options.get("use_tls")

        # Invoke the FritzBox super class to log in the box
        super().__init__(ip, username, password, use_tls)
        # Invoke the Thread init function. 
        Thread.__init__(self)
        self.goon=False

        # register control+c handler to abort the thread. 
        def signal_handler(signal, frame):
            plog.warn('You pressed Ctrl+C, stopping FritzLogger')
            self.stop()    
        signal.signal(signal.SIGINT, signal_handler)
            
    def run(self,delay=1):
        self.goon=True # The thread shall run as requested
        plog.warn("Control+C aborts the logging thread.")
        plog.debug("delay  =" + str(self.delayInSeconds))
        i=0
        starttime_Timer=0
        endtime_Timer=0
        timeToWait=0
        while (i!=self.numberOfRepeats):
            starttime_Logger = time.time()
            plog.debug("Repetition: " + str(i+1) + "/" + str(self.numberOfRepeats))
            super().login()
            allactors=super().get_actors()
            for actor in allactors:
                with open("LOG_" + actor.name+".txt", "a") as myfile:
                    myfile.write(time.strftime("%Y-%m-%d %H:%M:%S")+";"+str(actor.get_temperature())+"\n")
                plog.info(str(actor.get_temperature())+" [°C] @ " + actor.name)
            if self.goon==False:
                    plog.warn("Closing Thread")
                    return
            i=i+1;
            endtime_Logger = time.time()
            elapsedTime_Logger=int(endtime_Logger-starttime_Logger)
            plog.debug("elapsedTime_Logger " + str(elapsedTime_Logger))
            timeToWait=(self.delayInSeconds-elapsedTime_Logger)
            if timeToWait<0:
                timeToWait=0
                plog.warning("Requested delay ("+str(self.delayInSeconds)+"s) too short, logging took "+str(elapsedTime_Logger)+"s. Start next logging cycle directly...")
            elif timeToWait==0:
                plog.info("Start next logging cycle directly...")
            else:
                plog.info("Logging took "+str(elapsedTime_Logger)+"s. Waiting for "+str(timeToWait)+"s ...")
                while (endtime_Timer-endtime_Logger)<timeToWait:
                    time.sleep(1)
                    if self.goon==False:
                        plog.warn("Closing Thread")
                        return
                    endtime_Timer = time.time()
        plog.debug("Fritzlogger loop finished.")

    def stop(self):
        self.goon=False

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)
    plog.setLevel(logging.INFO)
    f=Logger("fritz.box", "smarthome","smarthome",delayInSeconds=15, numberOfRepeats=2)
    f.run()

    
