import importlib
import requests
import os
from os import path

from app import models, pending_actions
from app.plugins.views import TaskView
from app.plugins.worker import run_function_async
from app.plugins import get_current_plugin

from worker.celery import app
from rest_framework.response import Response
from rest_framework import status

from .rclone import StorageManager

class ImportFolderTaskView(TaskView):
    def post(self, request, project_pk=None, pk=None):
        task = self.get_and_check_task(request, pk)
        
        # Read form data
        storage_name = request.data.get('storage_name', None)
        storage_path = request.data.get('storage_path', None)
        username = request.user.username
        print('username in request')
        print(username)

        # Make sure values are set
        if storage_name == None or storage_path == None:
            return Response({'error': 'Storage name and storage path must be set'}, status=status.HTTP_400_BAD_REQUEST)

        print('check path exists')
        print(os.path.exists(get_current_plugin().get_path('config')))

        storage_manager = StorageManager(username)
        print("storage manager created")
        print("getting storage by name")
        storage = storage_manager.get_storage_by_name(storage_name)
        storage.path = storage_path

        # Make sure that the files actually exists
        print("getting file list")
        file_list = storage.get_file_list()
        print(file_list)
        if file_list == None:
            return Response({'error': 'Failed to get files'}, status=status.HTTP_400_BAD_REQUEST)
        print("file list exist")
        
        # Update the task with the new information
        print("importing..")
        task.console_output += "Importing {} images...\n".format(len(file_list))
        task.images_count = len(file_list)
        task.pending_action = pending_actions.IMPORT
        task.save()
        
        # Associate the folder url with the project and task
        # for status
        print("associating..")
        combined_id = "{}_{}".format(project_pk, pk)
        get_current_plugin().get_global_data_store().set_string(combined_id, storage_name+storage_path)

        # Start importing the files in the background
        print("start importing files async")
        storage_info = {"config_path":storage.config_path, "name":storage.name, "path":storage.path, "rclone_path":storage.rclone_path}
        run_function_async(import_files, task.id, storage_info)

        return Response({}, status=status.HTTP_200_OK)

def import_files(task_id, storage_info):
    from app import models
    from app.plugins import logger
    from coreplugins.rclonestorage.rclone import Storage
    import os

    logger.info("Start importing files")
    task = models.Task.objects.get(pk=task_id)
    task.create_task_directories()
    task.save()

    logger.info("initialize storage")
    storage = Storage(storage_info["config_path"], storage_info["name"], path=storage_info["path"], rclone_path=storage_info["rclone_path"] )

    logger.info("get file list")
    #get file list
    file_list = storage.get_file_list()

    logger.info("update file progress")
    # update file progress
    models.Task.objects.filter(pk=task.id).update(upload_progress=(float(10) / float(100)))

    # download all file
    logger.info("downloading..")
    storage.download(task.task_path())

    logger.info("upload into task")
    # upload all file
    for filename in file_list:
        task.check_if_canceled()
        # upload it
        path = os.path.join(task.task_path(),filename)
        logger.info("uploading image from ")
        logger.info(path)
        models.ImageUpload.objects.create(task=task, image=path)
    logger.info("upload file completed")
    models.Task.objects.filter(pk=task.id).update(upload_progress=(float(100) / float(100)))

    logger.info("update task status")
    task.refresh_from_db()
    task.pending_action = None
    task.processing_time = 0
    task.partial = False
    task.save()

    
    
    
