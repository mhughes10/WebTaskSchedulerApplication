from django.urls import path
from . import views, Main

urlpatterns = [
    path("", views.login, name="login"),
    path("home/", views.home, name="home"),
    path("setlprImageModeScheduler/", Main.setlprImageModeScheduler, name="setlprImageModeScheduler"),
    path("setRebootScheduler/", Main.setRebootScheduler, name="setRebootScheduler"),
    path("alprImageModeTask/", views.alprImageModeTask, name="alprImageModeTask"),
    path("rebootCamTask/", views.rebootCamTask, name="rebootCamTask"),
    path("editCamInfo/", views.editCamInfo, name="editCamInfo"),
    path("alprImageModeAddCam/", views.alprImageModeAddCam, name="alprImageModeAddCam"),
    path("rebootAddCam/", views.rebootAddCam, name="rebootAddCam"),
    path("lprImageModeSchedulerIsEnabled/", Main.lprImageModeSchedulerIsEnabled, name="lprImageModeSchedulerIsEnabled"),
    path("rebootSchedulerIsEnabled/", Main.rebootSchedulerIsEnabled, name="rebootSchedulerIsEnabled"),
    path("delete/", Main.delete, name="delete"),
    path("edit/", Main.edit, name="edit"),
    path("add/", Main.add, name="add"),
    path("verify", Main.verify, name="verify"),
]