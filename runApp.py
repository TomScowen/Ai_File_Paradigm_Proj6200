#  ___________________________________________________________________
# |=-=-=-=-=-=-=-=-=-=-=-=| APP LAUNCH PHASE |=-=-=-=-=-=-=-=-=-=-=-=|
# |           This section uses PyWebView to wrap the streamlit      |
# |     thus that can open the app as a desktop window instead of    |
# |                 opening the app within a browser.                |
#  \________________________________________________________________/

#Import list For PyWebView
import subprocess
import threading # runs things simultaneously (currently not working)
import time 
import webview #PyWebView (creates desktop window by wrapping streamlits browser engine)


def phase4Streamlit():
    subprocess.Popen([ #lets python launch and control other programs in script (lets it use streamlit in background)
        "streamlit", "run", "fileParadigmApp.py", "--server.headless","true"
    ])

thread = threading.Thread(target=phase4Streamlit)
thread.daemon = True
thread.start()

time.sleep(5) #gives time for streamlit to start.

#window aspects
webview.create_window(
    "AI-Driven File Paradigm",
    "http://localhost:8501",
    width=1200,
    height=800,
    resizable=True,
    min_size=(900, 800) #Prevents Window from becoming to small.
)

webview.start() #lets hope this actually runs