from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

tokenizer = AutoTokenizer.from_pretrained("tokenizer2", model_max_length=10000000)
model = AutoModelForTokenClassification.from_pretrained("model2")

def drug_search(sentence):
    effect_ner_model = pipeline(task="ner", model=model, tokenizer=tokenizer)
    val = effect_ner_model(sentence)

    result = []
    curr = ""

    for x in val:
        if x["entity"] == "LABEL_1":
            curr = x["word"]
        elif x["entity"] == "LABEL_2":
            curr += x["word"][2:]
        elif curr != "":
            result.append(curr)
        res = [*set(result)]
    return (res)


'''share/
HF_DATASETS_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
python3 main.py --pytorch_model.bin t5-small

'''