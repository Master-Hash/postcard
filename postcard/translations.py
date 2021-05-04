from babel import Locale
from babel.support import Translations

translations = Translations.load('locale', [
    Locale.parse(i, sep="-") for i in (
        "zh-CN",
        "zh-TW",
    )
])
