
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

    # File Type Options:
    if ext == '.pdf':
        print ("Loading Parsing Type:",ext)
        pass # PDF Parsing  #Logic To Be Coded here.
    elif ext == '.docx':
        print ("Loading Parsing Type:",ext)
        pass # Word Document Parsing
    elif ext == '.txt':
        print ("Loading Parsing Type:",ext)
        pass # Text File Parsing
    else:
        print ("File Type:",ext, "Can't be handled By The Application")
        pass #Unaccounted For Type


