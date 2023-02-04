import asyncio

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from parser.handlers.collectors.bottega import ParserBottega
from parser.models import Base


class Parser:

    def __init__(self):
        self.engine = create_engine('postgresql+psycopg2://oleg:oleg2000@localhost/parser_brands')
        self.Session = sessionmaker(self.engine)
        with self.Session():
            Base.metadata.create_all(self.engine)

        self.links_zilli = ["https://www.zilli.com/en/3-ready-to-wear", "https://www.zilli.com/en/12-shoes",
                            "https://www.zilli.com/en/10-accessories"]
        self.links_dior = [
            (
                "https://kpgnq6fji9-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20"
                "(4.13.1)%3B%20Browser",
                'bags'),
            (
                "https://kpgnq6fji9-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20"
                "(4.13.1)%3B%20Browser",
                'belts')
        ]
        self.links_loropiana = [
            ("https://ua.loropiana.com/ru/c/L1_MEN/results?page={}", "male_ready-to-wear"),
            ("https://ua.loropiana.com/ru/c/L2_MEN_ACCESSORIES/results?page={}", "male_accessories"),
            ("https://ua.loropiana.com/ru/c/L2_SHOES_MAN/results?page={}", "male_shoes"),
            ("https://ua.loropiana.com/ru/c/L1_WOM/results?page={}", "female_ready-to-wear"),
            ("https://ua.loropiana.com/ru/c/L2_WOM_ACCESSORIES/results?page={}", "female_accessories"),
            ("https://ua.loropiana.com/ru/c/L2_SHOES_WOM/results?page={}", "female_shoes"),
            ("https://ua.loropiana.com/ru/c/L2_WOM_LG/results?page={}", "female_leather-goods")
        ]
        self.links_louis = [
            ("https://api.louisvuitton.com/eco-eu/search-merch-eapi/v1/rus-ru/plp/products/tfr7qdp?page={}",
             'female_bags'),
            ("https://api.louisvuitton.com/eco-eu/search-merch-eapi/v1/rus-ru/plp/products/t164iz3b?page={}",
             'female_accessories'),
            ("https://api.louisvuitton.com/eco-eu/search-merch-eapi/v1/rus-ru/plp/products/ty346sh?page={}",
             'female_belts'),
            ("https://api.louisvuitton.com/eco-eu/search-merch-eapi/v1/rus-ru/plp/products/t1uezqf4?page={}",
             'male_bags'),
            ("https://api.louisvuitton.com/eco-eu/search-merch-eapi/v1/rus-ru/plp/products/t1g9dx5w?page={}",
             'male_belts'),
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
                "",
                ""
            ),
            (),
            (),
            (),
            (),
        ]
        self.links_bottega = [
            ("https://www.bottegaveneta.com/on/demandware.store/Sites-BV-R-INTL-Site/en_ZW/Search-UpdateGrid?"
             "cgid=women-bags&prefn1=akeneo_employeesSalesVisible&prefv1=false&prefn2=akeneo_markDownInto&"
             "prefv2=no_season&prefn3=countryInclusion&prefv3=ZW&start=0&sz=1000", 'Женские сумки'),
            ("https://www.bottegaveneta.com/on/demandware.store/Sites-BV-R-INTL-Site/en_ZW/Search-UpdateGrid?"
             "cgid=women-belts&prefn1=akeneo_employeesSalesVisible&prefv1=false&prefn2=akeneo_markDownInto&"
             "prefv2=no_season&prefn3=countryInclusion&prefv3=ZW&start=0&sz=1000", 'Женские ремни'),
        ]

    async def start_all_parsers(self):
        # for link_zilli in self.links_zilli:
        #     task_zilli = ParserZilli(link_zilli, self.Session())
        #     await task_zilli.main()
        # for link_dior in self.links_dior:
        #     task_dior = ParserDior(link_dior, self.Session())
        #     await task_dior.main()
        # for link_loropiana in self.links_loropiana:
        #     task_loropiana = ParserLoropiana(link_loropiana, self.Session())
        #     await task_loropiana.main()
        # for link_louis in self.links_louis:
        #     task_louis = ParserLouis(link_louis, self.Session())
        #     await task_louis.main()
        # for link_chanel in self.links_chanel:
        #     task_dior = ParserChanel(link_chanel, self.Session())
        #     await task_dior.main()
        # for link_brunello in self.links_brunello:
        #     task_brunello = ParserBrunello(link_brunello, self.Session())
        #     await task_brunello.main()
        # for link_brioni in self.links_brioni:
        #     task_brioni = ParserBrioni(link_brioni, self.Session())
        #     await task_brioni.main()
        # for link_stefano in self.links_brioni:
        #     task_stefano = ParserStefano(link_stefano, self.Session())
        #     await task_stefano.main()
        for link_bottega in self.links_bottega:
            task_stefano = ParserBottega(link_bottega, self.Session())
            await task_stefano.main()


if __name__ == '__main__':
    parser = Parser()
    asyncio.run(parser.start_all_parsers())
