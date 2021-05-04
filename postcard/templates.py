from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
templates.env.add_extension("jinja2.ext.i18n")
templates.env.trim_blocks = True
templates.env.lstrip_blocks = True
templates.env.newstyle_gettext = True
templates.env.enable_async = True

# https://jinja.palletsprojects.com/en/2.11.x/extensions/
# After enabling, an application has to provide gettext
# and ngettext functions, either globally or when rendering.
# A _() function is added as an alias to the gettext function.

# templates.env.install_gettext_translations(translations)

# 总之，它说的是不是直接把两个函数传入模板？（
