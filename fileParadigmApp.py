#  ___________________________________________________________________
# |=-=-=-=-=-=-=-=-=-=-=-=-=-| PHASE  FOUR |-=-=-=-=-=-=-=-=-=-=-=-=-=|
# | FILE PARADIGM APP > This section is dedicated to the Streamlit UI |
# | for the application. Where the UI will allow for file uploading,  |
# | passed through the other phases and outputting a newly generated. |
# | file made system.                                                 |
# |                                                                   |
# |                                                                   |
# |           The Core UI and Direction of the Application.           |
#  \_________________________________________________________________/

#=========================================================================|
# --------- IMPORT LIST ----> 
import streamlit # for building the user interface
import sys # pythons built in sys library (needs to be modified python path for core folder)
import os # pythons built-in operating system (needs to build file path for core folder)
#sys.stdout = open(os.devnull, 'w') #temporary

#getting path of current "__file__", getting the directory containing it from the OS and joining the path with the core for full
#path to core folder. The insert adds the path to the pythons search list (so imports work correctly from core)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "core")) 
# ^ useful links: https://docs.python.org/3/library/sys.html#sys.path + https://docs.python.org/3/library/os.path.html

#Importing from phase 2 and 3...
from documentParsing import parse_Doc

# ADDED WHEN LINKING - To load the AI MODEL and document processin functions and to cache the for the entire streamlit session.
@streamlit.cache_resource # - without this every time we rerun mistral7B would be loaded...
def load_model(): #imported in a function so the cache controls when it runs
    from documentCategoriser import categorise_Doc, saveDocument, formClusters, openData
    return categorise_Doc, saveDocument, formClusters, openData

#unpacks the returned function
categorise_Doc, saveDocument, formClusters, openData = load_model()

#new imports for time and hash ids
import time
import hashlib

#Temp File Import, for file to upload as in-memory objects.
import tempfile
import json
#=========================================================================|

#__________________________________________________________________________                     
# APP UI BUILDING INF Srces --->                                           |                        
# docs.streamlit.io                                                        |                                          
# docs.streamlit.io/library/api-reference                                  |                                            
# docs.streamlit.io/library/cheatsheet                                     |  
# developer.mozilla.org/en-US/docs/Web/CSS - Good link for CSS information.|                       
#__________________________________________________________________________|                       
                                                                            



# DISABLED -> When enabled it hides the streamlit default sys settings. (Not In Use)
temp = '''
streamlit.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
'''

#                                                 |||||||||||||||||
#                                          |||||||||||||||||||||||||||||||
#                                    |||||||||||||||||||||||||||||||||||||||||||
#                               |||||||||||||||||||||||||||||||||||||||||||||||||||||
#                           |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                        |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                      |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                    |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                   |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                  |||||                                                                     |||||
#                  |||||              APPLICATION INITIATION AND CONFIGURATIONS              |||||
#                  |||||                                                                     |||||
#                   |||                                                                       |||
#                    |                                                                         |
#                    V                                                                         V


#=========================================================================|
# --------- INITIALISATION ----> 
# Initial Page Setup  
streamlit.set_page_config( page_title="Ai-Driven File Paradigm Application", page_icon="🗂️", layout="wide" )

# Initialises Selected File, If it doesn't exist it creates it as an empty. (for app start up when nothing is uploaded.)
if "selected_file" not in streamlit.session_state: streamlit.session_state.selected_file=None

# Sets the default view mode upon App launch.
if "viewMode" not in streamlit.session_state: streamlit.session_state.viewMode = "AI-Sorted Repository"
viewModeTitle = streamlit.session_state.viewMode #sets title. 

#uploaded_files = []

# Loading The AI-Sorted Files Json:
def load_sorted_files():
    json_path = os.path.join(os.path.dirname(__file__), "data", "filesAiTagged.json") #Builds full file path to json.
    try:
        with open(json_path, "r") as f: return json.load(f) #Reads and Converts Json to Python

    except FileNotFoundError: return {"last_sorted": None, "documents": {}, "clusters": {}} #catches for App launch. 

sorted_data = load_sorted_files() #Calls the function.
#=========================================================================|

#=========================================================================|
# --------- STANDARDISING APP UI FRAMEWORK / SKELETON ----> 

#------------------------------------------------------------| CONTROL PANEL SKELETON CONFIG |------------------>
#Locking the CONTROL PANEL!  thus that its size doesn't alter and remains / retains its shape.
streamlit.markdown("""
<style>
                   
    [data-testid="stSidebar"] {
        min-width: 295px !important;
        max-width: 295px !important;
    }
    [data-testid="stSidebarResizer"] {
        display: none !important;
    }
    [data-testid="stSidebar"] .block-container {
        padding-bottom: 0rem !important;
    }
    [data-testid="stSidebar"] {
        min-width: 295px !important;
        max-width: 295px !important;
        background-color: #4a5a6e !important;
    }
    [data-testid="stSidebar"] ::-webkit-scrollbar {
    display: none !important;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #5d7a9a !important;
    }
    [data-testid="stMain"] {
        background-color: #5d7a9a !important;
    }
</style>
""", unsafe_allow_html=True)
#------------------------------------------------------------|



#------------------------------------------------------------| DIRECTORY PANEL HEADER (Right) |------------------>
#creates an adjustable header for the DIRECTORY PANEL, thus that the name and last sorted info adjusts with the options. (UPDATED)
streamlit.markdown(f"""
    <div style="
        background-color: #2952a3;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-left: -5rem;
        margin-right: -5rem;
        margin-top: -3.3rem;
        margin-bottom: 15px;
        border: 5px solid #1a3f6e;">
        <span style="color: white; font-size: 1.2em; font-weight: bold; font-style: italic;">
            🗂️ {viewModeTitle}
        </span>
        <span style="color: white; font-style: italic; font-size: 0.85em;">
           ⚠️ W.I.P: Last Sorted... Not yet sorted
        </span>
    </div>
""", unsafe_allow_html=True)
#------------------------------------------------------------|


#------------------------------------------------------------| CONTROL PANEL HEADER (Left) |------------------>
with streamlit.sidebar:
    streamlit.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
    streamlit.markdown("""
        <div style="
            background-color: #1a3a6b;
            padding: 11px 14px;
            margin-left: -0.9rem;
            margin-right: -0.9rem;
            margin-top: -2.8rem;
            margin-bottom:-5rem;
            border: 5px solid #0f2547;
        ">
            <span style="color: white; font-size: 1.1em; font-weight: bold;">
                ⚙️ AI-Driven File Paradigm APP
            </span>
        </div>
    """, unsafe_allow_html=True)

#                    |                                                                         |
#                   |||                                                                       |||
#                  |||||                                                                     |||||
#                  |||||              APPLICATION INITIATION AND CONFIGURATIONS              |||||
#                  |||||                                                                     |||||
#                   |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                    |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                      |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                        |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                           |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                               |||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                                    |||||||||||||||||||||||||||||||||||||||||||||||
#                                          |||||||||||||||||||||||||||||||||||
#                                                 |||||||||||||||||
#
#
#
#                                                 |||||||||||||||||
#                                          |||||||||||||||||||||||||||||||
#                                    |||||||||||||||||||||||||||||||||||||||||||
#                               |||||||||||||||||||||||||||||||||||||||||||||||||||||
#                           |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                        |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                      |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                    |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                   |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                  |||||                                                                     |||||
#                  |||||                       CONTROL PANEL UI & DESIGN                     |||||
#                  |||||                    (All of Left Side Panel Coding)                  |||||
#                   |||                                                                       |||
#                    |                                                                         |
#                    V                                                                         V

#------------------------------------------------------------| 
with streamlit.sidebar: #renders in control panel.
    streamlit.markdown('<div style="margin-top: 0px;"></div>', unsafe_allow_html=True)
    # Adds the UI Design for the Run Button.
    streamlit.markdown("""
    <style>
        [data-testid="stButton"] button {
            background-color: #eef2f7 !important;
            color: #4caf50 !important;
            border: 2px solid #4caf50 !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            margin-top: -15rem;
            margin-bottom: -20rem;
        }
        [data-testid="stButton"] button:hover {
            background-color: #4caf50 !important;
            color: white !important;
            border-color: #388e3c !important;
        }
        [data-testid="stExpander"] [data-testid="stButton"] button {
            background-color: transparent !important;
            color: #2d2d2d !important;
            border: 1px solid #2d2d2d !important;
            border-radius: 4px !important;
            padding: 2px 6px !important;
            font-size: 0.8em !important;
        }
    </style>
    """, unsafe_allow_html=True)
    # Run Button (added key to be selected) - was having an issue editing the run button, this lets us targets it
    streamlit.button("▶  Run AI-Categorising", use_container_width=True, key="run_button")





    # Run button logic has been moved, as it needs to operate after upload files...

    






    # Loading Bar (needs to be hooked up ofc)
    streamlit.markdown("""
    <style>
        .stProgress > div > div > div {
            border: 0.1px solid #4caf50 !important;
            border-radius: 4px !important;
        }
        .stProgress {
            margin-top: -20px !important;
            margin-bottom: -20px !important;
        }
        .stProgress > div > div > div > div {
            background-color: #4caf50 !important;
        }
        
    </style>
    """, unsafe_allow_html=True)
    streamlit.progress(10)


#    __________________________________________________________________    
#   |                     UPLOAD FILE BOX (FINAL)                      |
#   |                                                                  |
#   | stFileUploader > is the Outer Box.                               |
#   | stFileUploaderDropzone > is the inner box                        |
#   | stFileUploaderDropzoneInstructions span > Drag & drop text       |
#   | stFileUploaderDropzone button > the actual browse files button   |
#   | stFileUploader label = is the heading label of the box           |
#   |                                                                  |
#   | !important > forces the style to override streamlits defaults    |
#   |              (it essentially fights streamlits framework)        |
#   |                                                                  |
#   |  To Resolved The Issues: github.com/streamlit/streamlit/issues   |
#   | & inspect elements in browser tools                              |
#   |                                                                  |
#   V                                                                  V
#the ui design and tweaks of the drag and drop box
    streamlit.markdown("""
    <style>
        [data-testid="stFileUploader"] {
            background-color: #eef2f7;
            border: 2px solid #4a7ab5;
            border-color: #4a7ab5;
            border-radius: 8px;
            padding: 5px;
            margin-top: -1.5rem;
        }
        [data-testid="stFileUploaderDropzone"] {
            background-color: #f5f8fc !important;
            border-radius: 6px !important;
            text-align: center !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
        }
        [data-testid="stFileUploaderDropzoneInstructions"] span {
            color: #5a7a9a !important;
        }
        [data-testid="stFileUploaderDropzone"] button {
            background-color: #7aafd4 !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
        }
        [data-testid="stFileUploader"] label {
            text-align: center !important;
            display: block !important;
            color: #5a7a9a !important;
        }
    </style>
    """, unsafe_allow_html=True)
    # Upload File Box (Where u can drag and drop into)
    uploaded_files = streamlit.file_uploader(
        "📂 Upload Files",
        accept_multiple_files=True,
        type=["pdf", "docx", "txt"],
    )
    #checking if the run button has been clicked
    if streamlit.session_state.run_button:
        if not uploaded_files: #checks if files have been uploaded.
            streamlit.warning("Please upload files first!")
        else:
            #creates the progress bar to count how many files need processing, seems to not work come back to.
            progress = streamlit.progress(0) 
            total = len(uploaded_files)

        
            #loops through each uploaded file.
            for i, uploaded_file in enumerate(uploaded_files):
                streamlit.write(f"Processing: {uploaded_file.name}")
                
                #streamlit uploads in memory objects thus the file needs actual path on the disk. 
                with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp: #delete=false temporarily keeps before block closes
                    tmp.write(uploaded_file.getbuffer())
                    tmp_path = tmp.name
                
                #added timers for analysis
                parse_stTime = time.time()
                #parsing the document
                parsed_result = parse_Doc(tmp_path)
                parse_endTime= time.time()
                parseT = round(parse_endTime - parse_stTime, 2)
                
                #generates the fileID (which is unique but static to each file)
                fileID = hashlib.md5(f"{parsed_result['metadata']['filename']},{parsed_result['metadata']['size_bytes']}{parsed_result['metadata']['last_modified']}".encode()).hexdigest()[:8]
                data = openData()
                #if the FileID exists in the json we will skip mistral to save processing time. 
                if fileID not in [doc.get("fileID") for doc in data["documents"].values()]:

                    #adding timers for analysis
                    tag_stTime = time.time()
                    result = categorise_Doc(parsed_result) #inputting parsed results to categorise
                    tag_endTime = time.time()
                    tagT = round(tag_endTime - tag_stTime, 2)
                    totTime = round(parseT + tagT , 2)

                    print(f"TIMINGS FOR FILE: {uploaded_file.name} | Parsing time >> {parseT}s | Tagging time >> {tagT}s | Total Time >>> {totTime}s")

                    
                    if result:
                        #Like done in documentCategoriser.py this saves files infomration to the JSON
                        saveDocument(
                            filename=uploaded_file.name,
                            tags=result.get("tags", []),
                            rationale=result.get("rationale", ""),
                            metadata=parsed_result["metadata"],
                            error=parsed_result["error"],
                            parseT=parseT,
                            tagT=tagT,
                            totTime=totTime
                        )
                
                progress.progress((i + 1) / total)
            
            formClusters()
            streamlit.success("Done! Files categorised and clusters formed.")
            streamlit.rerun()
#   
#   |                 End Of Upload File Box UI                        |
#   |__________________________________________________________________|


#    ____________________________________________________________________________    
#   |                              Select View Feature                           |
#   |                                                                            |
#   | Select Options:                                                            |
#   | - AI-Sorted Repository                                                     |
#   | - Unsorted Repository                                                      |
#   | - Runtime Application Report                                               |
#   |                                                                            |
#   V                                                                            V

# Repository View Button - Sidebar using radio radio button groups
    streamlit.markdown("""
    <style>
      div[data-testid="stRadio"] {
          background-color: #eef2f7;
          border: 2px solid #4a7ab5;
         border-radius: 6px;
         padding: 10px;
         margin-top: -20px;
         margin-right: -15.7rem;
        
      }
     /* Repository View title */
     div[data-testid="stRadio"] > label {
         text-align: center !important;
         display: block !important;
         font-size: 1.1em !important;
         font-weight: bold !important;
         color: #5a7a9a !important;
     }
        /* Radio option text */
        div[data-testid="stRadio"] p {
            color: #5a7a9a !important;
     }
    </style>
    """, unsafe_allow_html=True)

# Repository Mode Selection ⚠️
    streamlit.radio(
        "Repository View",
     [
           "AI-Sorted Repository",
            "Upload Repository ⚠️ W.I.P",
            "Runtime Report ⚠️ W.I.P"
        ],
        key="viewMode")

#   |                       End of Select View Feature                           |
#   |____________________________________________________________________________|  

#    ____________________________________________________________________________    
#   |                      Select Processing Mode Feature                        |
#   |                                                                            |
#   | Select Options:                                                            |
#   | - Fast                                                                     |
#   | - Balanced                                                                 |
#   | - Thorough                                                                 |
#   |                                                                            |
#   V                                                                            V

# CSS for Processing Mode box (same as the repository view box ^^^^^)
    streamlit.markdown("""
    <style>
      div[data-testid="stRadio"]:nth-of-type(2) {
          background-color: #eef2f7;
          border: 2px solid #4a7ab5;
          border-radius: 6px;
          padding: 10px;
          margin-top: 10px;
          margin-right: 0rem; 
      }
    </style>
    """, unsafe_allow_html=True)

    # Processing Mode Selection
    streamlit.radio(
        "⚠️ Processing Mode (W.I.P) ⚠️",
        [
            "Fast ⚠️",
            "Balanced",
            "Thorough ⚠️"
        ],
        index=1,  #sets the default option as balanced
        key="processingMode"
    )
#   |                    End of Select Processing Mode Feature                   |
#   |____________________________________________________________________________|  


#    ____________________________________________________________________________    
#   |                  Download AI-Sorted Repository as Zip Feature              |
#   |                                                                            |
#   V                                                                            V

    #Adding the download button from streamlit 
    streamlit.markdown('<div style="margin-top: 0px;"></div>', unsafe_allow_html=True)
    streamlit.markdown("""
    <style>
        [data-testid="stDownloadButton"] button {
            background-color: #eef2f7 !important;
            color: #e53935 !important;
            border: 2px solid #e53935 !important;
            border-radius: 8px !important;
            width: 100% !important;
            font-weight: bold !important;
            font-size: 0.5em !important;
        }
        [data-testid="stDownloadButton"] button:hover {
            background-color: #e53935 !important;
            color: white !important;
            border-color: #b71c1c !important;
        }
        [data-testid="stDownloadButton"] {
            margin-top: -35px !important;
        }
        
    </style>
    """, unsafe_allow_html=True)

    #This adds the download button characteristics. (probably need a unique code generator and date for file name.)
    streamlit.download_button(
     label="⬇ Download New Repository ⚠️ W.I.P",
        data=b"",
     file_name="AI_Sorted_Repository.zip",
     mime="application/zip",
     use_container_width=True,
     disabled=True
    )
    #This adds the warning text right below the download button
    streamlit.markdown("""
        <div style="
           font-size: 0.7em;
            color: #e53935;
            text-align: center;
            font-style: italic;
            margin-top: -10px;
     ">
         ⚠️ This does not delete your original files.<br>
            Two sets of files may be found on your device!
        </div>
    """, unsafe_allow_html=True)

#   |                      End of Download Button Feature                        |
#   |____________________________________________________________________________|  

#                    |                                                                         |
#                   |||                                                                       |||
#                  |||||                                                                     |||||
#                  |||||                     END OF  CONTROL PANEL SECTION                   |||||
#                  |||||                                                                     |||||
#                   |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                    |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                      |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                        |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                           |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                               |||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                                    |||||||||||||||||||||||||||||||||||||||||||||||
#                                          |||||||||||||||||||||||||||||||||||
#                                                 |||||||||||||||||


# Section 3: Directory Panels 


#                                                 |||||||||||||||||
#                                          |||||||||||||||||||||||||||||||
#                                    |||||||||||||||||||||||||||||||||||||||||||
#                               |||||||||||||||||||||||||||||||||||||||||||||||||||||
#                           |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                        |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                      |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                    |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                   |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                  |||||                                                                     |||||
#                  |||||                     DIRECTORY PANEL VIEW OPTIONS                    |||||
#                  |||||                  (This Includes the Ifs for Options)                |||||
#                   |||                                                                       |||
#                    |                                                                         |
#                    V                                                                         V


#==============|  Folder Drop Down Styling  |===>
#initial expander is a different outer container of each folder dropdown.
#details expander is the clickable header of each folder
#details[open] is clickable header when expanded
# further expanders fore file names, and arrows and info butons forcing the colours.
# final expander adds a hover to highlight buttons
streamlit.markdown("""
    <style>
        [data-testid="stExpander"] {
            background-color: #ffffff !important;
            border-radius: 8px !important;
            border: 1px solid #c5d5e8 !important;
            margin-bottom: 5px !important;
        }
        details[data-testid="stExpander"] > summary {
            background-color: #ffffff !important;
            border-radius: 8px !important;
        }
        details[open] > summary {
            background-color: #fff176 !important;
            border-radius: 8px 8px 0 0 !important;
            color: #2d2d2d !important;
        }
        [data-testid="stExpander"] summary p {
            color: #2d2d2d !important;
        }
        [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {
            color: #2d2d2d !important;
        }
        [data-testid="stExpander"] summary span[data-testid="stIconMaterial"] {
            color: #2d2d2d !important;
        }
        [data-testid="stExpander"] [data-testid="stButton"] button {
            background-color: transparent !important;
            color: #2d2d2d !important;
            border: none !important;
            padding: 2px 6px !important;
            font-size: 0.8em !important;
            margin-right: 6rem !important;
        }
        [data-testid="stExpander"] [data-testid="stButton"] button:hover {
            background-color: #4caf50 !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)
#=====================================||
#


#|||======================================== Everything Below Only Renders In Right Panel IF AI-SORTED REPOSITORY selected.
# checking which radio is selected for viewmode. 
if streamlit.session_state.viewMode == "AI-Sorted Repository":

 #==============|  AI SEARCH BAR (WIP)  |===>
 # formatting search bar but not yet implemented for use.
    streamlit.markdown("""
        <div style="
            background-color: #4a6a8a;
            border: 1px solid #3a5a7a;
            border-radius: 8px;
            padding: 8px 14px;
            color: #c0d0e0;
            font-style: italic;
            margin-bottom: 10px;
        ">
            🔍 AI-Search... &nbsp;&nbsp;&nbsp; <span style="font-size:0.8em; color:#8aabcc;">⚠️ WIP - Not yet implemented</span>
        </div>
    """, unsafe_allow_html=True)
 #🔵
 # pulls the clusters dictionary out of filesAiTagged.json, if none exist - defaults to empty dictionary
    clusters = sorted_data.get("clusters", {})
    documents = sorted_data.get("documents", {})


#UPDATED THE SECTION: to allow for Linking to the CLusters.

#Loops each cluster and its lists of files, for each one it creates the expander folder. 🔵
    for cluster_name, cluster_data in clusters.items():
        cluster_files = cluster_data.get("documents", [])
        # builds folder titles on the info to add an extra s if plural and file count.
        with streamlit.expander(f"🔵 {cluster_name} Cluster -  ({len(cluster_files)} file{'s'if len(cluster_files) !=1 else''})",expanded=False):
            for filename in cluster_files: 
                doc = documents.get(filename, {})
                btn_col, file_col = streamlit.columns([1, 6])# splits each file row to columns
                with btn_col:
                    icon = "✕" if streamlit.session_state.selected_file == doc else "ℹ️" #checks if info pan is open

                    #Logic for the Button, only opens file if file isn't open, and closes other files info panel if they are open.
                    if streamlit.button(icon, key=f"sel_{filename}"):
                        if streamlit.session_state.selected_file == doc:
                            streamlit.session_state.selected_file = None
                        else:
                            streamlit.session_state.selected_file = doc
                        streamlit.rerun() #forces page refresh
                with file_col:
                    streamlit.markdown(f"📄 {filename}") #renders name in details - f-stringSonnet 4.6


#MISC FOLDER SECTION: 
    #Similar to previous but renders a Misc file section for unable to sort. 
    misc_files = sorted_data.get("misc", [])
    #Same as before creating collapsible drop down
    with streamlit.expander(f"❓ Misc (Unable to Sort)  ({len(misc_files)} file{'s'if len(misc_files) !=1 else ''})",expanded=False):
        if misc_files:#looks for misc files
            for file in misc_files: #loops for each
                btn_col, file_col = streamlit.columns([1, 6])
                with btn_col:
                    icon = "✕" if streamlit.session_state.selected_file == file else "ℹ️" #same as before
                    #same logic looking for opened details panels closing and opening its own etc.
                    if streamlit.button(icon, key=f"misc_{file['original_name']}"):
                        if streamlit.session_state.selected_file == file:
                            streamlit.session_state.selected_file = None
                        else:
                            streamlit.session_state.selected_file = file
                        streamlit.rerun()
                with file_col:
                    streamlit.markdown(f"📄 {file['original_name']}") #setting name of files
        else:
            streamlit.caption("No miscellaneous files.") #preferably the app shows this majority of the time.
# |===================================================================|

# |============== UNSORTED REPOSITORY (WIP)
# Work In Progress, Need to create this section, for now flat file list will do. 
elif streamlit.session_state.viewMode == "Unsorted Repository":

    # Flat file list in upload order for now
    if uploaded_files:
        for uf in uploaded_files:
            streamlit.markdown(f"📄 {uf.name}")
    else:
        streamlit.info("📂 No files uploaded yet.")

# |============== ACTIVITY LOG (WIP)
elif streamlit.session_state.viewMode == "Runtime Application Report":

    # placeholder this is WORK In Progress.
    streamlit.markdown("""
        <div style="
            background-color: #1a2a3a;
            border: 1px solid #3a5a7a;
            border-radius: 8px;
            padding: 12px;
            font-family: monospace;
            color: #a0c0e0;
            font-size: 0.85em;
        ">
            <p>⏳ Waiting for activity...</p>
            <p style="color:#8aabcc; font-style:italic;">Logs will appear here once categorisation begins.</p>
        </div>
    """, unsafe_allow_html=True)

#   |                    End of Right Side Directory Panel                       |
#   |____________________________________________________________________________|  

 
#                    |                                                                         |
#                   |||                                                                       |||
#                  |||||                                                                     |||||
#                  |||||                   END OF  DIRECTORY PANEL SECTION                   |||||
#                  |||||                                                                     |||||
#                   |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                    |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                      |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                        |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                           |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                               |||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                                    |||||||||||||||||||||||||||||||||||||||||||||||
#                                          |||||||||||||||||||||||||||||||||||
#                                                 |||||||||||||||||


#Adjusting Widths So When Details Panel is Selected or Not the Folder Panel (Directory) fits to the screen




#                                                 |||||||||||||||||
#                                          |||||||||||||||||||||||||||||||
#                                    |||||||||||||||||||||||||||||||||||||||||||
#                               |||||||||||||||||||||||||||||||||||||||||||||||||||||
#                           |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                        |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                      |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                    |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                   |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                  |||||                                                                     |||||
#                  |||||                          FILE DETAILS PANEL                         |||||
#                  |||||                (Small Section for Extended File Info)               |||||
#                   |||                                                                       |||
#                    |                                                                         |
#                    V                                                                         V

#This checks if the I info button has been selected.
if streamlit.session_state.selected_file:
    file = streamlit.session_state.selected_file

    #UPDATED file info section for new format, This section gives the UI for the Info. 
    streamlit.markdown(f"""
        <div style="
            position: fixed;
            top: 230px; 
            right: 40px;
            width: 300px;
            height: 500px;
            background-color: #1a2a3a;
            border: 2px solid #2952a3;
            border-radius: 8px;
            padding: 16px;
            z-index: 9999;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            overflow-y: auto;
            color: white;
        ">
            <h4 style="color:#7aafd4; margin-top:0;">{file.get('metadata', {}).get('filename', 'Unknown')}</h4>
            <hr style="border-color:#2952a3;">
            <p><b>🤖 AI Description:</b><br>{file.get('rationale') or 'N/A'}</p>
            <p><b>📄 File Type:</b> {file.get('metadata', {}).get('extension', 'Unknown')}</p>
            <p><b>💾 File Size:</b> {round(file.get('metadata', {}).get('size_bytes', 0) / 1024, 1)} KB</p>
            <p><b>Word Count:</b> {file.get('metadata', {}).get('word_count', 0)} words</p>
            <p><b>Date Added:</b> {file.get('addDate', 'Unknown')}</p>
            <p><b>⏱Processing Time:</b> {file.get('totTime', 0)}s</p>
            <p><b>🏷️ Tags:</b><br>{', '.join(file.get('tags', []))}</p>
            <p><b>🚩 App Report Flags:</b><br>
                <span style="color:{'#e53935' if file.get('error') else '#4caf50'}">
                    {file.get('error') or 'NONE'}
                </span>
            </p>

            <p><b>📁 Original Path:</b><br>
                <span style="color:#8aabcc; font-style:italic;">⚠️ WIP - Not yet implemented</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

#                   |                                                                         |
#                   |||                                                                       |||
#                  |||||                                                                     |||||
#                  |||||                   END OF  DIRECTORY PANEL SECTION                   |||||
#                  |||||                                                                     |||||
#                   |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                    |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                      |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                        |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                           |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                               |||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                                    |||||||||||||||||||||||||||||||||||||||||||||||
#                                          |||||||||||||||||||||||||||||||||||
#                                                 |||||||||||||||||