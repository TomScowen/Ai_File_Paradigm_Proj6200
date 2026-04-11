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
from documentParsing import parse_Doc
from documentCategoriser import categorise_Doc

#Temp File Import, for file to upload as in-memory objects.
import tempfile

#__________________________________________________
# APP UI BUILDING --->                                |
# docs.streamlit.io                                |
# docs.streamlit.io/library/api-reference          |
# docs.streamlit.io/library/cheatsheet             |
#__________________________________________________|

#User Interface Configuration 
streamlit.set_page_config(
    page_title="Ai-Driven File Paradigm Application",
    page_icon="🗂️",
    layout="wide" #maybe need to change to be a specific size or changeable depending on device being used...

)

# UI Skeleton Layout
# 1) Left Control Panel, 2) Main Folder Panel. 3) Pop Up Details Panel. 




# Panel 1
with streamlit.sidebar:
    streamlit.write("CONTROL PANEL")
# Panel 2
with streamlit.columns([3, 1]):
    streamlit.write("DIRECTORY PANEL")

# Panel 3
with streamlit.columns([3, 1]):
    streamlit.write("EXT INFORMATION PANEL")





