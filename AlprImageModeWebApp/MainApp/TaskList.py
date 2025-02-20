from . import Schedulers

#this will hold different classes that will be created at server startup.

class LprImageMode():
    
    def __init__(self):
        
        self.sched = Schedulers.LprImageModeScheduler()
        
class Reboot():
    
    def __init__(self):
        
        self.sched = Schedulers.RebootScheduler()