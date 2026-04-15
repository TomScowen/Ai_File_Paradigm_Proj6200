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


# IMPORT LIST ----> 
import streamlit # for building the user interface
import sys # pythons built in sys library (needs to be modified python path for core folder)
import os # pythons built-in operating system (needs to build file path for core folder)

#getting path of current "__file__", getting the directory containing it from the OS and joining the path with the core for full
#path to core folder. The insert adds the path to the pythons search list (so imports work correctly from core)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "core")) 
# ^ useful links: https://docs.python.org/3/library/sys.html#sys.path + https://docs.python.org/3/library/os.path.html

#Importing from phase 2 and 3...
#from documentParsing import parse_Doc
#from documentCategoriser import categorise_Doc

#Temp File Import, for file to upload as in-memory objects.
import tempfile

#__________________________________________________                          _______________________
# APP UI BUILDING --->                             |                        |Colour Codes:  
# docs.streamlit.io                                |                        |vry light grey: #f0f0f0                   
# docs.streamlit.io/library/api-reference          |                        |grey: #d0d0d0                     
# docs.streamlit.io/library/cheatsheet             |                        |darker grey: #a0a0a0
#__________________________________________________|                        |dark grey: #707070
                                                                            #(Colour Spectrum to be changed later.)

#User Interface Configuration 
streamlit.set_page_config(
    page_title="Ai-Driven File Paradigm Application",
    page_icon="🗂️",
    layout="wide" #maybe need to change to be a specific size or changeable depending on device being used...
    )


#hide the streamlit default features: (TEMPORARILY DISABLED)
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



#https://developer.mozilla.org/en-US/docs/Web/CSS - Good link for CSS information. 
# UI Skeleton Layout
# 1) Left Control Panel, 2) Main Folder Panel. 3) Pop Up Details Panel. 


# -------------> HEADER #(Need 2 Features In this later, Updating last sorted and updated name when switching between modes.)
streamlit.markdown("""
    <div style="
        background-color: #a0a0a0;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-left: -5rem;
        margin-right: -5rem;
        margin-top: -2rem;
        margin-bottom: 15px;
        border: 2px solid #707070
    ">
        <span style="color: white; font-size: 1.2em; font-weight: bold; font-style: italic;">
            🗂️ AI-Sorted Repository
        </span>
        <span style="color: white; font-style: italic; font-size: 0.85em;">
            Last Sorted... Not yet sorted
        </span>
    </div>
""", unsafe_allow_html=True)
# _______________________________________________________________________________________
#|------------> CONTROL PANEL HEADER (Final) <-------------------------------------------|
with streamlit.sidebar:
    streamlit.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
    streamlit.markdown("""
        <div style="
            background-color: #a0a0a0;
            padding: 11px 14px;
            margin-left: -0.98rem;
            margin-right: -0.98rem;
            margin-top: -2rem;
            margin-bottom:-1px;
            border: 2px solid #707070;
        ">
            <span style="color: white; font-size: 1.1em; font-weight: bold;">
                ⚙️ AI-Driven File Paradigm APP
            </span>
        </div>
    """, unsafe_allow_html=True)


# Details Panel Pop Up Selection.
if "selected_file" not in streamlit.session_state: #this means that it won't show unless selected.
    streamlit.session_state.selected_file=None



# Panel 1

#Fixing allignment of the Upload File Box.
streamlit.markdown("""
    <style>
        [data-testid="stFileUploaderDropzone"] {
            text-align: center;
     }
     [data-testid="stFileUploader"] label {
         text-align: center;
         width: 100%;
            display: block;
            font-weight: bold;
     }
    /* Centre browse files button */
    [data-testid="stFileUploaderDropzone"] button {
        display: block;
        margin: 0 auto;
    }
    /* Hide the drag and drop text, keep just the button */
    [data-testid="stFileUploaderDropzoneInstructions"] {
       display: none;
    }
        </style>
    """, unsafe_allow_html=True)

with streamlit.sidebar:
    streamlit.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
        
    #Runs the sorting
    streamlit.button("▶  Run AI-Categorising", use_container_width=True)
    #For future loading bar...
    loading_placeholder = streamlit.empty()

    
  # Upload File Box.
    streamlit.markdown("<div style='text-align:center; font-size: 3em;'>📄</div>", unsafe_allow_html=True)
    uploaded_files = streamlit.file_uploader(
        "Upload Files",
        accept_multiple_files=True,
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed"
    )

    






#Adjusting Widths So When Details Panel is Selected or Not the Folder Panel (Directory) fits to the screen


col2, col3 = streamlit.columns([3, 1])
# Panel 2


# Panel 3


# Temporary test button - remove later
if streamlit.button("Test Detail Panel"):
    if streamlit.session_state.selected_file:
        streamlit.session_state.selected_file = None
    else:
        streamlit.session_state.selected_file = "test"
    streamlit.rerun()

if streamlit.session_state.selected_file:
    #Config for Detail Panel
    streamlit.markdown("""
        <div style="
            position: fixed;
            top: 230px; 
            right: 40px;
            width: 300px;
            height: 400px;
            background-color: #a0a0a0;
            border: 3px dashed #ccc;
            border-color: #707070;
            border-radius: 8px;
            padding: 16px;
            z-index: 9999;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        ">
            EXT INFORMATION PANEL
        </div>
    """, unsafe_allow_html=True)



