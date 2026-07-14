import re

def split_paragraph_into_sentences(paragraph: str) -> list:
    """
    Splits a paragraph into a list of sentences using regex.
    """
    # Split on period, exclamation, or question mark followed by space or end of string
    sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())
    return [s for s in sentences if s]

def chunk_text(text: str, max_words: int = 120) -> list:
    """
    Splits a long string into a list of chunks, keeping paragraphs intact if possible,
    but splitting them into groups of sentences if a paragraph exceeds max_words.
    """
    if not text.strip():
        return []
        
    paragraphs = text.split("\n\n")
    chunks = []
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        words_count = len(para.split())
        if words_count <= max_words:
            # Paragraph is short enough, keep it as a single chunk
            chunks.append(para)
        else:
            # Paragraph is too long, split it into sentences and group them
            sentences = split_paragraph_into_sentences(para)
            current_chunk = []
            current_words = 0
            
            for sentence in sentences:
                sentence_words = len(sentence.split())
                if current_words + sentence_words <= max_words:
                    current_chunk.append(sentence)
                    current_words += sentence_words
                else:
                    if current_chunk:
                        chunks.append(" ".join(current_chunk))
                    current_chunk = [sentence]
                    current_words = sentence_words
                    
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                
    return chunks
