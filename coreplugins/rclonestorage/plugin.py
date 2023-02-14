from rest_framework import status
from rest_framework.response import Response

from app.plugins import PluginBase, Menu, MountPoint, get_current_plugin
from app.plugins.views import TaskView
from django.shortcuts import render
from django import forms
from .app_views import SettingView, LoadButtonsView
from .api_views import ImportFolderTaskView

class TestForm(forms.Form):
    testField = forms.CharField(label='Test')


class TestTaskView(TaskView):
    def get(self, request, pk=None):
        task = self.get_and_check_task(request, pk)
        return Response(task.id, status=status.HTTP_200_OK)


class Plugin(PluginBase):

    def main_menu(self):
        return [Menu("RClone Storage", self.public_url(""), "fas fa-archive")]

    def include_js_files(self):
        return ["load_buttons.js"]

    def include_css_files(self):
        return []

    def build_jsx_components(self):
        return ["ImportView.jsx"]

    def app_mount_points(self):
        return [
            MountPoint("$", SettingView(self)),
            MountPoint("load_buttons.js$", LoadButtonsView(self)),
        ]

    def api_mount_points(self):
        return [
            MountPoint("projects/(?P<project_pk>[^/.]+)/tasks/(?P<pk>[^/.]+)/import", ImportFolderTaskView.as_view()),
        ]

    def get_current_plugin_test(self):
        return get_current_plugin()
