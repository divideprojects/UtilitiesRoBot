from google_trans_new import google_translator
from kantex import Section

translator = google_translator()


def translate(text: str, toLanguage: str = "en"):
    translated = translator.translate(text, lang_tgt=toLanguage)
    language = translator.detect(text)
    return str(
        Section(
            f"Translated from {language} to {toLanguage}",
            f"{translated}",
        )
    )
