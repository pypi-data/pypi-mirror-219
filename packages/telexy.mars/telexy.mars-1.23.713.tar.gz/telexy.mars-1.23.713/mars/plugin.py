from datetime import datetime
import cherrypy
import os
import uuid

class MarsPluginBase(object):

    def __init__(self):
        """constructor"""

    def configuration(self):
        """get configuration"""
        return {}

class MarsFileManagementPlugin(MarsPluginBase):

    def __init__(self, subdirectory):
        """constructor"""
        super().__init__()
        self.subdirectory = subdirectory.strip("/")
    
    def getCurrentDirectory(self):
        """gets current directory of this file"""
        return os.path.dirname(__file__)

    def createFileName(self):
        """creates file name"""
        return '/' + str(uuid.uuid4())

    def getItemSubdirectory(self):
        return "/" + self.subdirectory + "/" + datetime.now().strftime("%m-%d-%Y")

    @cherrypy.expose
    def uploadFile(self, file):
        """upload file"""
        folderDirectory = self.getItemSubdirectory()
        itemDirectory = self.getCurrentDirectory() + folderDirectory
        fileName = self.createFileName()

        #check if path exists, if not, create it
        if(os.path.exists(itemDirectory) == False):
            os.makedirs(itemDirectory)
        
        uploadPath = itemDirectory + fileName
        with open(uploadPath, 'wb') as out:
            while True:
                data = file.file.read(8192)
                if not data:
                    break
                out.write(data)

        return folderDirectory + fileName

    def getFile(self, key):
        """retrieves file via key"""
        directory = self.getCurrentDirectory() + key
        return open(directory)


