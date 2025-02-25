import threading, ping3, socket, requests, logging, time
from . import Lists
from requests.auth import HTTPDigestAuth
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from onvif import ONVIFCamera

#This is the lpr image mode main logic for running the task
class LprImageMode():
    def __init__(self):
        self.list = Lists.LprImageModeList()
        self.logger = logging.getLogger("lprImageMode")
        self.session = requests.Session()
        self.retriesEnable = []
        self.retriesDisable = []
        self.failedEnable = []
        self.failedDisable = []
    
    #creates individual threads from the partitioned list of x cams per each thread and calls turnOFF method
    def turnOffImageMode(self):
        self.partEndpointList = self.list.getPartEndPointList()
        threads = []
        for part in self.partEndpointList:
            thread = threading.Thread(target=self.turnOff, args=(part,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        if self.retriesDisable != []:
            
            print("Retrying:")
            print(self.retriesDisable)
            self.turnOffImageModeRetries(self.retriesDisable)
            self.retriesDisable = []
            
        else:
            print("Retries: None")
                
        if self.failedDisable != []:
            
            print("Failed to disable:")
            print(self.failedDisable)
            self.list.addToFailedEndPointLists(None, self.failedDisable)
            self.failedDisable = []
            
        else:
            # intended to clear list of old entries
            self.list.addToFailedEndPointLists(self.failedDisable, None)
       
    def turnOnImageMode(self):
        self.partEndpointList = self.list.getPartEndPointList()
        threads = []
        for part in self.partEndpointList:
            thread = threading.Thread(target=self.turnOn, args=(part,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
            
        if self.retriesEnable != []:
            print("Retrying:") 
            print(self.retriesEnable) 
            self.turnOnImageModeRetries(self.retriesEnable)
            self.retriesEnable = []
        else:
            print("Retries: None")
                
        if self.failedEnable != []:
            print("Failed to enable:")
            print(self.failedEnable)
            self.list.addToFailedEndPointLists(self.failedEnable, None)
            self.failedEnable = []
        
        else:
            # intended to clear list of old entries
            self.list.addToFailedEndPointLists(self.failedEnable, None)
    
    #starts new threads to handle retries      
    def turnOnImageModeRetries(self, retries):
    
        self.partRetries = Lists.divideAndConquer(retries)
    
        threadRetriesL = []
        
        for element in self.partRetries:
            threadRetries = threading.Thread(target=self.turnOnRetry, args=(element,))
            threadRetriesL.append(threadRetries)
            threadRetries.start()
            
        for thread in threadRetriesL:
            thread.join()
    
    def turnOffImageModeRetries(self, retries):
                
        self.partRetries = Lists.divideAndConquer(retries)
        
        threadRetriesL = []
        
        for element in self.partRetries:
            threadRetries = threading.Thread(target=self.turnOffRetry, args=(element,))
            threadRetriesL.append(threadRetries)
            threadRetries.start()
            
        for thread in threadRetriesL:
            thread.join()
            
    
    def turnOff(self, part):
        for element in part:
            
            conDetail = [item.strip('"') for item in element.split(":")]
            
            camIp = conDetail[0]
            camPort = int(conDetail[1])            
            camUserN = conDetail[2]
            camPass = conDetail[3]
            
            #if self.pingCamera(camIp, camPort):
            
            try:
            
                #grab request url by inspecting page and watching for operator actions
                requestUrl = f"http://{camIp}:{camPort}/cgi-bin/operator/operator.cgi?action=set.lpr.settings&format=json"
                
                # must be in json format
                jsonPayload = {"nightModeEnable": 0}
                
                #post the changes set retry time out to 2 seconds
                response = requests.post(requestUrl, json=jsonPayload, auth=HTTPDigestAuth(f"{camUserN}", f"{camPass}"), headers={"Content-Type": "application/json"}, timeout=5)
                response.raise_for_status()
                
                if response.status_code == 200:
                    print(f"{conDetail} lpr image mode successfully disabled")
                else:
                    print(f"UNEXPECTED RESPONSE FOR: ({conDetail}) status code is {response.status_code}")
                    self.logger.error(f"UNEXPECTED RESPONSE FOR: ({conDetail}) status code is {response.status_code}")
                    
            except requests.exceptions.RequestException:
                
                self.retriesDisable.append(element)
                
        #figure out how to connect to the camera uncheck setting, save, then close connection
    
    def turnOn(self, part):
        for element in part:
            
            conDetail = [item.strip('"') for item in element.split(":")]
            
            camIp = conDetail[0]
            camPort = int(conDetail[1])            
            camUserN = conDetail[2]
            camPass = conDetail[3]
            
            #pings camera 5 sec timeout before attempting to connect 
            #if self.pingCamera(camIp, camPort):
            
            try:
            
                #grab request url by inspecting page and watching for operator actions
                requestUrl = f"http://{camIp}:{camPort}/cgi-bin/operator/operator.cgi?action=set.lpr.settings&format=json"
                
                # must be in json format
                jsonPayload = {"nightModeEnable": 1}
                
                #post the changes
                response = requests.post(requestUrl, json=jsonPayload, auth=HTTPDigestAuth(f"{camUserN}", f"{camPass}"), headers={"Content-Type": "application/json"}, timeout=5)
                
                response.raise_for_status()
                
                if response.status_code == 200:
                    
                    print(f"{conDetail} lpr image mode successfully enabled")
                    
                else:
                    
                    print(f"UNEXPECTED RESPONSE FOR: ({conDetail}) status code is {response.status_code}")
                    self.logger.error(f"UNEXPECTED RESPONSE FOR: ({conDetail}) status code is {response.status_code}")
                    
            except requests.exceptions.RequestException:
                
                self.retriesEnable.append(element)
                
        #figure out how to connect to the camera check setting, save, then close connection
        
    def pingCamera(self, camIp, camPort):
        connStat = True
        # returns None if ping has no response
        response = ping3.ping(camIp, timeout=5)
        if response == False:
            response = ping3.ping(camIp, timeout=5)
            if response == None:
                connStat = False
                self.logger.error(f"{camIp} is not reachable! (Timeout)")
            elif response == False:
                connStat = False
                self.logger.error(f"{camIp} is not reachable! (Immediate Failure)")
        elif response == None:
            connStat = False
            self.logger.error(f"{camIp} is not reachable! (Timeout)")
            
        if connStat is not False:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((camIp, camPort))
            if result != 0:
                connStat = False
                sock.close()
                self.logger.error(f"{camIp} port {camPort} is not open or is incorrect!")
            sock.close()
        return connStat
        
    def rebootCamera(self, camIp, camPort):
        xaddr = f"http://{camIp}:{camPort}/onvif/device_service"
        rebootSoap = """<?xml version="1.0" encoding="utf-8"?>
        <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope">
            <s:Body>
                <SystemReboot xmlns="http://www.onvif.org/ver10/device/wsdl"/>
            </s:Body>
        </s:Envelope>"""
        response = requests.post(xaddr, data=rebootSoap, auth=HTTPDigestAuth("admin", "admin1200"), headers={'Content-Type': 'application/soap+xml'})
        if response.status_code == 200:
            print("camera is rebooting")
        else:
            print(f"Failed to reboot the camera. Status code: {response.status_code}")
            
    def getCamCapabilaties(self, camIp,CamPort):
        cam = ONVIFCamera(camIp, CamPort, "admin", "admin1200")
        capabilities = cam.devicemgmt.GetCapabilities
        return print(capabilities)
    
    def turnOffRetry(self, part):
        
        for element in part:
        
            conDetail = element.split(":")
            
            camIp = conDetail[0]
            camPort = int(conDetail[1])
            camUserN = conDetail[2]
            camPass = conDetail[3]
        
            #if self.pingCamera(camIp, camPort):
            
            self.retries = Retry(total=3, backoff_factor=0.1, raise_on_status=False, status_forcelist=[500, 502, 503, 504])
            self.adapter = HTTPAdapter(max_retries=self.retries)
            self.session.mount("http://", self.adapter)
            self.session.mount("https://", self.adapter)
            
            try:
            
                #grab request url by inspecting page and watching for operator actions
                requestUrl = f"http://{camIp}:{camPort}/cgi-bin/operator/operator.cgi?action=set.lpr.settings&format=json"
                
                # must be in json format
                jsonPayload = {"nightModeEnable": 0}
                
                #post the changes set retry time out to 2 seconds
                response = self.session.post(requestUrl, json=jsonPayload, auth=HTTPDigestAuth(f"{camUserN}", f"{camPass}"), headers={"Content-Type": "application/json"}, timeout=5)
                response.raise_for_status()
                
                if response.status_code == 200:
                    print(f"{conDetail} lpr image mode successfully disabled")
                else:
                    print(f"UNEXPECTED RESPONSE FOR: ({conDetail}) status code is {response.status_code}")
                    self.logger.error(f"UNEXPECTED RESPONSE FOR: ({conDetail}) status code is {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                self.logger.error(f"{conDetail}: {e}")
                self.failedDisable.append(element)
                
        #figure out how to connect to the camera uncheck setting, save, then close connection
    
    def turnOnRetry(self, part):
        
        for element in part:
            
            conDetail = element.split(":")
            
            camIp = conDetail[0]
            camPort = int(conDetail[1])            
            camUserN = conDetail[2]
            camPass = conDetail[3]
            
            #pings camera 5 sec timeout before attempting to connect 
            #if self.pingCamera(camIp, camPort):
                            
            self.retries = Retry(total=3, backoff_factor=0.1, raise_on_status=False, status_forcelist=[500, 502, 503, 504])
            self.adapter = HTTPAdapter(max_retries=self.retries)
            self.session.mount("http://", self.adapter)
            self.session.mount("https://", self.adapter)
            
            try:
            
                #grab request url by inspecting page and watching for operator actions
                requestUrl = f"http://{camIp}:{camPort}/cgi-bin/operator/operator.cgi?action=set.lpr.settings&format=json"
                
                # must be in json format
                jsonPayload = {"nightModeEnable": 1}
                
                #post the changes
                response = self.session.post(requestUrl, json=jsonPayload, auth=HTTPDigestAuth(f"{camUserN}", f"{camPass}"), headers={"Content-Type": "application/json"}, timeout=5)
                
                response.raise_for_status()
                
                if response.status_code == 200:
                    print(f"{conDetail} lpr image mode successfully enabled")
                else:
                    print(f"UNEXPECTED RESPONSE FOR: ({conDetail}) status code is {response.status_code}")
                    self.logger.error(f"UNEXPECTED RESPONSE FOR: ({conDetail}) status code is {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                self.logger.error(f"{conDetail}: {e}")
                self.failedEnable.append(element)
                
        #figure out how to connect to the camera check setting, save, then close connection
class Reboot():
    def __init__(self):
        self.list = Lists.RebootList()
        self.logger = logging.getLogger("Reboot")
        self.session = requests.Session()
        self.retries = []
        self.failedReboot = []
    
    #creates individual threads from the partitioned list of x cams per each thread and calls turnOFF method
       
    def rebootCamera(self):
        self.partEndpointList = self.list.getPartEndPointList()
        threads = []
        for part in self.partEndpointList:
            thread = threading.Thread(target=self.reboot, args=(part,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
            
        if self.retries:
            print("Retrying:")
            self.rebootCameraRetries(self.retries)
            self.retries = []
        
        if self.failedReboot:
            print("Failed to reboot:")
            print(self.failedReboot)
            self.list.addToFailedEndPointList(self.failedReboot)
            self.failedReboot = []
    
    #starts new threads to handle retries      
    def rebootCameraRetries(self, retries):
        
        print(retries)
    
        self.partRetries = Lists.divideAndConquer(retries)
    
        threadRetriesL = []
        
        for element in self.partRetries:
            threadRetries = threading.Thread(target=self.rebootRetry, args=(element,))
            threadRetriesL.append(threadRetries)
            threadRetries.start()
            
        for thread in threadRetriesL:
            thread.join()
    
    def reboot(self, part):
        for element in part:
            
            conDetail = [item.strip('"') for item in element.split(":")]
            
            camIp = conDetail[0]
            camPort = int(conDetail[1])            
            camUserN = conDetail[2]
            camPass = conDetail[3]
            
            #pings camera 5 sec timeout before attempting to connect 
            #if self.pingCamera(camIp, camPort):
            
            try:
            
                #grab request url by inspecting page and watching for operator actions
                requestUrl = f"http://{camIp}:{camPort}/cgi-bin/admin/admin.cgi?action=reboot.system.maintenance&format=json"
                
                #post the changes
                response = requests.post(requestUrl, auth=HTTPDigestAuth(f"{camUserN}", f"{camPass}"), headers={"Content-Type": "application/json"}, timeout=5)
                
                response.raise_for_status()
                
                if response.status_code == 200:
                    
                    print(f"{conDetail} successfully rebooted")
                    
                else:
                    print(f"UNEXPECTED RESPONSE FOR: ({conDetail}) status code is {response.status_code}")
                    self.logger.error(f"UNEXPECTED RESPONSE FOR: ({conDetail}) status code is {response.status_code}")
                    
            except requests.exceptions.RequestException:
                
                self.retries.append(element)
                
        #figure out how to connect to the camera check setting, save, then close connection
        
    def pingCamera(self, camIp, camPort):
        connStat = True
        # returns None if ping has no response
        response = ping3.ping(camIp, timeout=5)
        if response == False:
            response = ping3.ping(camIp, timeout=5)
            if response == None:
                connStat = False
                self.logger.error(f"{camIp} is not reachable! (Timeout)")
            elif response == False:
                connStat = False
                self.logger.error(f"{camIp} is not reachable! (Immediate Failure)")
        elif response == None:
            connStat = False
            self.logger.error(f"{camIp} is not reachable! (Timeout)")
            
        if connStat is not False:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((camIp, camPort))
            if result != 0:
                connStat = False
                sock.close()
                self.logger.error(f"{camIp} port {camPort} is not open or is incorrect!")
            sock.close()
        return connStat
        
    def rebootCameraXaddr(self, camIp, camPort):
        xaddr = f"http://{camIp}:{camPort}/onvif/device_service"
        rebootSoap = """<?xml version="1.0" encoding="utf-8"?>
        <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope">
            <s:Body>
                <SystemReboot xmlns="http://www.onvif.org/ver10/device/wsdl"/>
            </s:Body>
        </s:Envelope>"""
        response = requests.post(xaddr, data=rebootSoap, auth=HTTPDigestAuth("admin", "admin1200"), headers={'Content-Type': 'application/soap+xml'})
        if response.status_code == 200:
            print("camera is rebooting")
        else:
            print(f"Failed to reboot the camera. Status code: {response.status_code}")
            
    def getCamCapabilaties(self, camIp,CamPort):
        cam = ONVIFCamera(camIp, CamPort, "admin", "admin1200")
        capabilities = cam.devicemgmt.GetCapabilities
        return print(capabilities)
    
    def rebootRetry(self, part):
        
        for element in part:
            
            conDetail = element.split(":")
            
            camIp = conDetail[0]
            camPort = int(conDetail[1])
            camUserN = conDetail[2]
            camPass = conDetail[3]
            
            #pings camera 5 sec timeout before attempting to connect 
            #if self.pingCamera(camIp, camPort):
                            
            self.retries = Retry(total=5, backoff_factor=0.1, raise_on_status=False, status_forcelist=[500, 502, 503, 504])
            self.adapter = HTTPAdapter(max_retries=self.retries)
            self.session.mount("http://", self.adapter)
            self.session.mount("https://", self.adapter)
            
            try:
            
                #grab request url by inspecting page and watching for operator actions
                requestUrl = f"http://{camIp}:{camPort}/cgi-bin/admin/admin.cgi?action=reboot.system.maintenance&format=json"
                
                #post the changes
                response = self.session.post(requestUrl, auth=HTTPDigestAuth(f"{camUserN}", f"{camPass}"), headers={"Content-Type": "application/json"}, timeout=5)
                
                response.raise_for_status()
                
                if response.status_code == 200:
                    print(f"{conDetail} successfully rebooted")
                else:
                    print(f"UNEXPECTED RESPONSE FOR: ({conDetail}) status code is {response.status_code}")
                    self.logger.error(f"UNEXPECTED RESPONSE FOR: ({conDetail}) status code is {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                self.logger.error(f"{conDetail}: {e}")
                self.failedReboot.append(element)
                
        #figure out how to connect to the camera check setting, save, then close connection
        
        
        