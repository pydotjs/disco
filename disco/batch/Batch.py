# import packages
import pathlib

import disco.logs
from disco.file.DocxFile import DocxFile
from disco.file.PdfFile import PdfFile
from disco.file.TxtFile import TxtFile

logger = disco.logs.get(__name__)

class Batch:
    '''
        Loader for files at input paths
    '''
    def __init__(self):

        self.files = [
            # files of disco.file class instance
        ]

    def find_files(self, path, extension, FileClass):
        """
            Open folder and extract matched 
        """

        files = list(path.glob('**/*.{0}'.format(extension)))

        for file_path in files:
            try:
                logger.debug('loading file {0}'.format(file_path))
                instance = FileClass(file_path)
                self.files.append(instance)
            except Exception as e:
                logger.error(e)

    def add_folder(self, path, **kwargs ):
        """
            Open folder and extract matched 
        """
        if isinstance(path, pathlib.PurePath):
            path_local = path
        else:
            path_local = pathlib.Path(path)

        mapping = [
            ['txt', TxtFile],
            ['pdf', PdfFile],
            ['docx', DocxFile]
        ]

        for entry in mapping:
            file_type, FileClass = entry
            active = kwargs.get('file_{0}'.format(file_type), False)
            if active == True:
                self.find_files(path_local, file_type, FileClass)

