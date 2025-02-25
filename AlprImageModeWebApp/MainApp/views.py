from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from MainApp import lprImageModeTask, rebootTask
from . import Forms

def home(request):
    
    return render(request, "home.html")
    
def login(request):
    
    return render(request, "login.html")
    
def alprImageModeTask(request):
    
    confState = lprImageModeTask.sched.conf.getConfIsEnabled()
    
    currentSched = lprImageModeTask.sched.conf.getConfSchedTime()
    
    setSchedule = Forms.SetTwoSchedulerTimes()
    
    # determines wether check box is set to true or false on server or page reload.
    if confState == "false":
        initialState = {"isEnabled": False}
    else:
        initialState = {"isEnabled": True}
    
    isEnabled = Forms.IsEnabled(initial=initialState)
    
    endPointList = lprImageModeTask.sched.lprImageMode.list.getEndpointList()
    
    # there cannot be a space between ":
    context = {"endPointList": endPointList, "setSchedule": setSchedule, "isEnabled": isEnabled, "currentSched": currentSched}
    
    return render(request, "lpr-image-mode-edit.html", context)

def editCamInfo(request):
    
    if request.method == "POST":
        endPoint = request.POST.get("endPoint")
        action = request.POST.get("action")
    
    partEndpoint = endPoint.split(":")
        
    initial_state = {"endUrl": partEndpoint[0], "endPort": partEndpoint[1], "endUser": partEndpoint[2], "endPass": partEndpoint[3]}
    
    editCamInfo = Forms.CamDetails(initial=initial_state)
    
    context = {"editCamInfo": editCamInfo, "endPoint": endPoint}
    
    if action == "lprImageMode":
        return render(request, "lpr-image-mode-cam-edit.html", context)
    
    elif action == "reboot":
        return render(request, "reboot-cam-edit.html", context)

def alprImageModeAddCam(request):
    
    initial_state = {"endUser": "admin", "endPass": "admin1200"}
    
    addCam = Forms.CamDetails(initial=initial_state)
    
    context = {"addCam": addCam}
    
    return render(request, "lpr-image-mode-cam-add.html", context)


def rebootAddCam(request):
    
    initial_state = {"endUser": "admin", "endPass": "admin1200"}
    
    addCam = Forms.CamDetails(initial=initial_state)
    
    context = {"addCam": addCam}
    
    return render(request, "reboot-cam-add.html", context)


def rebootCamTask(request):
    
    confState = rebootTask.sched.conf.getConfIsEnabled()
    
    rebootTime = rebootTask.sched.conf.getConfSchedTime()
    
    setSchedule = Forms.SetOneSchedulerTime()
    
    # determines wether check box is set to true or false on server or page reload.
    if confState == "false":
        initialState = {"isEnabled": False}
    else:
        initialState = {"isEnabled": True}
    
    isEnabled = Forms.IsEnabled(initial=initialState)
    
    endPointList = rebootTask.sched.reboot.list.getEndpointList()
    
    # there cannot be a space between ":
    context = {"endPointList": endPointList, "setSchedule": setSchedule, "isEnabled": isEnabled, "rebootTime": rebootTime}
        
    return render(request, "reboot-edit.html", context)