# import packages
import PyPDF2

from disco.file.File import File
import disco.logs
logger = disco.logs.get(__name__)

class PdfFile(File):

    @staticmethod
    def open_file(path):
        # open the pdf file
        return PyPDF2.PdfFileReader(str(path.resolve()))

    def inspect_chunks(self):
        file = self.file
        return file.getNumPages()

    def yield_chunks(self):
        file = self.file
        # extract text and do the search
        for i in range(0, self.chunks):
            page = file.getPage(i)
            text = page.extractText()
            yield text