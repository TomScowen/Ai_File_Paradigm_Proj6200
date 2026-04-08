#  ___________________________________________________________________
# |=-=-=-=-=-=-=-=-=-=-=-=-=-| PHASE THREE |-=-=-=-=-=-=-=-=-=-=-=-=-=|
# | DOCUMENT CATEGORISING PHASE, this is where extracted text from P2 |
# | is sent to Mistral7B with well designed prompting to return categ-|
# | -ory and rationale with a JSON format, the results will be stored |
# |                                                                   |
# |       This is where the CORE AI-Driven Aspect Is Applied.         |
#  \_________________________________________________________________/


# |-----: IMPORTS
import torch
import json
from model import model, tokenizer
from appConfig import MAX_CHARACTER_INPUTS, MAX_NEW_TOKENS, TEMPERATURE
from appErrors import ERRORS

#parsedResult will be passed through from the app.py (phase4)
def categorise_Doc(parsedResult, existing_categories=[]):
 
 #Metadata Fallback...
    if parsedResult["error"] == ERRORS["INSUFFICIENT_CONTENTS"] or parsedResult["error"] == ERRORS["UNSUPPORTED_FILE_TYPE"]: #To be added in the future.
        print("W.I.P: Currently Can't Handle MetaData Fallback")
        return None
    
    text = parsedResult["text"][:MAX_CHARACTER_INPUTS]

#To be Made...
    prompt = f"""..."""
