import ghostscript # for converting pdf file to text (though Hebrew is reversed)

from PyPDF2 import PdfFileReader # just for getting number of pages in PDF

from utils import suppress_stdout # so you don't see all of the output from Ghostscript

PDFPath = 'C:\\Users\\ADMIN\\PycharmProjects\\Project_Kdam\\data1\\Catalogue17-18.pdf'

pdf = PdfFileReader(open(PDFPath,'rb'))
numOfPages : int = pdf.getNumPages()

# p=pdf.getPage(70)
#
# p_text= p.extractText()
# # extract data line by line
# P_lines=[line for line in p_text.splitlines() if line!='']
# print(P_lines)

# getPageNum = [
#     "gs".encode(),
#     "-q".encode(), "-dNODISPLAY".encode(),
#     "-c".encode() + "(C:\\Users\\ADMIN\\PycharmProjects\\Project_Kdam\\data1\\Catalogue17-18.pdf) (r) file runpdfbegin pdfpagecount = quit".encode()
# ]
#
# ghostscript.Ghostscript(*getPageNum)

args = [
    "gs".encode(),
    "-sDEVICE=txtwrite".encode(),
    ("-o" + "C:\\Users\\ADMIN\\PycharmProjects\\Project_Kdam\\data1\\blah-%d.txt").encode(),
    PDFPath.encode(),
]

# devnull = open(os.devnull, 'w')
# oldstdout_fno = os.dup(sys.stdout.fileno())
# os.dup2(devnull.fileno(), 1)
# # makesomenoise()
# ghostscript.Ghostscript(*args)
# os.dup2(oldstdout_fno, 1)

with suppress_stdout():
    ghostscript.Ghostscript(*args)

# ghostscript.Ghostscript(*args)