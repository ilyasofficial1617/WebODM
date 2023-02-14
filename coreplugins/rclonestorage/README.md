# RCloneStorage

RCloneStorage plugin integrates RClone to be used for import images (and soon export) for WebODM. RClone integrates many cloud storage, such as google drive, dropbox, s3, http server, ftp, etc. 

## Installation
1. Download rclone.zip from https://rclone.org/downloads/
2. Extract the file named rclone into coreplugins/rclonestorage
3. From dashboard sidebar, there is rclone storage tab
4. In RClone Storage Setting page, upload your configuration. Your local configuration can be found with this command 'rclone config file'
5. This configuration is user-specific, which means every user have different configuration

## Usage
1. Click cloudimport button on the project
2. Provide information of storage name and storage path
3. Proceed as usual

## Limitation
The user-specified configuration is not yet being tested extensively. This means that user must verify that the configuration is valid from their own device, before inserting.

Many common feature of cloud storage is not yet exist, such as listing directory and verifying files.

The folder in remote or cloud storage MUST be only filled by image files.

Currently, this plugin uses only the generic rclone command without any additional flag. Storage-specific way to download, such as link download which uses flag, is not yet supported.

Feel free to contribute to remove these limitation or adding new type of storage-specific download. 

## Credit
Thanks to cloudimport plugin by Nicolas Chamo and dronedb plugin by Luca Di Leo, which i used a lot for reference and template. 

## Dev Notes

Features that not yet implemented:
1. Provide multiple choice of storage name instead of typing it in
2. Add export capabilities
3. Listing files inside directory and subfolder file search
4. File selection and filtering
5. Verify file existance before importing
Please feel free to contribute to this plugin

Here lies some of my log, design decision, and what i learn during development of this plugin. I hope this note can be beneficial.

1. Fundamentally its not too different compared to cloudimport and dronedb. The difference is in input data and how to download the images. The required data is storage name and the path inside of it. The download process is handled by rclone by using command 'rclone copy remote:path/to/folder specifiedpath', instead of ajax calls. 

2. There are four different way rclone can be used : docker, command terminal, python wrapper, librclone. I avoid using method that are difficult to implement and difficult to install. Docker are difficult to install, difficult to implement, and introduce new dependency, such as fuse and dockerpy. Python wrapper, such as librclone (official), python-rclone, rclone-python. These wrapper makes it easy to integrate with python, but i can't chose between these three, and i don't trust them updating their wrapper regularly. The best choice is to use command terminal. The executable file is just one file and can be moved without breaking its functionality. The plugin must be independent.

3. There are two ways to run command, with shell=True or with shell=False. Shell=True opens terminal from system like when a user opens a terminal. This proven problematic for path-ing. WebODM path uses the folder as its root folder. Try to run 'ls /' via WebODM app and via regular terminal, it'll results in different folder. Pathing hell. Shell=True also strongly not recommended because of security reasons. While Shell=False can't directly call rclone from /usr/bin , it can be solved by copying rclone into the plugin folder. It's kind of janky, but it works. In conclusion the best choice is to use shell=False and provide rclone program file to folder. 

4. Originally the name is rclone-storage, but i can't import python package with - in its name so i changed it to rclonestorage

5. Plugin.py contains mounting of app and api that being used. Those app and api came from app_views.py and api_views.py. api_views.py contains all logic that being used while app_views.py contains all top level views. Function logic inside api_views can be mounted on api calls inside plugin.py, they can be called by using ajax. 
