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

#______________
# Details Panel Pop Up Selection.
if "selected_file" not in streamlit.session_state: #this means that it won't show unless selected.
    streamlit.session_state.selected_file=None

#by Default AI-Sorted Repository is selected.
if "viewMode" not in streamlit.session_state:
    streamlit.session_state.viewMode = "AI-Sorted Repository"

#to Set the View Title:
viewModeTitle = streamlit.session_state.viewMode
#---------------

#Locks the Control Panel to Fixed Size:
streamlit.markdown("""
<style>
    [data-testid="stSidebar"] {
        min-width: 295px !important;
        max-width: 295px !important;
    }
    [data-testid="stSidebarResizer"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)




# -------------> HEADER #(Need 2 Features In this later, Updating last sorted and updated name when switching between modes.)
streamlit.markdown(f"""
    <div style="
        background-color: #a0a0a0;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-left: -5rem;
        margin-right: -5rem;
        margin-top: -3rem;
        margin-bottom: 15px;
        border: 2px solid #707070
    ">
        <span style="color: white; font-size: 1.2em; font-weight: bold; font-style: italic;">
            🗂️ {viewModeTitle}
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
            margin-top: -2.5rem;
            margin-bottom:-5rem;
            border: 2px solid #707070;
        ">
            <span style="color: white; font-size: 1.1em; font-weight: bold;">
                ⚙️ AI-Driven File Paradigm APP
            </span>
        </div>
    """, unsafe_allow_html=True)



# Panel 1
with streamlit.sidebar:
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
    </style>
    """, unsafe_allow_html=True)
    # Run Button
    streamlit.button("▶  Run AI-Categorising", use_container_width=True)
    
    # Loading Bar
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
    # Upload File Box
    uploaded_files = streamlit.file_uploader(
        "📂 Upload Files",
        accept_multiple_files=True,
        type=["pdf", "docx", "txt"],
    )
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

# CSS border around the mode:
    streamlit.markdown("""
    <style>
      div[data-testid="stRadio"] {
          background-color: #eef2f7;
          border: 2px solid #4a7ab5;
         border-radius: 6px;
         padding: 10px;
         margin-top: -20px;
         margin-right: -14.8rem;
        
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

# Repository Mode Selection
    streamlit.radio(
        "Repository View",
     [
           "AI-Sorted Repository",
            "Unsorted Repository",
            "Runtime Application Report"
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
        "⚡ Processing Mode ⚡",
        [
            "Fast",
            "Balanced",
            "Thorough"
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

    #Adding the download button to streamlit
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

    #This adds the download button features. (probably need a unique code generator and date for file name.)
    streamlit.download_button(
     label="⬇ Download New Repository",
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


if streamlit.session_state.viewMode == "AI-Sorted Repository":

    streamlit.markdown("### AI-Sorted Repository Frame")
    # future:
    # show sorted folders

elif streamlit.session_state.viewMode == "Unsorted Repository":

    streamlit.markdown("### Unsorted Repository Frame")
    # future:
    # show raw upload order

elif streamlit.session_state.viewMode == "Runtime Application Reports":

    streamlit.markdown("### Runtime Application Reports Frame")
    # future:
    # show logs / terminal output

#   |                       End of Select View Feature                           |
#   |____________________________________________________________________________|   





















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



