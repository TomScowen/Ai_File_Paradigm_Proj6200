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
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch #PyTorch is The deep learning library everything runs on. 

model_name = "mistralai/Mistral-7B-Instruct-v0.3" #String of model name

#---| LOAD THE MODEL |---#
print("Loading tokeniser...") #Load Note

#loading the tokeniser from local hugging face cache. 
tokenizer = AutoTokenizer.from_pretrained(model_name) 
tokenizer.pad_token = tokenizer.eos_token 
#loads all parameters from local cache, weights stored in 16 bit to save memory.
model = AutoModelForCausalLM.from_pretrained(model_name,
                                             dtype=torch.float16, #torch_dtype=torch.float16, <-- Doesn't Work
                                             device_map="auto") # auto assigns model layers to available hardware. (important)

print("Model Loaded!") #Load Note



