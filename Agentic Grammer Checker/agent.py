from model import correct_with_ai
import re
from tools import (
    check_grammar,
    check_consistency,
    improve_sentence_structure,
    fix_names,
    normalize_slang,
    basic_cleanup
)

def agent_process(text):
    original_text = text

    consistency_issues = check_consistency(original_text)
    steps = []
    # Step 1: Normalize slang (only if needed)
    if any(word in text.lower() for word in ["u", "ur", "wht", "r", "dont", "cant"]):
        text = normalize_slang(text)
        steps.append("Slang normalized")
    # Step 2: Cleanup
    if "ver" in text:
        text = basic_cleanup(text)
        steps.append("Basic cleanup applied")

    # Step 3: Line-by-line grammar correction
    lines = text.splitlines()

    # If no real line breaks, fallback to sentence splitting
    if len(lines) == 1:
        lines = re.split(r'(?<=[.!?])\s+', text)

    corrected_lines = []
    all_issues = []

    for line in lines:
        if line.strip() == "":
            corrected_lines.append("")
            continue

        sentences = re.split(r'(?<=[.!?]) +', line)

        corrected_sentences = []

        for sentence in sentences:
            result = check_grammar(sentence)
            corrected_sentence = result["corrected"]

            # ✅ FIX punctuation INSIDE loop
            if not corrected_sentence.endswith((".", "!", "?")):
                corrected_sentence += "."

            corrected_sentences.append(corrected_sentence)
            all_issues.extend(result["issues"])

        # ✅ Build line AFTER sentence loop
        corrected_line = " ".join(corrected_sentences)

        corrected_lines.append(corrected_line)

    # ✅ FINAL TEXT (VERY IMPORTANT)
    corrected_text = "\n".join(corrected_lines)

    steps.append("Grammar checked (line-by-line)")
  
    # Step 4: Scoring
    grammar_count = len(all_issues)
    consistency_count = len(consistency_issues)

    score = 100 - (grammar_count * 5) - (consistency_count * 3)

    if score < 0:
        score = 0
    
    print("DEBUG OUTPUT:")
    print(repr(corrected_text))
    return {

    "original": original_text,
    "corrected": corrected_text,    
    "grammar_issues": all_issues,
    "consistency_issues": consistency_issues,
    "score": score,
    "steps": steps
}