import os
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def main():
    model_name = "facebook/nllb-200-distilled-600M"
    print(f"Loading tokenizer for {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    print(f"Loading model for {model_name} (using CPU)...")
    # Load model on CPU
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    text = "Gradient descent is an optimization algorithm used to minimize some function by iteratively moving in the direction of steepest descent."
    print(f"\nOriginal text (EN):\n{text}\n")
    
    # Target language is Vietnamese (vie_Latn)
    target_lang = "vie_Latn"
    
    print("Tokenizing input text...")
    inputs = tokenizer(text, return_tensors="pt")
    
    print("Generating translation...")
    # Generate translation by forcing target language
    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_lang),
        max_length=128
    )
    
    print("Decoding translation...")
    translation = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    
    print(f"\nTranslated text (VI - NLLB Baseline):\n{translation}\n")

if __name__ == "__main__":
    main()
