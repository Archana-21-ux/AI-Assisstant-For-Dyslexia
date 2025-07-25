from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load the model and tokenizer
model = T5ForConditionalGeneration.from_pretrained("t5-small")
tokenizer = T5Tokenizer.from_pretrained("t5-small")

def simplify_text(text):
    input_text = "simplify: " + text
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    
    output_ids = model.generate(input_ids, max_length=150, num_beams=4, early_stopping=True)
    simplified_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return simplified_text
