#base rclone
#config filename
#storage_name
#storage_path
#download(local_path, #param dict)
#upload(storage_name, storage_path, local_path)
#set_param(dict)
#build_command()

#this rclone is syncronous

import subprocess
import os
import sys
    
class Storage:
    def __init__(self, config_path, name, path='', rclone_path="/webodm/coreplugins/rclonestorage/rclone"):
        self.config_path = config_path
        self.name = name
        self.path = path
        self.rclone_path = rclone_path

    def download(self, destination_path):
        command = self.download_command_builder()
        command.append(destination_path)
        subprocess.run(command)

    def upload(self, local_path):
        command = self.upload_command_builder(local_path)
        subprocess.run(command)

    def get_file_list(self):
        command = self.get_file_list_command_builder()
        print(command)
        res = subprocess.run(command, capture_output=True, text=True)
        files = res.stdout
        err = res.stderr
        print("files")
        print(files)
        print(err)
        #raise Exception("testing")
        #if there are no files, then none
        if files == '':
            return None
        file_list = files.splitlines()
        return file_list

    def download_command_builder(self):
        command = [self.rclone_path, 
                    '--config',
                    self.config_path,
                    'copy', 
                    ''+self.name+':'+self.path+'']
        return command

    def upload_command_builder(self, local_path):
        command = [self.rclone_path, 
                    '--config',
                    self.config_path,
                    'copy',
                    local_path,
                    ''+self.name+':'+self.path+'']

    def get_file_list_command_builder(self):
        command = [self.rclone_path, 
                    '--config',
                    self.config_path,
                    'lsf', 
                    ''+self.name+':'+self.path+'']
        return command


class StorageManager:
    def __init__(self, username, config_dir="/webodm/coreplugins/rclonestorage/config", rclone_path="/webodm/coreplugins/rclonestorage/rclone"):
        self.username = username
        self.config_dir = config_dir
        self.config_path = os.path.join(config_dir,username+'.conf')
        self.rclone_path = rclone_path
        self.load_storages()

    def get_storage_name_list(self):
        if self.storages == None : 
            return None
        names = []
        for storage in self.storages:
            names.append( storage.name )
        return names

    def get_storage_by_name(self,name):
        for storage in self.storages:
            if storage.name == name:
                return storage
        return None

    def load_storages(self):
        print("config path")
        print(self.config_path)
        command = [
            self.rclone_path,
            "--config",
            self.config_path,
            "listremotes"
        ]
        storage_info = subprocess.run(command, capture_output=True, text=True).stdout
        print("printing storage info..")
        print(storage_info)


        if storage_info == '':
            self.storages = None
            return
        
        split_storage_info = storage_info.splitlines()
        storages = []
        for storage_info in split_storage_info:
            name = storage_info[:-1]
            storages.append( Storage(self.config_path, name, rclone_path=self.rclone_path) )
        self.storages = storages
