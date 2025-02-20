import atexit
from . import Functions, Configs
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

#this is the class that handles all scheduling for lpr image mode cameras
class LprImageModeScheduler():
    
    def __init__(self):
                
        self.conf = Configs.LprImageModeConfig()
        
        if self.conf.isEnabled == "true":
            self.isEnabled = True
        else:
            self.isEnabled = False
        
        self.lprImageMode = Functions.LprImageMode()
        
        self.t1 = self.conf.t1
        self.t2 = self.conf.t2
        
        self.scheduler = BackgroundScheduler()
        
        self.t1List = self.t1.split(":")
        self.t2List = self.t2.split(":") 
    
        self.scheduler.add_job(self.turnOn, CronTrigger(hour=self.t1List[0], minute=self.t1List[1]), id="t1", misfire_grace_time=10)
        self.scheduler.add_job(self.turnOff, CronTrigger(hour=self.t2List[0], minute=self.t2List[1]), id="t2", misfire_grace_time=10) 
               
        self.scheduler.start()
        
        if self.isEnabled == False:
            
            self.scheduler.pause()
            
        atexit.register(self.shutdown)
        
    def setEnabled(self):
        
        if self.isEnabled == False:
            
            self.conf.setConfigSetting("isEnabled", "true")
            
            self.isEnabled = True
            
            self.scheduler.resume()
        else:
            print("already enabled")
        
    def setDisabled(self):
        
        if self.isEnabled:
        
            self.conf.setConfigSetting("isEnabled", "false")
            
            self.isEnabled = False
            
            self.scheduler.pause()            
        else:
            print("already disabled")
    
    def setScheduler(self, t1, t2):
                
        self.conf.setConfigSetting("executeTime1", t1)
        self.conf.setConfigSetting("executeTime2", t2)
        
        self.t1List = t1.split(":")
        
        self.t2List = t2.split(":") 
        
        self.scheduler.remove_job("t1")
        self.scheduler.remove_job("t2")
        
        self.scheduler.add_job(self.turnOn, CronTrigger(hour=self.t1List[0], minute=self.t1List[1]), id="t1", misfire_grace_time=10)
        self.scheduler.add_job(self.turnOff, CronTrigger(hour=self.t2List[0], minute=self.t2List[1]), id="t2", misfire_grace_time=10)
        
    def turnOn(self):
        
        self.lprImageMode.turnOnImageMode()
    
    def turnOff(self):
        
        self.lprImageMode.turnOffImageMode()
        
    def shutdown(self):
        
        self.scheduler.shutdown()

class RebootScheduler():
    
    def __init__(self):
                
        self.conf = Configs.RebootConfig()
        
        if self.conf.isEnabled == "true":
            self.isEnabled = True
        else:
            self.isEnabled = False
        
        self.reboot = Functions.Reboot()
        
        self.t1 = self.conf.t1
        
        self.scheduler = BackgroundScheduler()
        
        self.t1List = self.t1.split(":") 
    
        self.scheduler.add_job(self.startReboot, CronTrigger(hour=self.t1List[0], minute=self.t1List[1]), id="t1", misfire_grace_time=10) 
               
        self.scheduler.start()
        
        if self.isEnabled == False:
            
            self.scheduler.pause()
            
        atexit.register(self.shutdown)
        
    def setEnabled(self):
        
        if self.isEnabled == False:
            
            self.conf.setConfigSetting("isEnabled", "true")
            
            self.isEnabled = True
            
            self.scheduler.resume()
        else:
            print("already enabled")
        
    def setDisabled(self):
        
        if self.isEnabled:
        
            self.conf.setConfigSetting("isEnabled", "false")
            
            self.isEnabled = False
            
            self.scheduler.pause()            
        else:
            print("already disabled")
    
    def setScheduler(self, t1):
                
        self.conf.setConfigSetting("executeTime1", t1)
        
        self.t1List = t1.split(":")
                
        self.scheduler.remove_job("t1")
        
        self.scheduler.add_job(self.startReboot, CronTrigger(hour=self.t1List[0], minute=self.t1List[1]), id="t1", misfire_grace_time=10)
        
    def startReboot(self):
        
        self.reboot.rebootCamera()
        
        return
        
    def shutdown(self):
        
        self.scheduler.shutdown()
