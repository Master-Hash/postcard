from babel import Locale
from babel.support import Translations
from functools import lru_cache
from typing import Union

from fastapi.templating import Jinja2Templates

# starlette 菜，任他报错
templates = Jinja2Templates(directory=["templates", "API/res/icon"])
templates.env.add_extension("jinja2.ext.i18n")
templates.env.trim_blocks = True
templates.env.lstrip_blocks = True
templates.env.newstyle_gettext = True
templates.env.enable_async = True


@lru_cache(typed=True)
def getTranslation(locale: Union[str, Locale]):
    return Translations.load("locale", locale)

# @lru_cache
# def getTranslations(locale: Locale) -> Translations:
#     return Translations.load("locale", locale)

# templates.env.install_gettext_callables(
#     lambda msg: getTranslation().gettext(msg),
#     lambda s, p, n: getTranslation().ngettext(s, p, n),
#     newstyle=True,
# )

# https://jinja.palletsprojects.com/en/2.11.x/extensions/
# After enabling, an application has to provide gettext
# and ngettext functions, either globally or when rendering.
# A _() function is added as an alias to the gettext function.

# templates.env.install_gettext_translations(translations)

# 总之，它说的是不是直接把两个函数传入模板？（
