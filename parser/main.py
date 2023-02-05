import asyncio
import threading

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from handlers.collectors.bottega import ParserBottega
from handlers.collectors.brioni import ParserBrioni
from handlers.collectors.brunello import ParserBrunello
from handlers.collectors.celine import ParserCeline
from handlers.collectors.chanel import ParserChanel
from handlers.collectors.dior import ParserDior
from handlers.collectors.ford import ParserFord
from handlers.collectors.laurent import ParserLaurent
from handlers.collectors.loropiana import ParserLoropiana
from handlers.collectors.louis import ParserLouis
from handlers.collectors.stefano import ParserStefano
from handlers.collectors.zilli import ParserZilli
from models import Base


class Parser:

    def __init__(self):
        self.engine = create_engine('postgresql+psycopg2://oleg:oleg2000@localhost/parser_brands')
        self.Session = sessionmaker(self.engine)
        with self.Session():
            Base.metadata.create_all(self.engine)
        self.links_zilli = [
            ("https://www.zilli.com/en/3-ready-to-wear", "Верхняя одежда"),
            ("https://www.zilli.com/en/12-shoes", "Обувь"),
            ("https://www.zilli.com/en/10-accessories", "Аксессуары")
        ]
        self.links_dior = [
            (
                "https://kpgnq6fji9-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20"
                "(4.13.1)%3B%20Browser",
                'Сумки'),
            (
                "https://kpgnq6fji9-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20"
                "(4.13.1)%3B%20Browser",
                'Ремни')
        ]
        self.links_loropiana = [
            ("https://ua.loropiana.com/ru/c/L1_MEN/results?page={}", "Мужская верхняя одежда"),
            ("https://ua.loropiana.com/ru/c/L2_MEN_ACCESSORIES/results?page={}", "Мужские аксессуары"),
            ("https://ua.loropiana.com/ru/c/L2_SHOES_MAN/results?page={}", "Мужская обувь"),
            ("https://ua.loropiana.com/ru/c/L1_WOM/results?page={}", "Женская верхняя одежда"),
            ("https://ua.loropiana.com/ru/c/L2_WOM_ACCESSORIES/results?page={}", "Женские аксессуары"),
            ("https://ua.loropiana.com/ru/c/L2_SHOES_WOM/results?page={}", "Женская обувь"),
            ("https://ua.loropiana.com/ru/c/L2_WOM_LG/results?page={}", "Женские изделия из кожи")
        ]
        self.links_louis = [
            ("https://api.louisvuitton.com/eco-eu/search-merch-eapi/v1/rus-ru/plp/products/tfr7qdp?page={}",
             'Женские сумки'),
            ("https://api.louisvuitton.com/eco-eu/search-merch-eapi/v1/rus-ru/plp/products/t164iz3b?page={}",
             'Женские аксессуары'),
            ("https://api.louisvuitton.com/eco-eu/search-merch-eapi/v1/rus-ru/plp/products/ty346sh?page={}",
             'Женские ремни'),
            ("https://api.louisvuitton.com/eco-eu/search-merch-eapi/v1/rus-ru/plp/products/t1uezqf4?page={}",
             'Мужские сумки'),
            ("https://api.louisvuitton.com/eco-eu/search-merch-eapi/v1/rus-ru/plp/products/t1g9dx5w?page={}",
             'Мужские ремни'),
        ]
        self.links_chanel = [
            (
                "https://www.chanel.com/asset/frontstage/api/m/v1/products/?fh_location=//catalog01/ru_RU/categories<{catalog01_one}/categories<{catalog01_one_fashion}/categories<{catalog01_one_fashion_1x1}/categories<{catalog01_one_fashion_1x1_1x1x1}/categories<{catalog01_one_fashion_1x1_1x1x1_1x1x1x1}/tridiv_producttype>{fshitem}/tridiv_variant_market>{russia}/tridiv_variant_status>{active}/tridiv_variant_activationdate_russia_web<20230131/tridiv_variant_cancellationdate_russia_web>20230131/tridiv_variant_nocomunication_russia>{false}/tridiv_variant_targetdiffusion_russia>{web}/tridiv_variant_catalog_segment>{ncs;none}/tridiv_producttype>{fshitem}/tridiv_gridselection>{true}&fh_context_location=//catalog01/ru_RU/categories<{catalog01_one}/categories<{catalog01_one_fashion}/categories<{catalog01_one_fashion_1x1}/categories<{catalog01_one_fashion_1x1_1x1x1}/categories<{catalog01_one_fashion_1x1_1x1x1_1x1x1x1}/tridiv_producttype>{fshitem}&fh_start_index=0&fh_view_size=200&fh_session=HV4_PRD&platform=HV4&page=0&pcmNewComLocale=ru_RU&pcmAlternateLocale=ru_RU",
                "Сумка-конверт"
            ),
            (
                "https://www.chanel.com/asset/frontstage/api/m/v1/products/?fh_view_size=200&fh_session=HV4_PRD&fh_refpath=d1c9c38f-1226-456c-9cc4-b348e59985a4&page=0&platform=HV4&fh_context_location=//catalog01/ru_RU/categories<{catalog01_one}/categories<{catalog01_one_fashion}/categories<{catalog01_one_fashion_1x1}/categories<{catalog01_one_fashion_1x1_1x1x1}/categories<{catalog01_one_fashion_1x1_1x1x1_1x1x1x4}/tridiv_producttype>{fshitem}&fh_refview=lister&fh_reffacet=tridiv_line_united_states&fh_location=//catalog01/ru_RU/categories<{catalog01_one}/categories<{catalog01_one_fashion}/categories<{catalog01_one_fashion_1x1}/categories<{catalog01_one_fashion_1x1_1x1x1}/categories<{catalog01_one_fashion_1x1_1x1x1_1x1x1x4}/tridiv_producttype>{fshitem}/tridiv_variant_market>{russia}/tridiv_variant_status>{active}/tridiv_variant_activationdate_russia_web<20230131/tridiv_variant_cancellationdate_russia_web>20230131/tridiv_variant_nocomunication_russia>{false}/tridiv_variant_targetdiffusion_russia>{web}/tridiv_variant_catalog_segment>{none;ncs}/tridiv_gridselection>{true}&fh_start_index=0&pcmAlternateLocale=ru_RU&pcmNewComLocale=ru_RU",
                "Сумка HOBO"
            ),
            (
                "https://www.chanel.com/asset/frontstage/api/m/v1/products/?fh_view_size=200&fh_session=HV4_PRD&fh_refpath=d1c9c38f-1226-456c-9cc4-b348e59985a4&page=0&platform=HV4&fh_context_location=//catalog01/ru_RU/categories<{catalog01_one}/categories<{catalog01_one_fashion}/categories<{catalog01_one_fashion_1x1}/categories<{catalog01_one_fashion_1x1_1x1x1}/categories<{catalog01_one_fashion_1x1_1x1x1_1x1x1x3}/tridiv_producttype>{fshitem}&fh_refview=lister&fh_reffacet=tridiv_line_united_states&fh_location=//catalog01/ru_RU/categories<{catalog01_one}/categories<{catalog01_one_fashion}/categories<{catalog01_one_fashion_1x1}/categories<{catalog01_one_fashion_1x1_1x1x1}/categories<{catalog01_one_fashion_1x1_1x1x1_1x1x1x3}/tridiv_producttype>{fshitem}/tridiv_variant_market>{russia}/tridiv_variant_status>{active}/tridiv_variant_activationdate_russia_web<20230131/tridiv_variant_cancellationdate_russia_web>20230131/tridiv_variant_nocomunication_russia>{false}/tridiv_variant_targetdiffusion_russia>{web}/tridiv_variant_catalog_segment>{none;ncs}/tridiv_gridselection>{true}&fh_start_index=0&pcmAlternateLocale=ru_RU&pcmNewComLocale=ru_RU",
                "Сумка-шоппер"
            ),
            (
                "https://www.chanel.com/asset/frontstage/api/m/v1/products/?fh_view_size=200&fh_session=HV4_PRD&fh_refpath=e6d9bdfb-3d42-4c1f-8b15-46c67d2f38ab&page=0&platform=HV4&fh_context_location=//catalog01/ru_RU/categories<{catalog01_one}/categories<{catalog01_one_fashion}/categories<{catalog01_one_fashion_1x1}/categories<{catalog01_one_fashion_1x1_1x1x1}/tridiv_line_united_states>{1x3x22}/tridiv_producttype>{fshitem}&fh_refview=lister&fh_reffacet=tridiv_subcategory_united_states&fh_location=//catalog01/ru_RU/categories<{catalog01_one}/categories<{catalog01_one_fashion}/categories<{catalog01_one_fashion_1x1}/categories<{catalog01_one_fashion_1x1_1x1x1}/tridiv_line_united_states>{1x3x22}/tridiv_producttype>{fshitem}/tridiv_variant_market>{russia}/tridiv_variant_status>{active}/tridiv_variant_activationdate_russia_web<20230131/tridiv_variant_cancellationdate_russia_web>20230131/tridiv_variant_nocomunication_russia>{false}/tridiv_variant_targetdiffusion_russia>{web}/tridiv_variant_catalog_segment>{none;ncs}/tridiv_gridselection>{true}&fh_start_index=0&pcmAlternateLocale=ru_RU&pcmNewComLocale=ru_RU",
                "Макси-сумка"
            ),
            (
                "https://www.chanel.com/asset/frontstage/api/m/v1/products/?fh_view_size=200&fh_session=HV4_PRD&fh_refpath=ecc4acb6-941b-4424-a11c-3c9627a37a78&platform=HV4&fh_context_location=//catalog01/ru_RU/categories<{catalog01_one}/categories<{catalog01_one_fashion}/categories<{catalog01_one_fashion_1x1}/categories<{catalog01_one_fashion_1x1_1x1x1}/categories<{catalog01_one_fashion_1x1_1x1x1_1x1x1x2}/tridiv_producttype>{fshitem}&fh_refview=lister&fh_reffacet=fsh_fabricfacet&fh_location=//catalog01/ru_RU/categories<{catalog01_one}/categories<{catalog01_one_fashion}/categories<{catalog01_one_fashion_1x1}/categories<{catalog01_one_fashion_1x1_1x1x1}/categories<{catalog01_one_fashion_1x1_1x1x1_1x1x1x2}/tridiv_producttype>{fshitem}/tridiv_variant_market>{russia}/tridiv_variant_status>{active}/tridiv_variant_activationdate_russia_web<20230131/tridiv_variant_cancellationdate_russia_web>20230131/tridiv_variant_nocomunication_russia>{false}/tridiv_variant_targetdiffusion_russia>{web}/tridiv_variant_catalog_segment>{none;ncs}/tridiv_gridselection>{true}/fsh_fabricfacet>{ff00003}&page=0&fh_start_index=0&pcmAlternateLocale=ru_RU&pcmNewComLocale=ru_RU",
                "Рюкзак"
            ),
            (
                "https://www.chanel.com/asset/frontstage/api/m/v1/products/?fh_view_size=200&fh_session=HV4_PRD&fh_refpath=d1c9c38f-1226-456c-9cc4-b348e59985a4&page=0&platform=HV4&fh_context_location=//catalog01/ru_RU/categories<{catalog01_one}/categories<{catalog01_one_fashion}/categories<{catalog01_one_fashion_1x1}/categories<{catalog01_one_fashion_1x1_1x1x1}/categories<{catalog01_one_fashion_1x1_1x1x1_1x1x1x5}/tridiv_producttype>{fshitem}&fh_refview=lister&fh_reffacet=tridiv_line_united_states&fh_location=//catalog01/ru_RU/categories<{catalog01_one}/categories<{catalog01_one_fashion}/categories<{catalog01_one_fashion_1x1}/categories<{catalog01_one_fashion_1x1_1x1x1}/categories<{catalog01_one_fashion_1x1_1x1x1_1x1x1x5}/tridiv_producttype>{fshitem}/tridiv_variant_market>{russia}/tridiv_variant_status>{active}/tridiv_variant_activationdate_russia_web<20230131/tridiv_variant_cancellationdate_russia_web>20230131/tridiv_variant_nocomunication_russia>{false}/tridiv_variant_targetdiffusion_russia>{web}/tridiv_variant_catalog_segment>{none;ncs}/tridiv_gridselection>{true}&fh_start_index=0&pcmAlternateLocale=ru_RU&pcmNewComLocale=ru_RU",
                "Сумка vanity"
            ),
            (
                "https://www.chanel.com/asset/frontstage/api/m/v1/products/?fh_view_size=200&fh_session=HV4_PRD&fh_refpath=ecc4acb6-941b-4424-a11c-3c9627a37a78&page=0&platform=HV4&fh_context_location=//catalog01/ru_RU/categories<{catalog01_one}/categories<{catalog01_one_fashion}/categories<{catalog01_one_fashion_1x1}/categories<{catalog01_one_fashion_1x1_1x1x1}/categories<{catalog01_one_fashion_1x1_1x1x1_1x1x1x7,1x1x1x19}/tridiv_producttype>{fshitem}&fh_refview=lister&fh_reffacet=fsh_fabricfacet&fh_location=//catalog01/ru_RU/categories<{catalog01_one}/categories<{catalog01_one_fashion}/categories<{catalog01_one_fashion_1x1}/categories<{catalog01_one_fashion_1x1_1x1x1}/categories<{catalog01_one_fashion_1x1_1x1x1_1x1x1x7,catalog01_one_fashion_1x1_1x1x1_1x1x1x19}/tridiv_producttype>{fshitem}/tridiv_variant_market>{russia}/tridiv_variant_status>{active}/tridiv_variant_activationdate_russia_web<20230131/tridiv_variant_cancellationdate_russia_web>20230131/tridiv_variant_nocomunication_russia>{false}/tridiv_variant_targetdiffusion_russia>{web}/tridiv_variant_catalog_segment>{none;ncs}/tridiv_gridselection>{true}&fh_start_index=0&pcmAlternateLocale=ru_RU&pcmNewComLocale=ru_RU",
                "Вечерняя сумка"
            ),
            (
                "https://www.chanel.com/asset/frontstage/api/m/v1/products/?fh_view_size=20&fh_session=HV4_PRD&fh_refpath=e6d9bdfb-3d42-4c1f-8b15-46c67d2f38ab&page=0&platform=HV4&fh_context_location=//catalog01/ru_RU/categories<{catalog01_one}/categories<{catalog01_one_fashion}/categories<{catalog01_one_fashion_1x1}/categories<{catalog01_one_fashion_1x1_1x1x1}/tridiv_categoryname_united_states>{1x1x1x11;1x1x1x12;1x1x1x16;1x1x1x2;1x1x1x23;1x1x1x24;1x1x1x25;1x1x1x26;1x1x1x6;1x1x1x8,1x1x1x21}/tridiv_producttype>{fshitem}&fh_refview=lister&fh_reffacet=tridiv_subcategory_united_states&fh_location=//catalog01/ru_RU/categories<{catalog01_one}/categories<{catalog01_one_fashion}/categories<{catalog01_one_fashion_1x1}/categories<{catalog01_one_fashion_1x1_1x1x1}/tridiv_categoryname_united_states>{1x1x1x6;1x1x1x2;1x1x1x16;1x1x1x8;1x1x1x26;1x1x1x11;1x1x1x12;1x1x1x21;1x1x1x25;1x1x1x23}/tridiv_producttype>{fshitem}/tridiv_variant_market>{russia}/tridiv_variant_status>{active}/tridiv_variant_activationdate_russia_web<20230131/tridiv_variant_cancellationdate_russia_web>20230131/tridiv_variant_nocomunication_russia>{false}/tridiv_variant_targetdiffusion_russia>{web}/tridiv_variant_catalog_segment>{none;ncs}/tridiv_gridselection>{true}&fh_start_index=0&pcmAlternateLocale=ru_RU&pcmNewComLocale=ru_RU",
                "Другая сумка"
            ),
        ]
        self.links_brunello = [
            (
                "https://shop.brunellocucinelli.com/ru-ru/%D0%B6%D0%B5%D0%BD%D1%89%D0%B8%D0%BD%D1%8B/%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/%D0%B2%D0%B5%D1%80%D1%85%D0%BD%D1%8F%D1%8F-%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/?start=0&sz=100&template=search/grid3Template",
                "Женская верхняя одежда"),
            (
                "https://shop.brunellocucinelli.com/ru-ru/%D0%B6%D0%B5%D0%BD%D1%89%D0%B8%D0%BD%D1%8B/%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/%D0%BF%D0%B8%D0%B4%D0%B6%D0%B0%D0%BA%D0%B8/?template=search/grid3Template&start=0&sz=100",
                "Женские пиджаки"
            ),
            (
                "https://shop.brunellocucinelli.com/ru-ru/%D0%BC%D1%83%D0%B6%D1%87%D0%B8%D0%BD%D1%8B/%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/%D0%B2%D0%B5%D1%80%D1%85%D0%BD%D1%8F%D1%8F-%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/?template=search/grid3Template&start=0&sz=200",
                "Мужская верхняя одежда"
            ),
            (
                "https://shop.brunellocucinelli.com/ru-ru/%D0%BC%D1%83%D0%B6%D1%87%D0%B8%D0%BD%D1%8B/%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/%D0%BF%D0%B8%D0%B4%D0%B6%D0%B0%D0%BA%D0%B8/?template=search/grid3Template&start=0&sz=200",
                "Мужские пиджаки"
            ),
        ]
        self.links_brioni = [
            (
                "https://wnp6tqnc8r-3.algolianet.com/1/indexes/prod_primary_index_products_milan-noeu_ru/query",
                "Мужская верхняя одежда"
            ),
        ]
        self.links_stefano = [
            (
                "4AL",
                "Мужская верхняя одежда"
            ),
            (
                "LGN",
                "Мужские спортивные костюмы"
            ),
            (
                "5ID",
                "Мужские ремни"
            ),
            (
                "UI7",
                "Мужские сумки"
            ),
            (
                "6X0",
                "Мужские изделия из кожи"
            ),
            (
                "SR03",
                "Мужская обувь"
            ),
        ]
        self.links_bottega = [
            ("https://www.bottegaveneta.com/on/demandware.store/Sites-BV-R-INTL-Site/en_ZW/Search-UpdateGrid?"
             "cgid=women-bags&prefn1=akeneo_employeesSalesVisible&prefv1=false&prefn2=akeneo_markDownInto&"
             "prefv2=no_season&prefn3=countryInclusion&prefv3=ZW&start=0&sz=1000", 'Женские сумки'),
            ("https://www.bottegaveneta.com/on/demandware.store/Sites-BV-R-INTL-Site/en_ZW/Search-UpdateGrid?"
             "cgid=women-belts&prefn1=akeneo_employeesSalesVisible&prefv1=false&prefn2=akeneo_markDownInto&"
             "prefv2=no_season&prefn3=countryInclusion&prefv3=ZW&start=0&sz=1000", 'Женские ремни'),
        ]
        self.links_celine = [
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?cgid=A0302&start=0&"
                "sz=1000&selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0302&start=0&sz=1000",
                "Женские сумки 16"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?cgid=A0303&start=0&"
                "sz=1000&selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0303&start=0&sz=1000",
                "Женские сумки 'Триумф'"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?cgid=A0320&start=0&"
                "sz=1000&selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0320&start=0&sz=1000",
                "Женские сумки 'Кожа Триумф'"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0311&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0311&start=0&sz=1000",
                "Женские сумки 'Холс Триумф'"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0317&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0317&start=0&sz=1000",
                "Женские сумки 'АВА'"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0314&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0314&start=0&sz=1000",
                "Женские сумки 'Корзина'"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0305&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0305&start=0&sz=1000",
                "Женские сумки 'Классическая'"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0304&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0304&start=0&sz=1000",
                "Женские поясные сумки"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0306&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0306&start=0&sz=1000",
                "Женские сумки 'Рюкзак'"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0308&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0308&start=0&sz=1000",
                "Женские сумки 'Больше линий'"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0321&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0321&start=0&sz=1000",
                "Женские мини-сумки"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A00101&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A00101&start=0&sz=1000",
                "Женские Ремни"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A00103&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A00103&start=0&sz=1000",
                "Женские шапки и шарфы"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A00107&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A00107&start=0&sz=1000",
                "Женское пляжное"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0022&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0022&start=0&sz=1000",
                "Женские ботинки"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0023&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0023&start=0&sz=1000",
                "Женские лоферы и балетки"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0021&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0021&start=0&sz=1000",
                "Женские Сандали"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0020&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0020&start=0&sz=1000",
                "Женские пампы"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0024&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0024&start=0&sz=1000",
                "Женские кроссовки"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0046&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0046&start=0&sz=1000",
                "Женские мелкие кожанные изделия 'Холс Триумф'"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0040&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0040&start=0&sz=1000",
                "Женские кошельки"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0041&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0041&start=0&sz=1000",
                "Женские визитницы"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A00106&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A00106&start=0&sz=1000",
                "Женские кожаные изделия"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0044&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0044&start=0&sz=1000",
                "Женские маленькие аксессуары"
            ),
            (
                "https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0044&start=0&sz=1000&"
                "selectedUrl=https://www.celine.com/on/demandware.store/Sites-CELINE_WW-Site/en/Search-UpdateGrid?"
                "cgid=A0044&start=0&sz=1000",
                "Женские маленькие аксессуары"
            ),
        ]
        self.links_laurent = [
            (
                "https://www.ysl.com/on/demandware.store/Sites-SLP-INTL-Site/en_ZW/Search-UpdateGrid?"
                "cgid=view-all-handbags-women&prefn1=akeneo_employeesSalesVisible&prefv1=false&prefn2=akeneo_markDownInto"
                "&prefv2=no_season&prefn3=countryInclusion&prefv3=ZW&start=0&sz=1000",
                "Женские сумки"
            ),
            (
                "https://www.ysl.com/on/demandware.store/Sites-SLP-INTL-Site/en_ZW/Search-UpdateGrid?"
                "cgid=view-all-mini-bags-women&prefn1=akeneo_employeesSalesVisible&prefv1=false&prefn2=akeneo_markDownInto"
                "&prefv2=no_season&prefn3=countryInclusion&prefv3=ZW&start=0&sz=1000",
                "Женские мини-сумки"
            ),
            (
                "https://www.ysl.com/on/demandware.store/Sites-SLP-INTL-Site/en_ZW/Search-UpdateGrid?"
                "cgid=view-all-slg-women&prefn1=akeneo_employeesSalesVisible&prefv1=false&prefn2=akeneo_markDownInto"
                "&prefv2=no_season&prefn3=countryInclusion&prefv3=ZW&start=0&sz=1000",
                "Женские маленькие кожаные изделия"
            ),
            (
                "https://www.ysl.com/on/demandware.store/Sites-SLP-INTL-Site/en_ZW/Search-UpdateGrid?"
                "cgid=belts-and-belt-bags-women&prefn1=akeneo_employeesSalesVisible&prefv1=false&prefn2=akeneo_markDownInto"
                "&prefv2=no_season&prefn3=countryInclusion&prefv3=ZW&start=0&sz=1000",
                "Женские ремни и поясные сумки"
            ),
            (
                "https://www.ysl.com/on/demandware.store/Sites-SLP-INTL-Site/en_ZW/Search-UpdateGrid?"
                "cgid=view-all-shoes-women&prefn1=akeneo_employeesSalesVisible&prefv1=false&prefn2=akeneo_markDownInto"
                "&prefv2=no_season&prefn3=countryInclusion&prefv3=ZW&start=0&sz=1000",
                "Женская обувь"
            ),

        ]
        self.links_ford = [
            (
                "https://www.tomford.com/women/handbags/?start={start}&sz={size}", "Женские сумки"
            ),
            (
                "https://www.tomford.com/women/shoes/?start=0&sz=10000&format=page-element", "Женская обувь"
            ),
            (
                "https://www.tomford.com/women/accessories/?start=0&sz=10000&format=page-element", "Женские аксессуары"
            )
        ]

        self.all_tasks = []

    async def start_and_join(self):
        for task in self.all_tasks:
            task.start()
        for task in self.all_tasks:
            task.join()
        self.all_tasks = []

    async def start_all_parsers(self):
        for link_zilli in self.links_zilli:
            task_zilli = ParserZilli(link_zilli, self.Session())
            task = threading.Thread(target=asyncio.run, args=(task_zilli.main(),))
            self.all_tasks.append(task)
        for link_dior in self.links_dior:
            task_dior = ParserDior(link_dior, self.Session())
            task = threading.Thread(target=asyncio.run, args=(task_dior.main(),))
            self.all_tasks.append(task)
        for link_loropiana in self.links_loropiana:
            task_loropiana = ParserLoropiana(link_loropiana, self.Session())
            task = threading.Thread(target=asyncio.run, args=(task_loropiana.main(),))
            self.all_tasks.append(task)
        await self.start_and_join()
        for link_louis in self.links_louis:
            task_louis = ParserLouis(link_louis, self.Session())
            task = threading.Thread(target=asyncio.run, args=(task_louis.main(),))
            self.all_tasks.append(task)
        for link_chanel in self.links_chanel:
            task_chanel = ParserChanel(link_chanel, self.Session())
            task = threading.Thread(target=asyncio.run, args=(task_chanel.main(),))
            self.all_tasks.append(task)
        for link_brunello in self.links_brunello:
            task_brunello = ParserBrunello(link_brunello, self.Session())
            task = threading.Thread(target=asyncio.run, args=(task_brunello.main(),))
            self.all_tasks.append(task)
        await self.start_and_join()
        for link_brioni in self.links_brioni:
            task_brioni = ParserBrioni(link_brioni, self.Session())
            task = threading.Thread(target=asyncio.run, args=(task_brioni.main(),))
            self.all_tasks.append(task)
        for link_stefano in self.links_stefano:
            task_stefano = ParserStefano(link_stefano, self.Session())
            task = threading.Thread(target=asyncio.run, args=(task_stefano.main(),))
            self.all_tasks.append(task)
        for link_bottega in self.links_bottega:
            task_stefano = ParserBottega(link_bottega, self.Session())
            task = threading.Thread(target=asyncio.run, args=(task_stefano.main(),))
            self.all_tasks.append(task)
        await self.start_and_join()
        for link_celine in self.links_celine:
            task_celine = ParserCeline(link_celine, self.Session())
            task = threading.Thread(target=asyncio.run, args=(task_celine.main(),))
            task.start()
            task.join()
        for link_laurent in self.links_laurent:
            task_laurent = ParserLaurent(link_laurent, self.Session())
            task = threading.Thread(target=asyncio.run, args=(task_laurent.main(),))
            self.all_tasks.append(task)
        for link_ford in self.links_ford:
            task_ford = ParserFord(link_ford, self.Session())
            task = threading.Thread(target=asyncio.run, args=(task_ford.main(),))
            self.all_tasks.append(task)
            await self.start_and_join()


if __name__ == '__main__':
    parser = Parser()
    asyncio.run(parser.start_all_parsers())
