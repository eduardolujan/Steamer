
from django import forms

from steamer.djagios.models import Host
from steamer.djagios.models import Service

class RemoveHostFromServiceForm(forms.Form):
    host = forms.ModelChoiceField(
            label='Host',
            queryset=Host.objects.exclude(register=False).order_by('host_name'))
    service = forms.ModelChoiceField(
            Service.objects.exclude(register=False), 
            widget=forms.Select(
                    attrs={'disabled': 'True'},
                    choices=(('-1', 'Select Host'), )))


class AddHostToServiceForm(forms.Form):
    service = forms.ModelChoiceField(label='Service', 
        queryset=Service.objects.exclude(register=False)\
                .order_by('service_description'))
    host = forms.ModelChoiceField(label='Host', 
        queryset=Host.objects.exclude(register=False).order_by('host_name'))

class AddHostForm(forms.Form):
    host_name = forms.CharField(label='Server Name', max_length=50)
    address = forms.CharField(label='Server Address', max_length=50)
    use = forms.ModelChoiceField(label='Template', 
            queryset=Host.objects.filter(register=False).order_by('name'))

class RemoveHostForm(forms.Form):
    host = forms.ModelChoiceField(label='Host', 
            queryset=Host.objects.exclude(register=False).order_by('host_name'))
    sure = forms.BooleanField(label='Check if you are sure', required=True)


