import re
from django import forms
from django.core.exceptions import ValidationError

def validateIp(ip): #          or          or       ("?" allows 2-9 or 10-99)
                   #250-255  200-249     100-199       10-99    2-9   0-1 (.) repeat...
    ipPattern = r'^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[2-9]|[01])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[2-9]|[01])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[2-9]|[01])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[2-9]|[01])$'
    domainPattern = r'^(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,6}$'
    
    if not (re.match(ipPattern, ip) or re.match(domainPattern, ip)):                                                                                    
        raise ValidationError("Please enter Ip in the required format (25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[2-9]|[01])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[2-9]|[01])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[2-9]|[01])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[2-9]|[01])")
    
def validateParseCorrectFormat(credential):
    
    if credential.find(":") > -1:
        raise ValidationError('":" is an Invalid character')
    
class SetTwoSchedulerTimes(forms.Form):
    startTime1 = forms.TimeField(label="Enable Time", input_formats=['%H:%M'], error_messages={'invalid': 'Invalid format'}, widget=forms.TimeInput(attrs={'type': 'time'}))
    startTime2 = forms.TimeField(label="Disable Time", input_formats=['%H:%M'], error_messages={'invalid': 'Invalid format'}, widget=forms.TimeInput(attrs={'type': 'time'}))
    
class SetOneSchedulerTime(forms.Form):
    startTime = forms.TimeField(label="Start Time", input_formats=['%H:%M'], error_messages={'invalid': 'Invalid format'}, widget=forms.TimeInput(attrs={'type': 'time'}))
    
class IsEnabled(forms.Form):
    isEnabled = forms.BooleanField(label="Scheduler Enabled", required = False)
    
class CamDetails(forms.Form):
    endUrl = forms.CharField(validators=[validateIp], label="IP", required = True)
    endPort = forms.IntegerField(label="Port", max_value=65535, min_value=0, required = True)
    endUser = forms.CharField(label="Username", validators=[validateParseCorrectFormat], required = True)
    endPass = forms.CharField(label="Password", validators=[validateParseCorrectFormat], required = True)