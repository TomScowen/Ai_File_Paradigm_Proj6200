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
def categorise_Doc(parsedResult, fileCategories=[]):
 
 #Metadata Fallback...
    if parsedResult["error"] == ERRORS["INSUFFICIENT_CONTENTS"] or parsedResult["error"] == ERRORS["UNSUPPORTED_FILE_TYPE"]: #To be added in the future.
        print("W.I.P: Currently Can't Handle MetaData Fallback")
        return None
    
    text = parsedResult["text"][:MAX_CHARACTER_INPUTS]

#To be Made...
    promptDocData = f"""[INST]
    
    Mistral7B, Your Duty is as a Document Categorisation Assistant.

    The Existing Document Categories are as: {fileCategories}

    You will need to analyse the document contents and decide wheres it should belong within a file system.
    
    Instruction List:
    - If the Document fits within an existing category, use that exact category name. 
    - If no existing category fits, create a new short category name. (5 Words Maximum)
    - Respond ONLY with JSON format, no extra text or explanation.

    Document Content:
    ||| {text} |||

    Required JSON response format: 
    {{"category": "Finance and Accounting", "rationale": "This Document Contains Financial Statements"}} 
    [/INST]"""

#Taken From Model.py (From earlier Testing) but Using AppConfig Max Tokens:
# V 
# Converts prompt string into num token ids. 
    inputs = tokenizer(promptDocData, return_tensors="pt", padding=True).to(model.device)
# Generates response from the input. 
    outputs = model.generate(
    input_ids=inputs["input_ids"],
    attention_mask=inputs["attention_mask"],
    max_new_tokens=MAX_NEW_TOKENS, #limter on response to 100 new tokens.
    pad_token_id=tokenizer.eos_token_id, 
    temperature=TEMPERATURE
    )

# Converts the output token IDS back to human txt. (decoding)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)    

    #Parse the JSON: 
    try: 
        result = json.loads(response)
        return result
    except json.JSONDecodeError:
        print(ERRORS["PARSE_FAILED"])
        return None




#promptMetaData -> needs to be added in future...





# Reading Material For MISTRAL usage...
#https://docs.mistral.ai/capabilities/function_calling
#https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3