#useful links:
# pymupdf.readthedocs.io 
# python-docx.readthedocs.io
# docs.python.org/3/library/pathlib.html
#  _________________________________________________________________
# |=-=-=-=-=-=-=-=-=-=-=-=-=-| PHASE TWO |-=-=-=-=-=-=-=-=-=-=-=-=-=|
# | DOCUMENT PARSING SEGMENT, This section takes uploaded files,    |
# | and extracts the raw text from it: ready to be sent to mistral. |

# |-----: IMPORTS
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
    # PDF FILES
    if ext == '.pdf':
        print ("Loading Parsing Type:",ext)
        documentX = fitz.open(file_path)
        textX = ""
        for page in documentX:
            textX += page.get_text()
    # WORD DOCUMENT FILES
    elif ext == '.docx':
        print ("Loading Parsing Type:",ext)
        pass # Word Document Parsing
    # TEXT FILES
    elif ext == '.txt':
        print ("Loading Parsing Type:",ext)
        pass # Text File Parsing
    #UNKNOWN FILES
    else:
        print ("File Type:",ext, "Can't be handled By The Application")
        pass #Unaccounted For Type

    return textX

#for testing temporarily
if __name__ == "__main__":
    test_file = '/Users/TomScowen/Desktop/Booking.com_ Confirmation.pdf'
    result = parse_Doc(test_file)
    print(result[500])  

    # note edgecase as this pdf (booking.com pdf) generated from a web is largely formated as images rather than text, thus a lot of the document can't be parsed.
    # to counter this maybe I should add a minimum words processed, option 2 is to use OCR (optical character recognition)