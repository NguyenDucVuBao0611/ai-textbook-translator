import os
import csv
import torch
import sacrebleu
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def main():
    csv_path = os.path.join("data", "handmade_pairs.csv")
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} does not exist.")
        return
        
    # Read sentences from CSV
    sentences = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sentences.append({
                "english": row["english"],
                "literal": row["vietnamese_literal"],
                "rewrite": row["vietnamese_rewrite"]
            })
            
    print(f"Read {len(sentences)} sample sentences from dataset.")
    
    # Load model
    model_name = "facebook/nllb-200-distilled-600M"
    print(f"Loading NLLB model and tokenizer ({model_name})...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    predictions = []
    literals = []
    rewrites = []
    
    target_lang = "vie_Latn"
    
    print("\nStarting batch translation evaluation...")
    for idx, item in enumerate(sentences, 1):
        en_text = item["english"]
        print(f"[{idx}/{len(sentences)}] Translating: '{en_text[:40]}...'")
        
        inputs = tokenizer(en_text, return_tensors="pt")
        translated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_lang),
            max_length=128
        )
        translation = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        
        predictions.append(translation)
        literals.append(item["literal"])
        rewrites.append(item["rewrite"])
        
    print("\nTranslations completed. Calculating BLEU scores...")
    
    # Compute BLEU score against literal references
    bleu_literal = sacrebleu.corpus_bleu(predictions, [literals])
    print(f"\n📊 BLEU score against Literal reference: {bleu_literal.score:.2f}")
    
    # Compute BLEU score against rewrite references
    bleu_rewrite = sacrebleu.corpus_bleu(predictions, [rewrites])
    print(f"📊 BLEU score against Rewrite (Beginner) reference: {bleu_rewrite.score:.2f}")
    
    # Print sample comparison
    print("\n=== Sample Translation Comparison ===")
    print(f"EN Source: {sentences[0]['english']}")
    print(f"NLLB Baseline VI: {predictions[0]}")
    print(f"Literal Ref: {literals[0]}")
    print(f"Rewrite Ref: {rewrites[0]}\n")

if __name__ == "__main__":
    main()
