import language_tool_python
import re

tool = language_tool_python.LanguageTool('en-US')

def check_grammar(text):
    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
        
    issues = []

    for match in matches:
        issues.append({
            "message": match.message,
            "suggestion": match.replacements[0] if match.replacements else "",
            "error_text": text[match.offset: match.offset + match.error_length]
        })

    return {
        "original": text,
        "corrected": corrected_text,
        "issues": issues
    }
    
def improve_sentence_structure(text):
    text = text.strip()

    # Capitalize first letter
    if text:
        text = text[0].upper() + text[1:]

    # Add punctuation
    if text and text[-1] not in ".!?":
        text += "."

    return text

def fix_names(text):
    words = text.split()

    fixed_words = []
    for word in words:
        # simple rule: capitalize if it's a proper noun candidate
        if word.lower() in ["india", "tamilnadu", "chennai", "john", "rahul"]:
            fixed_words.append(word.capitalize())
        else:
            fixed_words.append(word)

    return " ".join(fixed_words)

def check_consistency(text):
    issues = []

    if " u " in text or text.startswith("u "):
        issues.append("Use 'you' instead of 'u'")

    if "dont" in text:
        issues.append("Use 'don't' instead of 'dont'")

    if text.islower():
        issues.append("Sentence should start with capital letter")

    return issues

def normalize_slang(text):
    slang_dict = {
        "u": "you",
        "ur": "your",
        "r": "are",
        "ar": "are",
        "wht": "what",
        "fr": "for",
        "dont": "don't",
        "cant": "can't",
        "im": "I'm"
    }

    words = text.split()
    new_words = []

    for word in words:
        clean = word.lower()
        if clean in slang_dict:
            new_words.append(slang_dict[clean])
        else:
            new_words.append(word)

    return " ".join(new_words)

def basic_cleanup(text):
    # Fix common words
    text = text.replace("ver", "very")
    return text