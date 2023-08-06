from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import os
from huggingface_hub import hf_hub_download


tokenizer = AutoTokenizer.from_pretrained("/tokenizer2", model_max_length=10000000)
model_path = "./model2"
pytorch_model_url = "https://huggingface.co/ronoys/testDeploy/blob/main/pytorch_model.bin"


def drug_search(sentence):
    
    if not os.path.exists(os.path.join(model_path, "pytorch_model.bin")):
        
        hf_hub_download(repo_id="ronoys/testDeploy", filename="pytorch_model.bin", local_dir = "./model2")

    

    model = AutoModelForTokenClassification.from_pretrained("model2")

    effect_ner_model = pipeline(task="ner", model=model, tokenizer=tokenizer)
    val = effect_ner_model(sentence)

    result = []
    curr = ""

    for x in val:
        if x["entity"] == "LABEL_1":
            curr = x["word"]
        elif x["entity"] == "LABEL_2":
            curr += x["word"][2:]
        else:
            result.append(curr)
        res = [*set(result)]
    while("" in res):
        res.remove("")
    return (res)


'''share/
HF_DATASETS_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
python3 example.py --pytorch_model.bin t5-small

'''
