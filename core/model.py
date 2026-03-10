


# ---| MODEL IMPORTS |---#
# 1)Loads the Mistral Model, 2)Converts Txt Into numbers the model understands.
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch #PyTorch is The deep learning library everything runs on. 

model_name = "mistralai/Mistral-7B-Instruct-v0.3" #String of model name

#---| LOAD THE MODEL |---#
print("Loading tokeniser...") #Load Note

#loading the tokeniser from local hugging face cache. 
tokenizer = AutoTokenizer.from_pretrained(model_name) 
#loads all parameters from local cache, weights stored in 16 bit to save memory.
model = AutoModelForCausalLM.from_pretrained(model_name,
                                             dtype=torch.float16, #torch_dtype=torch.float16, <-- Doesn't Work
                                             device_map="auto") # auto assigns model layers to available hardware. (important)

print("Model Loaded! test prompt....") #Load Note

# Mistral Syntax at: 
# Using Mistral intruction format. [INST] tags wrap the users msg. (tells model its an instruction)
prompt = "[INST] What category would you give a document about company financial reports? [/INST]"

# Converts prompt string into num token ids. 
inputs = tokenizer(prompt, return_tensors="pt", padding=True).to(model.device)
# Generates response from the input. 
outputs = model.generate(
    input_ids=inputs["input_ids"],
    attention_mask=inputs["attention_mask"],
    max_new_tokens=100, #limter on response to 100 new tokens.
    pad_token_id=tokenizer.eos_token_id 
)

# Converts the output token IDS back to human txt. (decoding)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("Response: ", response) #Printing Response. 