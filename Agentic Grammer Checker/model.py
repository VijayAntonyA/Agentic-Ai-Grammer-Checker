from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load model (runs locally, first time takes time ⏳)
model_name = "vennify/t5-base-grammar-correction"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def correct_with_ai(text):
    input_text = "grammar: " + text

    inputs = tokenizer.encode(
        input_text, return_tensors="pt", max_length=512, truncation=True)

    outputs = model.generate(
        inputs,
        max_length=512,
        num_beams=5,
        early_stopping=True
    )

    corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return corrected_text
