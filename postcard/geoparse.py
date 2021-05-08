from functools import lru_cache
from ipaddress import IPv4Address, IPv6Address
from typing import Callable, Optional, Union

from babel import Locale
from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError
from geoip2.models import City
from werkzeug.datastructures import LanguageAccept


@lru_cache(typed=True)
def getCityModel(ip: Union[
    str,
    IPv4Address,
    IPv6Address,
]) -> Optional[City]:
    try:
        with Reader("GeoLite2-City.mmdb") as reader:
            response = reader.city(ip)
    except AddressNotFoundError:
        response = None
    return response


@lru_cache(typed=True)
def getCity(
    model: City,
    *,
    lang: Locale,
    langs: LanguageAccept,
    _: Callable[[str], str]
) -> str:
    '''
    数据库内的 IP 地理位置查询。
    '''
    for x, xs in (
        (model.city.name,               model.city.names),
        (model.country.name,            model.country.names),
        # (model.registered_country.name, model.registered_country.name),
        # 不可信，例子：
        # geoip2.models.City({'city': {'geoname_id': 5128581, 'names': {'de': 'New York City', 'en': 'New York', 'es': 'Nueva York', 'fr': 'New York', 'ja': 'ニューヨーク', 'pt-BR': 'Nova Iorque', 'ru': 'Нью-Йорк', 'zh-CN': '纽约'}}, 'continent': {'code': 'NA', 'geoname_id': 6255149, 'names': {'de': 'Nordamerika', 'en': 'North America', 'es': 'Norteamérica', 'fr': 'Amérique du Nord', 'ja': '北アメリカ', 'pt-BR': 'América do Norte', 'ru': 'Северная Америка', 'zh-CN': '北美洲'}}, 'country': {'geoname_id': 6252001, 'iso_code': 'US', 'names': {'de': 'USA', 'en': 'United States', 'es': 'Estados Unidos', 'fr': 'États-Unis', 'ja': 'アメリカ合衆国', 'pt-BR': 'Estados Unidos', 'ru': 'США', 'zh-CN': '美国'}}, 'location': {'accuracy_radius': 100, 'latitude': 40.7123, 'longitude': -74.0068, 'metro_code': 501, 'time_zone': 'America/New_York'}, 'postal': {'code': '10118'}, 'registered_country': {'geoname_id': 953987, 'iso_code': 'ZA', 'names': {'de': 'Südafrika', 'en': 'South Africa', 'es': 'Sudáfrica', 'fr': 'Afrique du Sud', 'ja': '南アフリカ', 'pt-BR': 'África do Sul', 'ru': 'ЮАР', 'zh-CN': '南非'}}, 'subdivisions': [{'geoname_id': 5128638, 'iso_code': 'NY', 'names': {'de': 'New York', 'en': 'New York', 'es': 'Nueva York', 'fr': 'New York', 'ja': 'ニューヨーク州', 'pt-BR': 'Nova Iorque', 'ru': 'Нью-Йорк', 'zh-CN': '纽约州'}}], 'traits': {'ip_address': '165.53.216.170', 'prefix_len': 16}}, ['en'])  # noqa
        # 纽约市的 IP 在南非登记（
        (model.continent.name,          model.continent.names),
    ):
        if xs:
            # geoip2.records.City 不是字典，没有 get() 方法（
            return lang.list_patterns.base["locale_id"].lower() \
                .replace("_", "-") in xs and xs[lang] \
                or langs.best_match(xs) and xs[lang] \
                or x
    else:
        # logging.warning("理论上这里不会出现")
        # 还真有，23.136.181.245
        # geoip2.models.City({'registered_country': {'geoname_id':
        # 6252001, 'iso_code': 'US', 'names': {'de': 'USA', 'en':
        # 'United States', 'es': 'Estados Unidos', 'fr':
        # 'États-Unis', 'ja': 'アメリカ合衆国', 'pt-BR': 'Estados
        # Unidos', 'ru': 'США', 'zh-CN': '美国'}}, 'traits':
        # {'ip_address': '23.136.181.245', 'prefix_len': 20}},
        # ['en'])

        return _("nowhere")


@lru_cache(typed=True)
def getSpecialCity(
    ip: Union[IPv4Address, IPv6Address],
    *,
    _: Callable[[str], str],
) -> str:
    '''
    数据库里没有的 IP。
    主要有内网 IP，保留 IP 等。
    '''
    # ipaddress 里面的 is 有点多……
    # 懒得写那麽多特判了，并且名詞也不好找
    # There's no place like 127.0.0.1, that's a famous saying.
    if ip.is_private:
        return _("localhost")
    elif ip.is_reserved:
        return _("some reservation")
    else:
        return _("nowhere")
