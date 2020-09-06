# import packages
import pathlib

import pandas as pd

from disco.file.File import File
import disco.logs
logger = disco.logs.get(__name__)

class Report:
    '''
        Base Report class which houses typical methods
        Don't use this class directly - use the appropriate
        class for your file type
    '''
    def __init__(self, files, path):

        assert isinstance(files, list), 'files must be a list'

        for entry in files:
            assert isinstance(entry, File), 'file must be of Disco File instance'

        self.files = files

        if isinstance(path, pathlib.PurePath):
            path_local = path
        else:
            path_local = pathlib.Path(path)
        self.path = path_local

        self.path.mkdir(parents=True, exist_ok=True)

    def process(self, terms):
        """
            Override on children
        """
        # create output folder if not already exist
        
        return None