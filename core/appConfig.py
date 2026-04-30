#  ___________________________________________________________________
# |=-=-=-=-=-=-=-=-=-=-=-=-=-| CONFIG LIST |-=-=-=-=-=-=-=-=-=-=-=-=-=|
# | This File is for storing my tweakable CONFIGERATIONS for Testing  |
# |                                                                   |
#  \_________________________________________________________________/  

MIN_CHARACTER_INPUTS = 50 # Parsing Mininun threshold to use text of document. (50 Words)

MAX_CHARACTER_INPUTS = 1500 #Amount of Characters sent to Mistral,
MAX_NEW_TOKENS = 100 #Mistrals Response Length.
TEMPERATURE = 0.3 #Creativity of Response, low score means its focused, higher score means its more creative.
PROCESSING_MODE = "balanced" # "fast", "balanced", "thorough". (This is for later UI Estimated Time Selection.)
                             # to select how long you would roughly like to spend categorising documents.
TOKENS_PER_DOC_FORCLUSTER = 50 #Per each Doc this many tokens can be used to cluster the repository. 


