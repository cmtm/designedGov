from PyPDF2 import PdfFileReader, PdfFileWriter
 
output = PdfFileWriter()
pdfOne = PdfFileReader(open("coverPage.pdf", "rb"))

pdfTwo = PdfFileReader(open("finalReportDraft.pdf", "rb"))

output.addPage(pdfOne.getPage(0))

numPages = pdfTwo.getNumPages()

for i in range(1, numPages):
	output.addPage(pdfTwo.getPage(i))
 
outputStream = open(r"finalReportDraft-incTitle.pdf", "wb")
output.write(outputStream)
outputStream.close()
