import logging, configparser

class LprImageModeConfig():
    
    def __init__(self):
        
        self.configFilePath = "C:\System Administrator\AutomatedWebTasks\AlprImageMode\AlprImageMode_Config\LprImageMode.ini"
        
        self.config = configparser.ConfigParser()
        
        self.config.read(self.configFilePath)
        
        self.t1 = self.config["settings"]["executeTime1"]
        self.t2 = self.config["settings"]["executeTime2"]
        self.isEnabled = self.config["settings"]["isEnabled"]
        self.csvListFilePath = self.config["settings"]["csvListFilePath"] 
        self.failedEnableListFilePath = self.config["settings"]["failedEnableListfilepath"]
        self.failedDisableListFilePath = self.config["settings"]["failedDisableListfilepath"]       
        
        # this is to change settings in the config file
    def setConfigSetting(self, setting, value):
        
        self.config.read(self.configFilePath)
        
        self.config["settings"][f"{setting}"] = value
        
        configFile = open(self.configFilePath, "w")
        
        self.config.write(configFile)
        
        configFile.close()
        
    def getConfIsEnabled(self):
        self.config.read(self.configFilePath)
        self.isEnabled = self.config["settings"]["isEnabled"]
        return self.isEnabled
    
    def getConfSchedTime(self):
        
        self.uT1 = self.config["settings"]["executetime1"]
        self.uT2 = self.config["settings"]["executetime2"]
        
        return f"Enable at: [{self.uT1}] | Disable at: [{self.uT2}]"

class RebootConfig():
    
    def __init__(self):
        
        self.configFilePath = "C:\System Administrator\AutomatedWebTasks\Reboot\Reboot_Config\Reboot.ini"
        
        self.config = configparser.ConfigParser()
        
        self.config.read(self.configFilePath)
        
        self.t1 = self.config["settings"]["executeTime1"]
        self.isEnabled = self.config["settings"]["isEnabled"]
        self.csvListFilePath = self.config["settings"]["csvListFilePath"]
        self.failedListFilePath = self.config["settings"]["failedListFilePath"]
        
        # this is to change settings in the config file
    def setConfigSetting(self, setting, value):
        
        self.config.read(self.configFilePath)
        
        self.config["settings"][f"{setting}"] = value
        
        configFile = open(self.configFilePath, "w")
        
        self.config.write(configFile)
        
        configFile.close()
        
    def getConfIsEnabled(self):
        self.config.read(self.configFilePath)
        self.isEnabled = self.config["settings"]["isEnabled"]
        return self.isEnabled
    
    def getConfSchedTime(self):
        
        self.uT1 = self.config["settings"]["executetime1"]
        
        return f"Reboot at: [{self.uT1}]"