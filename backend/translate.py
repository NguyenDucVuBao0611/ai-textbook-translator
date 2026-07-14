import os
import csv
import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from dotenv import load_dotenv

# Load env configurations
load_dotenv()

class TranslationCoordinator:
    def __init__(self):
        # Load model identifiers from .env or default to the NLLB base model
        self.stage1_model_id = os.getenv("HF_MODEL_STAGE1", "facebook/nllb-200-distilled-600M")
        self.stage2_model_id = os.getenv("HF_MODEL_STAGE2", None)  # None by default in Option A
        
        print(f"Initializing Stage 1 Translation Model: {self.stage1_model_id}")
        self.tokenizer_s1 = AutoTokenizer.from_pretrained(self.stage1_model_id)
        self.model_s1 = AutoModelForSeq2SeqLM.from_pretrained(self.stage1_model_id)
        
        self.tokenizer_s2 = None
        self.model_s2 = None
        
        # Load Stage 2 model if specified (only once the user trains and uploads it)
        if self.stage2_model_id:
            try:
                print(f"Initializing Stage 2 Rewrite Model: {self.stage2_model_id}")
                self.tokenizer_s2 = AutoTokenizer.from_pretrained(self.stage2_model_id)
                self.model_s2 = AutoModelForSeq2SeqLM.from_pretrained(self.stage2_model_id)
            except Exception as e:
                print(f"Warning: Could not load Stage 2 model ({e}). Using rule-based glossary fallback.")
                
        # Load glossary from data/glossary.csv
        self.glossary = self.load_glossary()
        
    def load_glossary(self) -> list:
        glossary = []
        glossary_path = os.path.join("data", "glossary.csv")
        if os.path.exists(glossary_path):
            try:
                with open(glossary_path, mode="r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        glossary.append({
                            "english": row["english"].strip(),
                            "academic": row["vietnamese_academic"].strip(),
                            "beginner": row["vietnamese_beginner"].strip(),
                        })
                # Sort terms by length in descending order to mask longer phrases first
                glossary.sort(key=lambda x: len(x["english"]), reverse=True)
                print(f"Loaded {len(glossary)} glossary terms for replacement.")
            except Exception as e:
                print(f"Error loading glossary: {e}")
        return glossary

    def mask_terms(self, text: str) -> tuple:
        """
        Finds English terms in the source text, masks them with __TERM_i__,
        and returns the masked text along with a mapping dict.
        """
        masked_text = text
        mask_map = {}
        
        for idx, item in enumerate(self.glossary):
            term = item["english"]
            # Search for term as a whole word case-insensitively using word boundaries (\b)
            pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
            
            if pattern.search(masked_text):
                mask_tag = f"__TERM_{idx}__"
                masked_text = pattern.sub(mask_tag, masked_text)
                mask_map[mask_tag] = item
                
        return masked_text, mask_map

    def unmask_terms(self, translated_text: str, mask_map: dict, mode: str) -> str:
        """
        Replaces the masks (__TERM_i__) in the translated text with the appropriate
        Vietnamese translation based on the mode (Academic or Beginner).
        Handles optional spaces and case variations introduced by the translation engine.
        """
        text = translated_text
        
        # Regex to match the mask dynamically: __TERM_i__, __term_i__, __ TERM_i __ etc.
        pattern = re.compile(r"__\s*TERM_(\d+)\s*__", re.IGNORECASE)
        
        def replace_match(match):
            idx = int(match.group(1))
            mask_tag = f"__TERM_{idx}__"
            
            if mask_tag in mask_map:
                item = mask_map[mask_tag]
                return item["academic"] if mode == "academic" else item["beginner"]
            return match.group(0)
            
        return pattern.sub(replace_match, text)

    def translate_sentence(self, text: str, mode: str = "academic") -> str:
        """
        Translates a single sentence from English to Vietnamese.
        Applies Terminology Masking before NLLB translation and Unmasking after.
        """
        if not text.strip():
            return ""
            
        # 1. Mask English terms in the source sentence
        masked_text, mask_map = self.mask_terms(text)
        
        # 2. Translate the masked text using Stage 1 (NLLB)
        target_lang = "vie_Latn"
        inputs = self.tokenizer_s1(masked_text, return_tensors="pt")
        
        with torch.no_grad():
            translated_tokens = self.model_s1.generate(
                **inputs,
                forced_bos_token_id=self.tokenizer_s1.convert_tokens_to_ids(target_lang),
                max_length=128
            )
        s1_translation = self.tokenizer_s1.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        
        # 3. Stage 2: Explanatory Rewrite (if Beginner and Stage 2 model is present)
        if mode == "beginner" and self.model_s2 and self.tokenizer_s2:
            inputs_s2 = self.tokenizer_s2(s1_translation, return_tensors="pt")
            with torch.no_grad():
                rewritten_tokens = self.model_s2.generate(
                    **inputs_s2,
                    forced_bos_token_id=self.tokenizer_s2.convert_tokens_to_ids(target_lang),
                    max_length=128
                )
            translation = self.tokenizer_s2.batch_decode(rewritten_tokens, skip_special_tokens=True)[0]
        else:
            translation = s1_translation
            
        # 4. Unmask terms with the final translation values
        final_translation = self.unmask_terms(translation, mask_map, mode)
        
        return final_translation

if __name__ == "__main__":
    coordinator = TranslationCoordinator()
    text = "Gradient descent is an optimization algorithm used to minimize some function by iteratively moving in the direction of steepest descent."
    print(f"\nOriginal (EN): {text}")
    
    academic_tr = coordinator.translate_sentence(text, mode="academic")
    print(f"\nAcademic Translation (VI): {academic_tr}")
    
    beginner_tr = coordinator.translate_sentence(text, mode="beginner")
    print(f"\nBeginner Translation (VI): {beginner_tr}")
