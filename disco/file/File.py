# import packages
import pathlib

import disco.logs
logger = disco.logs.get(__name__)

class File:
    '''
        Base File class which houses typical methods
        Don't use this class directly - use the appropriate
        class for your file type
    '''
    def __init__(self, path):

        if isinstance(path, pathlib.PurePath):
            path_local = path
        else:
            path_local = pathlib.Path(path)

        self.path = path_local
        self.file = None
        self.accessed = False
        self.inspected = False

        self.inspect()

    def access(self):
        """
        Attempt to open file and store data on instance
        """
        # open the pdf file
        data = self.open_file(self.path)

        self.file = data
        self.accessed = True

    @staticmethod
    def open_file(path):
        """
            Override on children
        """
        return None

    def inspect_title(self):
        """
            Override on children
        """
        return self.path.stem

    def inspect_chunks(self):
        """
            Override on children
        """
        return 0

    def inspect(self):
        """
            Gather meta data for file. Types of meta data
            available will vary on the file type, e.g. page
            count for PDF, paragraphs for DocX, which will
            be mapped to common props, such as 'chunks'
        """
        if self.accessed == False:
            self.access()

        self.title = self.inspect_title()
        self.chunks = self.inspect_chunks()

    def yield_chunks(self):
        '''
            Yield chunks of text from file
            Override on children
        '''

        for entry in []:
            yield entry

    def content_chunks(self):
        '''
            return chunks of text from file in sequence
        '''
        if self.inspected == False:
            self.inspect()

        for i, entry in enumerate(self.yield_chunks()):
            logger.debug('chunk {0}'.format(i))
            yield entry

    def build_complete(self):
        '''
            Return complete text from file
            Override on children
        '''
        complete = []
        for chunk in self.yield_chunks():
            complete.append(chunk)
        return '\n'.join(complete)

    def content_complete(self):
        '''
            return complete text from a file
        '''
        if self.inspected == False:
            self.inspect()

        return self.build_complete()