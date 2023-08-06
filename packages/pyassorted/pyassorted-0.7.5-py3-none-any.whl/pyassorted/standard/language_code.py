from enum import Enum
from typing import Text


class LanguageCode(Enum):
    AMHARIC = ("am", "Amharic")
    ARABIC = ("ar", "Arabic")
    BASQUE = ("eu", "Basque")
    BENGALI = ("bn", "Bengali")
    ENGLISH_UK = ("en-GB", "English (UK)")
    PORTUGUESE_BRAZIL = ("pt-BR", "Portuguese (Brazil)")
    BULGARIAN = ("bg", "Bulgarian")
    CATALAN = ("ca", "Catalan")
    CHEROKEE = ("chr", "Cherokee")
    CROATIAN = ("hr", "Croatian")
    CZECH = ("cs", "Czech")
    DANISH = ("da", "Danish")
    DUTCH = ("nl", "Dutch")
    ENGLISH_US = ("en", "English (US)")
    ESTONIAN = ("et", "Estonian")
    FILIPINO = ("fil", "Filipino")
    FINNISH = ("fi", "Finnish")
    FRENCH = ("fr", "French")
    GERMAN = ("de", "German")
    GREEK = ("el", "Greek")
    GUJARATI = ("gu", "Gujarati")
    HEBREW = ("iw", "Hebrew")
    HINDI = ("hi", "Hindi")
    HUNGARIAN = ("hu", "Hungarian")
    ICELANDIC = ("is", "Icelandic")
    INDONESIAN = ("id", "Indonesian")
    ITALIAN = ("it", "Italian")
    JAPANESE = ("ja", "Japanese")
    KANNADA = ("kn", "Kannada")
    KOREAN = ("ko", "Korean")
    LATVIAN = ("lv", "Latvian")
    LITHUANIAN = ("lt", "Lithuanian")
    MALAY = ("ms", "Malay")
    MALAYALAM = ("ml", "Malayalam")
    MARATHI = ("mr", "Marathi")
    NORWEGIAN = ("no", "Norwegian")
    POLISH = ("pl", "Polish")
    PORTUGUESE_PORTUGAL = ("pt-PT", "Portuguese (Portugal)")
    ROMANIAN = ("ro", "Romanian")
    RUSSIAN = ("ru", "Russian")
    SERBIAN = ("sr", "Serbian")
    CHINESE_PRC = ("zh-CN", "Simplified Chinese")
    SLOVAK = ("sk", "Slovak")
    SLOVENIAN = ("sl", "Slovenian")
    SPANISH = ("es", "Spanish")
    SWAHILI = ("sw", "Swahili")
    SWEDISH = ("sv", "Swedish")
    TAMIL = ("ta", "Tamil")
    TELUGU = ("te", "Telugu")
    THAI = ("th", "Thai")
    CHINESE_TAIWAN = ("zh-TW", "Traditional Chinese")
    TURKISH = ("tr", "Turkish")
    URDU = ("ur", "Urdu")
    UKRAINIAN = ("uk", "Ukrainian")
    VIETNAMESE = ("vi", "Vietnamese")
    WELSH = ("cy", "Welsh")

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, language_code: Text, display_name: Text):
        self.language_code = language_code
        self.display_name = display_name

    @classmethod
    def from_language_code(cls, language_code: Text):
        if not language_code:
            raise ValueError("Invalid language code: None")
        if isinstance(language_code, LanguageCode):
            return language_code
        for language in cls:
            if language.language_code == language_code:
                return language
            if language.value.casefold() == language_code.casefold():
                return language
        raise ValueError(f"Invalid language code: {language_code}")
