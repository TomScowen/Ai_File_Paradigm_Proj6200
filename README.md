Author:
Thomas Scowen - 1074249
Liverpool John Moores University
Supervised by Mrs. Janet Lunn
--------------------------------------------------------------------------------------------------------
                                        WARNING READ ME - IMPORTANT
    Mistral7B LLM takes up over 14GB worth of space, installing this program will require you to have
    this space available. 

    This Program can run on most computers however without a GPU or High End Computer the Program takes
    significantly longer to run. (from 10-15minutes per file to 30-60seconds per file)

!!!  There is a Participant C - Test Video Uploaded If You Wish to View the Runnings of the Program  !!!
!!!              Without having to install or test the program yourself.      
                       !!!
if you do run the program, upload your 2-4 files and run them all at once, to save on computer resources.

--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------
AI Driven File Paradigm Application
6200COMP Final Year Project - Thomas Scowen


Overview:
--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------
A prototype AI-Driven file organisation system, which uses LLM - Mistral7B to automatically
tag, describe and cluster uploaded documents into a semantically meaningful group with 0 manual input. 
(Files can exist in multiple clusters)

-1: Documents are uploaded & parsed to extract text
-2: Mistral7B generates semantic tags for each document and a description.
-3: Tags and Descriptions are used to cluster documents into meaningful groups on shared themes.
-4: Results are displayed in an interactive UI with per-document metadata.
--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------
REQUIREMENTS!!!

1: At LEAST 20 GB of Free Storage (LLM's Take Up a Lot of Space)
2: Internet access for downloading packages (mistral7B)
3: Python 3.11 or higher — [Download here](https://www.python.org/downloads/) 
                            Recommended Version: https://www.python.org/downloads/release/python-3119/
4: 16GB Ram Recommended (Min)
5: GPU is recommended for MUCH faster speeds:
                **For NVIDIA GPU users** - Install CUDA Toolkit from
                                            [developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads)
                                            for GPU acceleration. (OPTIONAL but Recommended)
--------------------------------------------------------------------------------------------------------                                   
--------------------------------------------------------------------------------------------------------

Setup & Installation:
--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------
 ###                   **FIRST TIME SETUP**

# Step 1 - DOWNLOAD the Project
Download this repositoriy to your computer from **github**. 

# Step 2 - Open a Terminal
- **Mac** - Open Terminal (Cmd + Space, type "Terminal")
- **Windows** - Open Command Prompt (Start menu, Type "cmd") (Or use search bar at the bottom)

# Step 3: Navigate to the Project folder (Type this with the correct path in Terminal / Command Prompt)
cd 'path/to/Ai_File_Paradigm_Proj6200'
                                      > **REPLACE path/to with the actual location you downloaded the project to**
                                      > **Mac** will Look Something like this: cd /Users/username/Downloads/Ai_File_Paradigm_Proj6200
                                      > **Windows** will look something like this: cd C:\Users\username\Downloads\Ai_File_Paradigm_Proj6200
Type this command in the terminal. 
# Step 4: For Windows: Run These Commands in Ai_File_Paradigm_Proj6200 PATH ^
*1st Run The Line Below: (To Install the virtual environment)*||
py -3.11 -m venv venv 

*2nd Run The Line Below: (To install windows requirements)* ||
venv\Scripts\pip.exe install -r requirements-win.txt --ignore-requires-python

# Step 4: Run Setup Script in Terminal:
python setup.py 
                > **This will automattically handle / install packages and launch the app**
                        * Alternatively you can install all the requirements from either requirements-mac or requirements-win.txt
                        * And run: streamlit run fileParadigm.App.py 
                        * (though this method is more likely to break from human error)
--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------
 ###        **RUNNING AGAIN AFTER SETUP**
 1: In Terminal Run:
        # *For **Mac** / **Linux**:*
            source venv/bin/activate  
        # *For **Windows**:*
            venv\Scripts\activate
 2: In Terminal Run:
        streamlit run fileParadigmApp.py
--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------
IMPORTANT: WHEN USING THE APPLICATION

- The App Currently only supports, .docx, .pdf and .txt (Scanned / Image PDFs can't be parsed, thus error may be added)

- core/appConfig.py allows tweaking properities of the AI (recommended to avoid)

- As the app is being ran locally the program can take up to 15minutes per document on CPUs (depending on hardware), for maximum
  efficiency it is recommended to upload all files at once and the run these at once, to avoid reclustering each time.
    **GPU SIGNIFICANTLY REDUCES THIS TO 30-60 Seconds Per DOCUMENT**

- In the UI which will appear in the web browser, you should upload files in the drop box, then click the >Run AI-Categorising 

- There is a small possibility that Mistral hullucinates file names in the cluster assignments, LLMs are non deterministic which can result in   varied responses. (this only happened once in testing)

.
--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------
Features in Development:
- Ai Semantic Searching
- Dynamic Processing modes, (fast/balanced or thorough, currently set just to thorough)
- Downloading repository as ZIP
- Full Runtime application reports/logs with AI oversight
- Tag Relationship graphs between clusters

*
--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------
                                        KNOWN ISSUES WARNING
- Pythonnet Build Failure: without running the requirements command as listed and ignoring python we can
expect some issues when building the packages

- Python 3.14 compatability: PyTorch isn't available with 3.14, please use 3.11 if this fails. 

- For GPU's - RTX 5060 / newer GPUs: Require nightly PyTorch build with
              cu128 index. Standard cu124 will show compatibility warning.

- When uploading files and running the application on CPU it is likely to take a long time for less powerful computers
  which may lead you to expect the program to be failing.
*
--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------



        
#Important Webpages for Features Used:
Mistral-7B-Instruct-v0.3
HuggingFace Transformers
Streamlit Documentation
PyMuPDF Documentation
Python-docx Documentation
