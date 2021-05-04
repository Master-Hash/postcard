import logging
import geoip2.database

from .translations import translations

_ = translations.gettext


# https://siongui.github.io/2012/10/11/python-parse-accept-language-in-http-request-header/
# def parseAcceptLanguage(acceptLanguage: str) -> list[tuple[str, str]]:
#     languages = acceptLanguage.split(",")
#     locale_q_pairs = []

#     for language in languages:
#         if language.split(";")[0] == language:
#             # no q => q = 1
#             locale_q_pairs.append((language.strip(), "1"))
#         else:
#             _tmp = language.split(";")
#             locale = _tmp[0].strip()
#             q = _tmp[1].split("=")[1]
#             locale_q_pairs.append((locale, q))

#     return locale_q_pairs


# 这里有一个奇怪的问题
# 理论上可以直接查到 locale
# 但是有时候地名查不到对应语言，所以必须处理下多语言情况？
# 先允许我在这里搞纯英文

# 有一个暂时的方案：把 accept-language 列表左右加长，
# 左边是 Query，右边是默认 en
def getCity(ip: str, *, locale: str) -> str:
    if ip in (
        "127.0.0.1",
        "::1",
    ):
        # There's no place like 127.0.0.1, that's a famous saying.
        return _("localhost")
    with geoip2.database.Reader("GeoLite2-City.mmdb") as reader:
        response = reader.city(ip)
    if response.city.names:
        if locale in response.city.names:
            return response.city.names[locale]
        else:
            return response.city.name
    elif response.country.names:
        if locale in response.country.names:
            return response.country.names[locale]
        else:
            return response.country.name
    elif response.continent.names:
        if locale in response.country.names:
            return response.continent.names[locale]
        else:
            return response.continent.name
    else:
        logging.warn(f"找不到 ip 位置：{ip}")
        return _("nowhere")
