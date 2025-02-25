from MainApp import lprImageModeTask, rebootTask
from django.shortcuts import HttpResponse, redirect
from . import views, Forms

""" Not using django forms
def setlprImageModeScheduler(request):
    if request.method == "POST":
        t1 = request.POST.get("t1")
        t2 = request.POST.get("t2")
        lprImageModeTask.sched.setScheduler(t1, t2)
    return views.alprImageModeTask(request)
"""

def setlprImageModeScheduler(request):
    if request.method == "POST":
        setSched = Forms.SetTwoSchedulerTimes(request.POST)
        if setSched.is_valid():
            t1 = str(setSched.cleaned_data["startTime1"])
            t2 = str(setSched.cleaned_data["startTime2"])
            lprImageModeTask.sched.setScheduler(t1, t2)
            
            return redirect("alprImageModeTask")
        else:
            return HttpResponse(f"{setSched.errors}")
        
    return redirect("alprImageModeTask")

def setRebootScheduler(request):
    if request.method == "POST":
        setSched = Forms.SetOneSchedulerTime(request.POST)
        if setSched.is_valid():
            t1 = str(setSched.cleaned_data["startTime"])
            
            rebootTask.sched.setScheduler(t1)
            
            return redirect("rebootCamTask")
        else:#shows errors if input is incorrect time format
            return HttpResponse(f"{setSched.errors}")
        
    return redirect("rebootCamTask")

def lprImageModeSchedulerIsEnabled(request):
    if request.method == "POST":
        isEnabled = Forms.IsEnabled(request.POST)
        if isEnabled.is_valid():
            check = isEnabled.cleaned_data["isEnabled"]
            if check:
                lprImageModeTask.sched.setEnabled()
            else:
                lprImageModeTask.sched.setDisabled()
                
    return redirect("alprImageModeTask")

def rebootSchedulerIsEnabled(request):
    if request.method == "POST":
        isEnabled = Forms.IsEnabled(request.POST)
        if isEnabled.is_valid():
            check = isEnabled.cleaned_data["isEnabled"]
            if check:
                rebootTask.sched.setEnabled()
            else:
                rebootTask.sched.setDisabled()
                
    return redirect("rebootCamTask")

def delete(request):
    if request.method == "POST":
        endPoint= request.POST.get("endPoint")
        action = request.POST.get("action")
        if action == "lprImageMode":
            lprImageModeTask.sched.lprImageMode.list.deleteEndPoint(endPoint)
            return views.alprImageModeTask(request)
        elif action == "reboot":
            rebootTask.sched.reboot.list.deleteEndPoint(endPoint)
            return views.rebootCamTask(request)
        else:
            return HttpResponse("No matching action")
    return HttpResponse("Error: POST required")

def edit(request):
    if request.method == "POST":
        endPoint= request.POST.get("endPoint")
        action = request.POST.get("action")
        editCamForm = Forms.CamDetails(request.POST)
        # you have to check that is_valid() first before you can use the variables
        if editCamForm.is_valid():
            endUrl= editCamForm.cleaned_data["endUrl"]
            endPort= editCamForm.cleaned_data["endPort"]
            endUser= editCamForm.cleaned_data["endUser"]
            endPass= editCamForm.cleaned_data["endPass"]
            if action == "lprImageMode": 
                lprImageModeTask.sched.lprImageMode.list.editEndPointList(endPoint, endUrl, endPort, endUser, endPass)
                return redirect("alprImageModeTask")
            elif action == "reboot":
                rebootTask.sched.reboot.list.editEndPointList(endPoint, endUrl, endPort, endUser, endPass)
                return redirect("rebootCamTask")
            else:
                return HttpResponse("Error: no matching action")
        else:
            return HttpResponse(f"form not Valid {editCamForm.errors}")
    return redirect("Error: required POST")

def add(request):
    # requests are seperated by action so as to utilize the same method for different requests
    if request.method == "POST":
        addCam = Forms.CamDetails(request.POST)
        action = request.POST.get("action")
        if addCam.is_valid():
            endUrl= addCam.cleaned_data["endUrl"]
            endPort= addCam.cleaned_data["endPort"]
            endUser= addCam.cleaned_data["endUser"]
            endPass= addCam.cleaned_data["endPass"]
            if action == "lprImageMode":
                lprImageModeTask.sched.lprImageMode.list.addToEndPointList(endUrl, endPort, endUser, endPass)
                return redirect("alprImageModeTask")
            elif action == "reboot":
                rebootTask.sched.reboot.list.addToEndPointList(endUrl, endPort, endUser, endPass)
                return redirect("rebootCamTask")
            else:
                return HttpResponse("Error: no matching action")
        else:
            return HttpResponse(f"Error: Form not valid {addCam.errors}")
    return HttpResponse("Error: POST required")

def verify(request):
    return redirect("home")

