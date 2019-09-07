import PyPDF2, os


# Get all the PDF filenames.
pdfFiles = []
path = r'D:\Onedrive\OneDrive - Singapore University of Technology and Design\Term 2\UROP unsupervised learning\scraping\pdf test'
for filename in os.listdir(path):
    if filename.endswith('.pdf'):
        pdfFiles.append(filename)
        
pdfFiles.sort(key = str.lower) #sort the filenames in alphabetical order

pdfWriter = PyPDF2.PdfFileWriter() #to hold the combined PDF pages

# Loop through all the PDF files.
for filename in pdfFiles:
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # Loop through all the pages (except the first) and add them.
    for pageNum in range(1, pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)
        pdfWriter.addPage(pageObj)

# Save the resulting PDF to a file.
pdfOutput = open('allminutes.pdf', 'wb')
pdfWriter.write(pdfOutput)
pdfOutput.close()
    
    
