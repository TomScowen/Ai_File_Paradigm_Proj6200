

AI Driven File Paradigm Application
#----------------------------------#
6200COMP Final Year Project - Thomas Scowen

Overview:
#---------------------------->
A prototype AI-Driven file organisation system, which uses LLM - Mistral7B to automatically
tag, describe and cluster uploaded documents into a semantically meaningful group with 0 manual input. 
(Files can exist in multiple clusters)

-1: Documents are uploaded & parsed to extract text
-2: Mistral7B generates semantic tags for each document and a description.
-3: Tags and Descriptions are used to cluster documents into meaningful groups on shared themes.
-4: Results are displayed in an interactive UI with per-document metadata. 

Requirements:
1: Internet access for downloading packages (mistral7B)
2: Python 3.10 or higher — [Download here](https://www.python.org/downloads/)
3: 16GB Ram Recommended (Min)
4: GPU is recommended for MUCH faster speeds:
                **For NVIDIA GPU users** - Install CUDA Toolkit from
                                            [developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads)
                                            for GPU acceleration. (OPTIONAL but Recommended)

Setup & Installation:

**FIRST TIME SETUP**
# Step 1 - DOWNLOAD the Project
Download this repositoriy to your computer from **github**. 

# Step 2 - Open a Terminal
- **Mac** - Open Terminal (Cmd + Space, type "Terminal")
- **Windows** - Open Command Prompt (Start menu, Type "cmd")

# Step 3: Navigate to the Project folder
cd 'path/to/Ai_File_Paradigm_Proj6200'
                                      > **REPLACE path/to with the actual location you downloaded the project to**
                                      > **Mac** will Look Something like this: cd /Users/username/Downloads/Ai_File_Paradigm_Proj6200
                                      > **Windows** will look something like this: cd C:\Users\username\Downloads\Ai_File_Paradigm_Proj6200
Type this command in the terminal. 

# Step 4: Run Setup Script in Terminal:
python setup.py 
                > **This will automattically handle / install packages and launch the app**
                        * Alternatively you can install all the requirements from either requirements-mac or requirements-win.txt
                        * And run: streamlit run fileParadigm.App.py 
                        * (though this method is more likely to break from human error)




        

This will create the virtual 
