import requests

from django import forms
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.validators import FileExtensionValidator


class SettingForm(forms.Form):
    file = forms.FileField()

def save_config(file_path, f):
    with open(file_path,'wb+') as destination : 
        for chunk in f.chunks():
            destination.write(chunk)


def SettingView(plugin):
    @login_required
    def view(request):
        if request.method == "POST":
            form = SettingForm(request.POST, request.FILES)
            if form.is_valid():
                file_path = plugin.get_path("config")+'/'+request.user.get_username()+'.conf'
                save_config(file_path,request.FILES['file'])
                messages.success(request, "Configuration updated successfuly!")
        
        else : 
            form = SettingForm()

        return render(
            request,
            plugin.template_path("setting.html"),
            {"title": "RClone Storage", "form": form},
        )
    return view

def LoadButtonsView(plugin):
    def view(request):

        return render(
            request,
            plugin.template_path("load_buttons.js"),
            {
                "api_url": "/api" + plugin.public_url("").rstrip("/"),
            },
            content_type="text/javascript",
        )

    return view