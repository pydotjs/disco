# import packages
import PyPDF2

from disco.file.File import File
import disco.logs
logger = disco.logs.get(__name__)

class TxtFile(File):

    @staticmethod
    def open_file(path):
        return None

    def inspect_doc(self, file_path, terms):
        # open the pdf file
        # pdf_data = PyPDF2.PdfFileReader(str(file_path.resolve()))

        return None

    def yield_chunks(self):
        file = self.file
        # extract text and do the search
        for i in range(0, self.chunks):
            page = file.getPage(i)
            text = page.extractText()
            yield text