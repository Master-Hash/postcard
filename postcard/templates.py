from fastapi.templating import Jinja2Templates
from .translations import translations

templates = Jinja2Templates(directory="templates")
templates.env.add_extension("jinja2.ext.i18n")
templates.env.trim_blocks = True
templates.env.lstrip_blocks = True
templates.env.newstyle_gettext = True
templates.env.install_gettext_translations(translations)
