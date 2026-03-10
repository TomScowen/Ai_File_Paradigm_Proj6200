#useful links:
# pymupdf.readthedocs.io 
# python-docx.readthedocs.io
# docs.python.org/3/library/pathlib.html
#  _________________________________________________________________
# |=-=-=-=-=-=-=-=-=-=-=-=-=-| PHASE TWO |-=-=-=-=-=-=-=-=-=-=-=-=-=|
# | DOCUMENT PARSING SEGMENT, This section takes uploaded files,    |
# | and extracts the raw text from it: ready to be sent to mistral. |
#  \________________________________________________________________/

# |-----: IMPORTS
from appErrors import ERRORS # Imports list of errors of the app.
from appConfig import MIN_CHARACTER_INPUTS # Minimum Words Input
import fitz #For PDFS (pymupdf)
import docx #For Word Docs (python-docx)
from pathlib import Path #for handling file paths. 

# |----: MAIN FUNCTION
def parse_Doc(file_path):
    ext = Path(file_path).suffix.lower()

    #Pre-Define Variables
    textX = ""
    documentX = ""

    # File Type Options:
    # PDF FILES:
    if ext == '.pdf':
        print ("Loading Parsing Type:",ext)
        documentX = fitz.open(file_path) #opens file
        textX = ""
        for page in documentX:
            textX += page.get_text()
    # WORD DOCUMENT FILES:
    elif ext == '.docx':
        print ("Loading Parsing Type:",ext)
        documentX = docx.Document(file_path) #opens file
        textX = "\n".join([para.text for para in documentX.paragraphs]) #gets a list of paragraphs in document, and loops through each paragraph
    # TEXT FILES:
    elif ext == '.txt':
        print ("Loading Parsing Type:",ext)
        with open(file_path, "r", encoding="utf-8") as f:
            textX = f.read()
    #UNKNOWN FILES:
    else:
        print ("File Type:",ext, "...", ERRORS["UNSUPPORTED_FILE_TYPE"])
        print ("Falling Back To Use Metadata")
        return "METADATA_FALLBACK"

    # Minimum Characters to Ensure a File Has Sufficient Resources to Categorise on. 
    if len(textX.split()) < MIN_CHARACTER_INPUTS:
        print(ERRORS["INSUFFICIENT_CONTENTS"])
        return "METADATA_FALLBACK"
    return textX


#Fallback option, thus if insufficient contents we use metadata instead. 




#for testing temporarily
if __name__ == "__main__":
    test_file = '/Users/TomScowen/Desktop/IMG_7965 2.png'
    result = parse_Doc(test_file)
    print(result[:500])  

    # note edgecase as this pdf (booking.com pdf) generated from a web is largely formated as images rather than text, thus a lot of the document can't be parsed.
    # to counter this maybe I should add a minimum words processed, option 2 is to use OCR (optical character recognition)