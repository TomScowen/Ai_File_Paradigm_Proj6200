#Hugging Face Token: (HF Token allows for Higher Rate Limits and Faster Downloads)
#TEMPORARY VERSION:
#export HF_TOKEN=your_token_here  (Paste in Terminal If Using)
#PERMANENT OPTION: 
#echo 'export HF_TOKEN= ' >> ~/.zshrc
#source ~/.zshrc
# ^^^^ MOVE TO READ-ME LATER. 

#  _______________________________________________________
# |=-=-=-=-=-=-=-=-=-=-=| PHASE ONE |=-=-=-=-=-=-=-=-=-=-=|
# | PHASE 1: PREPARING THE MODEL FOR USE.                 |
# | Current: proof of concept.                            |
#  \_____________________________________________________/

# ---| MODEL IMPORTS |---#
# 1)Loads the Mistral Model, 2)Converts Txt Into numbers the model understands.
from transformers import AutoModelForCausalLM, AutoTokenizer, logging
import torch #PyTorch is The deep learning library everything runs on. 
import streamlit #added here for cach decorator

# this suppresses huggingfaces logging output, means our end result doesn't spam the terminal with warnings
import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
logging.set_verbosity_error()

model_name = "mistralai/Mistral-7B-Instruct-v0.3" #String of model name

#wrapping the model loading with streamlits cache system, means mistral only loads 1 time per session
@streamlit.cache_resource 
def loadModel():
    import sys
    import io
    # Suppress tqdm output that causes I/O errors in PyWebView
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    #---| LOAD THE MODEL |---#
    #loading the tokeniser from local hugging face cache. 
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name) 
        tokenizer.pad_token = tokenizer.eos_token 
    #loads all parameters from local cache, weights stored in 16 bit to save memory.
        model = AutoModelForCausalLM.from_pretrained(model_name,
                                                        dtype=torch.float16, #torch_dtype was broken
                                                        device_map="auto")
        return model, tokenizer
    finally:
        sys.stderr= old_stderr #ensures restore if loading fails.
    
model, tokenizer = loadModel()



