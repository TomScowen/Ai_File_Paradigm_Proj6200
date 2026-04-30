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
from appConfig import MAX_CHARACTER_INPUTS, MAX_NEW_TOKENS, TEMPERATURE, TOKENS_PER_DOC_FORCLUSTER
from appErrors import ERRORS
import time #new import to record how long each document took to process.
#Adding new Imports for formulating the JSON for each doc.
import os
from datetime import datetime
import hashlib #(hashlib allows us to create unique ids with metadata)


# path to store Ai Tagged file info.
JSON_PATH = os.path.join(os.path.dirname(__file__), "..","data","filesAiTagged.json")

#|||=================================> Opening JSON Data
def openData():
    try: #attempts to open and read the json file
        with open(JSON_PATH,"r") as f:
            return json.load(f) #opens at the given path
    except FileNotFoundError: #Catch is useful to stop errors
        return{ #setting values to default if error
            "lastSorted": None,
            "documents": {},
            "clusters": {}
        }
#||===============================> Saving Document Data to JSON

def saveDocument(filename,tags,rationale,metadata,error,parseTime,tagTime,totTime):
    data=openData() #loads existing JSON

    #generating unique file ID with Hashlib - https://docs.python.org/3/library/hashlib.html#hashlib.md5
    fileID = hashlib.md5(f"{filename},{metadata['size_bytes']}{metadata['last_modified']}".encode()).hexdigest()[:8] #hexidigest converts hash output to human-readable hexadec string
   
   #updated to have a last modified date, though yet to be able to link this with UI
    lastModifiedRead = datetime.fromtimestamp(metadata["last_modified"]).strftime("%Y-%m-%d %H:%M:%S")

    #creates the new entry in doc dictionary with finame as key. 
    data["documents"][filename]={
        "fileID": fileID, 
        "tags":tags,
        "rationale": rationale,
        "metadata":{"extension": metadata["extension"],"size_bytes":metadata["size_bytes"],"word_count":metadata["word_count"],"last_modified":lastModifiedRead},
        "error": error,
        "parseTime":parseTime,
        "tagTime":tagTime,
        "totTime": totTime,
        "addDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    #this is for updating the lastsorted time stamp. 
    data["lastSorted"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

    # writes the full dictionary back to JSON
    with open(JSON_PATH, "w") as f:
        json.dump(data, f, indent=4) #indent makes it human readable + formatted (which should also help mistral)
    #confirms with the terminal that its document was saved successfully
    print(f"Saved: {filename}")




#parsedResult will be passed through from the app.py (phase4)
def categorise_Doc(parsedResult, existingTags=[]):
 
 #unfortunately haven't figured out how to properly fallback on files yet. 
 #Metadata Fallback...
    if parsedResult["error"] == ERRORS["INSUFFICIENT_CONTENTS"] or parsedResult["error"] == ERRORS["UNSUPPORTED_FILE_TYPE"] or parsedResult["error"]==ERRORS["UNSUPPORTED_IMAGEorSCANNED_PDF"]: #To be added in the future.
        print("W.I.P: Currently Can't Handle MetaData Fallback")
        return None
    
    text = parsedResult["text"][:MAX_CHARACTER_INPUTS]

#Last of OLD PROMPTS as there is a better system recommended for mistral7B and as to add better tagging.
    OLDPROMPT = {'''
#First Iteration of Prompting
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
'''}

#Second Iteration of Prompting
    promptDocData = {f"""[INST]

    Mistral7B, Your duty is as a document tagging assistant.

    Analyse the documents contents and generate a list of descriptive tags of which can accurately describe its contents, topics and context.

    Instruction List:
    - Generate 3 to 8 short tags (1-3 words each).
    - The Tags should be specific and meaningful.
    - The Tags should cover the main topics in the file as well as entities and document type. 
    - Repond ONLY in JSON format, no extra text or explanation. !IMPORTANT!

    Document Content:
    ||| {text} |||

    The following is the Required JSON response format, with example data inserted:

    {{"tags": ["finance", "invoice", "2025", "Loydds Bank"], "rational:" "Document contains financial invoice data from Loydds bank for 2025"}}
    [/INST]"""}

#There has been many versions of this Prompt but this is the final version...
#Attempting new method recommended by huggingface for accuracy. (These messages  is the prompt for Mistral7B)
    messages = [
        {"role":"system","content": "You are a document tagging assistant. You Always respond only in valid JSON format with no extra text."},
        {"role":"user","content": f"""Analyse this document and generate descriptive tags. 
         
         Instructions:
         - Generate 3 to 8 descriptive tags (2-4 words each)
         - The FIRST tag must describe the document type (e.g. "University Supervision Form", "Financial Invoice", "Research Dissertation")
         - Tags should accurately describe the document's content, purpose and context
         - Respond ONLY in JSON format

         Document Content:
         ||| {text} |||

         Required JSON format:
         {{"tags": ["Tag Type One", "Tag Subject Two", "Tag Context Three"], "rationale": "Brief one sentence description of the document."}}
         """}]

    #This converts the input ^ to the format mistral7B expects
    inputs = tokenizer.apply_chat_template(messages,
                                           return_tensors="pt", #returns token output as PyTorch for model Input
                                           add_generation_prompt=True, #adds special token to signal that mistral should generate a response
                                           
                                           ).to(model.device)
    input_ids = inputs["input_ids"].to(model.device) #Extracts the actual token ID nums from token output > resolved errors of mistrals output 
    attention_mask = inputs["attention_mask"].to(model.device) #attention mask tells model which tokens to pay attention to.

    #runs mistrals and gives the input tokens for a new response.
    outputs = model.generate(input_ids=input_ids, 
                             max_new_tokens=MAX_NEW_TOKENS, #custom limiter
                             attention_mask=attention_mask,
                             pad_token_id=tokenizer.eos_token_id, #setts padding to be same as end of sequence. 
                             temperature=TEMPERATURE,
                             do_sample=True)
    

#Taken From Model.py (From earlier Testing) but Using AppConfig Max Tokens: ^Currently Rebuilding
    OLDINPUTS = '''
# Converting the prompt for mistral to read.
    inputs = tokenizer(promptDocData, return_tensors="pt", padding=True).to(model.device) 
# Using mistral to generate a response based on the prompt
    outputs = model.generate(
    input_ids=inputs["input_ids"],
    attention_mask=inputs["attention_mask"] ,#attention mask tells model which tokens to pay attention to.
    max_new_tokens=MAX_NEW_TOKENS, #limter on response to 100 new tokens.
    pad_token_id=tokenizer.eos_token_id, 
    temperature=TEMPERATURE,
    )'''

# decodes the output to human text for reading. (potentially should not decode yet for clustering?)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)    

    #json parsing to find only what we want from the output 
    try:
        json_end = response.rfind("}") + 1
        json_start = response.rfind("{", 0, json_end)
        json_string = response[json_start:json_end]
        result = json.loads(json_string)
        return result
    except json.JSONDecodeError: #catches just encase it fails
        print(ERRORS["PARSE_FAILED"])
        print("Raw response was:", response)
        return None


#promptMetaData -> needs to be added in future... *Avoiding as metadata doesn't actually need to be analysed. 

#|=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-|
# Forming the Clusters from tagged documents using Mistral7B (again)
def formClusters():
    data = openData()
    documents = data.get("documents", {})
    #Making sure 2 documents exist thus to save time and resources on mistral if there isn't 2.
    if len(documents) <2:
        print("There needs to be at least 2 documents to form a cluster. (Not Enough Valid Documents)")
        return
    
    #Building a summary of each document's info for Mistral to form clusters on.

    docSummaries =""
    for filename, doc in documents.items():
        tags=", ".join(doc.get("tags", []))
        rationale=doc.get("rationale","")
        docSummaries += f"-{filename}: Tags: [{tags}] | Rationale: {rationale}\n"

    #to terminal
    print("Forming The Clusters from documents semantic context review.")
    print("Sending semantics to mistral.")
    print(docSummaries) 

    #required to not risk mistral7B getting carried away.
    minClusters =2
    maxClusters = max(2, len(documents)//2) #so the amount of clusters built is dynamically based on how many scanned

    #There has been many versions of this Prompt but this is the final version...
    messages=[{"role":"system","content":"You're a document clustering assistant. You must always respond in JSON Format with no extra text."},
              {"role" :"user","content":f"""Given the following documents and their tag rationales, group them into meaningful semantic clusters. 
               
               
                INSTRUCTIONS:

                -Create between {minClusters} and {maxClusters} clusters.
                -Each cluster should have a short descriptive name (2-5 Words)
                -Assign each document to the cluster that it best fits
                -A document Can appear in multiple Clusters if it fits more than one.
                -If a document 100% doesn't appear to have much belonging to anything, place it in a MISC cluster.
                -Base clustering on SHARED themes across documents. Documents with related tags or topics MUST be grouped together.
                -Prefer BROADER cluster names that can contain multiple documents (e.g. "Loydds Bank" and "Legal Documents" not "Loyyds Bank Invoices" or "Legal Documents on Tenancy")
                -Encourage adding documents to multiple clusters where they share relations, although do not force this.  
                -Respond ONLY in JSON format.
                 

                Documents:
                {docSummaries}

                Required JSON Format:
                {{ "clusters": {{ "Loyyds Banking": {{ "documents": ["fileA.docx", "fileB.pdf"]}}, "Finance Invoices": {{ "documents": ["fileA.docx"]}}}}}}
               """}]

    #Added clusters max tokens, based on the config tokens * by the amount of documents to cluster.
    clusterMaxTokens = max(100, min(len(documents) * TOKENS_PER_DOC_FORCLUSTER, 1000)) #each document needs roughly 20 tokens for outputs. (This is configurable)
    #Added a cap to stop exponential generation.


    #Inputs and Outputs like previously done for document analysis (mistral)
    #=======================-------o
    inputs = tokenizer.apply_chat_template(messages,return_tensors="pt", add_generation_prompt=True) #
    input_ids =inputs["input_ids"].to(model.device)
    attention_mask= inputs["attention_mask"].to(model.device)
    outputs = model.generate( input_ids=input_ids,
                             max_new_tokens=clusterMaxTokens,pad_token_id=tokenizer.eos_token_id, 
                             attention_mask=attention_mask, temperature=TEMPERATURE ,do_sample=True)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    #=======================-------o (Same as Earlier but just for clusters, maybe can be done in function?)
    print("Clusters Raw Response:", response)
    
    #ADDED try catch, for JSON parsing like before, but with more caution as the responses will be much longer. (probably)
    try: #this finds the position of last } like for tagging documents, to get the intended mistral content we need
        json_end = response.rfind("}") + 1
        json_start = response.rfind("{", 0, json_end)
        result = None


        #Loop to keep searching (backwards) until there are still {
        while json_start > 0:
            try: #attempts to parse
                json_string = response[json_start:json_end] 
                result = json.loads(json_string)
                break
            except json.JSONDecodeError:
                json_start = response.rfind("{", 0, json_start) #if parsing fails we move back 1 till next {
        
        #makes sure to only save JSON file if its found
        if result:
            #extracts clustered dictionary from the parsed
            data["clusters"] = result.get("clusters", {})

            with open(JSON_PATH, "w") as f:
                json.dump(data, f, indent=4) #same as before (formatting)
            print("Clusters saved successfully!")
            return result
        else:
            print(ERRORS["PARSE_FAILED"]) #Errors for novelty
            print("Raw Response Was:", response)
            return None

    except: #adds error again if failed.
        print(ERRORS["PARSE_FAILED"])
        print("Raw Response Was:", response)
        return None


#Temporary to test the categorising section...
#only runs when this file is directly executed
if __name__ == "__main__":
    from documentParsing import parse_Doc
    #test file location
    test_file = 'path/file'
    parse_stTime = time.time() #calculates parse time to see how long everything takes,
    parsed_result = parse_Doc(test_file)
    parse_endTime= time.time() 
    parseTime= round(parse_endTime - parse_stTime, 2) #calculating time to parse document
    print("Parsed Result:", parsed_result["metadata"])
    
    fileID = hashlib.md5(f"{parsed_result['metadata']['filename']},{parsed_result['metadata']['size_bytes']}{parsed_result['metadata']['last_modified']}".encode()).hexdigest()[:8] #hexidigest converts hash output to human-readable hexadec string
    data = openData()
    # IF statement checks that the unique hash file ID doesn't already exist, if it does it won't process the document.
    if fileID in [doc.get("fileID") for doc in data["documents"].values()]:
        print("This File Has Already Been Procossed, Skipping AI Processing...")
    else:    
        # added timing and printing results, maybe will add this to info feature.
        print("Processing Results to Document...")
        tag_stTime = time.time() 
        result = categorise_Doc(parsed_result, existingTags=[])
        tag_endTime = time.time()
        tagTime = round(tag_endTime - tag_stTime, 2)
        totTime = round(parseTime +tagTime, 2)

        print("Tag Result:", result)
        print(f"Parsing Time: {parseTime}s & Tagging Time: {tagTime}s || Total Time: {totTime}s")
        #Testing saving document, works /
        if result:
            saveDocument(
                filename=parsed_result["metadata"]["filename"],
                tags=result.get("tags",[]),
                rationale=result.get("rationale", ""),
                metadata=parsed_result["metadata"],
                error=parsed_result["error"],
                parseTime=parseTime,
                tagTime=tagTime,
                totTime=totTime
            )
    formClusters() #THIS WILL ALWAYS RUN TO FORM THE CLUSTERS.

# Reading Material For MISTRAL usage...
#https://docs.mistral.ai/capabilities/function_calls
#https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3