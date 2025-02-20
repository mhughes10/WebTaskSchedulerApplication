from . import Configs
import csv

#this is the class that manages the list given to to the task
class LprImageModeList():
    def __init__(self):
        
        self.conf = Configs.LprImageModeConfig()
        
        self.csvFilePath = self.conf.csvListFilePath
        
        self.failedEnableListFilePath = self.conf.failedEnableListFilePath
        self.failedDisableListFilePath = self.conf.failedDisableListFilePath
        
        # Read file containing end points separated by spaces.
        self.endpointFile = open(self.csvFilePath, "r")
        
        self.fileContents = self.endpointFile.read()
        
        # save to a list separated by spaces.
        self.endpointList = self.fileContents.split()
        
        self.endpointFile.close()
        
        # uses recursion to split the list into smaller chunks for processing.
        
        """ For testing divide and conquer function
        testList = list(range(1, 230))
        """
        
        # essentially creates a list of lists
        self.partEndpointList = divideAndConquer(self.endpointList)
        
        """ For testing divide and conquer function
        for part in partEndpointList:
            print(part)
        """
        
    def getEndpointList(self):
        
        self.endpointFile = open(self.csvFilePath, "r")
    
        self.fileContents = self.endpointFile.read()
        
        # save to a list separated by spaces.
        self.endpointList = self.fileContents.split()
        
        self.endpointFile.close()
        
        return self.endpointList
    
    def getPartEndPointList(self):
        
        self.endpointFile = open(self.csvFilePath, "r")
        
        self.fileContents = self.endpointFile.read()
        
        # save to a list separated by spaces.
        self.endpointList = self.fileContents.split()
        
        self.endpointFile.close()
        
        # uses recursion to split the list into smaller chunks for processing.
        
        """ For testing divide and conquer function
        testList = list(range(1, 230))
        """
        
        # essentially creates a list of lists
        self.partEndpointList = divideAndConquer(self.endpointList)
        
        return self.partEndpointList
    
    def deleteEndPoint(self, endPoint):
        
        with open(self.csvFilePath, mode="r", newline="") as file:
            reader = csv.reader(file)
            rows = [row for row in reader if endPoint not in row]
        
        with open(self.csvFilePath, mode="w", newline="") as file:
            writer = csv.writer(file)
            for row in rows:
                writer.writerow(row)
                
    def editEndPointList(self, endPoint, endUrl, endPort, endUser, endPass):
        
        updatedEndPoint = ":".join([str(endUrl), str(endPort), str(endUser), str(endPass)])
                
        with open(self.csvFilePath, mode="r", newline="") as file:
            reader = csv.reader(file)
            rows = [row for row in reader if endPoint not in row]
                        
            rows.append([updatedEndPoint])
                        
        with open(self.csvFilePath, mode="w", newline="") as file:
            writer = csv.writer(file)
            for row in rows:
                writer.writerow(row)
    
    def addToEndPointList(self, endUrl, endPort, endUser, endPass):
        
        updatedEndPoint = ":".join([str(endUrl), str(endPort), str(endUser), str(endPass)])
        
        with open(self.csvFilePath, mode="r", newline="") as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
            
            rows.append([updatedEndPoint])
            
        with open(self.csvFilePath, mode="w", newline="") as file:
            writer = csv.writer(file)
            for row in rows:
                writer.writerow(row)
                
    def addToFailedEndPointLists(self, failedEnableList, failedDisableList):
        
        if failedDisableList != None:
            with open(self.failedDisableListFilePath, mode="w", newline="") as file:
                writer = csv.writer(file)
                for row in failedDisableList:
                    writer.writerow([row])
                
        if failedEnableList != None:
            with open(self.failedEnableListFilePath, mode="w", newline="") as file:
                writer = csv.writer(file)
                for row in failedEnableList:
                    writer.writerow([row])

class RebootList():
    def __init__(self):
        
        self.conf = Configs.RebootConfig()
        
        self.csvFilePath = self.conf.csvListFilePath
        
        self.failedListFilePath = self.conf.failedListFilePath
        
        # Read file containing end points separated by spaces.
        self.endpointFile = open(self.csvFilePath, "r")
        
        self.fileContents = self.endpointFile.read()
        
        # save to a list separated by spaces.
        self.endpointList = self.fileContents.split()
        
        self.endpointFile.close()
        
        # uses recursion to split the list into smaller chunks for processing.
        
        """ For testing divide and conquer function
        testList = list(range(1, 230))
        """
        
        # essentially creates a list of lists
        self.partEndpointList = divideAndConquer(self.endpointList)
        
        """ For testing divide and conquer function
        for part in partEndpointList:
            print(part)
        """
        
    def getEndpointList(self):
        
        self.endpointFile = open(self.csvFilePath, "r")
    
        self.fileContents = self.endpointFile.read()
        
        # save to a list separated by spaces.
        self.endpointList = self.fileContents.split()
        
        self.endpointFile.close()
        
        return self.endpointList
    
    def getPartEndPointList(self):
        
        self.endpointFile = open(self.csvFilePath, "r")
        
        self.fileContents = self.endpointFile.read()
        
        # save to a list separated by spaces.
        self.endpointList = self.fileContents.split()
        
        self.endpointFile.close()
        
        # uses recursion to split the list into smaller chunks for processing.
        
        """ For testing divide and conquer function
        testList = list(range(1, 230))
        """
        
        # essentially creates a list of lists
        self.partEndpointList = divideAndConquer(self.endpointList)
        
        return self.partEndpointList
    
    def deleteEndPoint(self, endPoint):
        
        with open(self.csvFilePath, mode="r", newline="") as file:
            reader = csv.reader(file)
            rows = [row for row in reader if endPoint not in row]
        
        with open(self.csvFilePath, mode="w", newline="") as file:
            writer = csv.writer(file)
            for row in rows:
                writer.writerow(row)
                
    def editEndPointList(self, endPoint, endUrl, endPort, endUser, endPass):
        
        updatedEndPoint = ":".join([str(endUrl), str(endPort), str(endUser), str(endPass)])
                
        with open(self.csvFilePath, mode="r", newline="") as file:
            reader = csv.reader(file)
            rows = [row for row in reader if endPoint not in row]
                        
            rows.append([updatedEndPoint])
                        
        with open(self.csvFilePath, mode="w", newline="") as file:
            writer = csv.writer(file)
            for row in rows:
                writer.writerow(row)
    
    def addToEndPointList(self, endUrl, endPort, endUser, endPass):
        
        updatedEndPoint = ":".join([str(endUrl), str(endPort), str(endUser), str(endPass)])
        
        with open(self.csvFilePath, mode="r", newline="") as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
            
            rows.append([updatedEndPoint])
            
        with open(self.csvFilePath, mode="w", newline="") as file:
            writer = csv.writer(file)
            for row in rows:
                writer.writerow(row)

    def addToFailedEndPointList(self, failedList):
                
        with open(self.failedListFilePath, mode="w", newline="") as file:
            writer = csv.writer(file)
            for row in failedList:
                writer.writerow([row])
        
def divideAndConquer(endpointList):
    
            if len(endpointList) <= 50:
                # if the list is less than 50 return the list wrapped in a list format
                return [endpointList]
            # this is where the function calls itself like a loop and returns a chunk to be stored in a separate list
            return [endpointList[:50]] + divideAndConquer(endpointList[50:])
        
        