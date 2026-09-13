from pypdf import PdfReader

reader = PdfReader("uploads/Unit-III-BEE (1).pdf")
text=reader.pages[0].extract_text()
print(text)

document_text=""

for page in reader.pages:
   document_text+=page.extract_text()



