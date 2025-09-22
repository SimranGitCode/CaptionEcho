import re
import requests
 
TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"
 
NON_LATIN_LANGS = {"hi", "te", "bn", "ta", "kn", "ml", "mr", "gu", "or", "pa", "si", "ur"}

def normalize_caption_text(s: str) -> str: 
    if not s:
        return s
    s = s.replace("Ġ", " ").replace("▁", " ").replace("##", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s

def looks_mixed_script(s: str, target_lang: str) -> bool: 
    if not s or target_lang not in NON_LATIN_LANGS:
        return False
    return bool(re.search(r"[A-Za-z]", s))

def postclean_non_latin(s: str) -> str: 
    s = re.sub(r"\b[a-zA-Z]{1,4}\b", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def translate_caption(text: str, target_lang: str) -> str: 
    text = normalize_caption_text(text)
    try:
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": target_lang,
            "dt": "t",
            "q": text
        }
        resp = requests.get(TRANSLATE_URL, params=params, timeout=6)
        resp.raise_for_status()
        data = resp.json()
        translated = "".join(seg[0] for seg in data[0] if seg and seg[0])
        translated = normalize_caption_text(translated)

        if looks_mixed_script(translated, target_lang):
            return postclean_non_latin(translated)
        return translated
    except Exception as e:
        return f"Translation Error: {str(e)}"

