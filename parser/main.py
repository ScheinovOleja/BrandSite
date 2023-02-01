import asyncio

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from parser.handlers.collectors.dior import ParserDior
from parser.handlers.collectors.zilli import ParserZilli
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

    async def start_all_parsers(self):
        # for link_zilli in self.links_zilli:
        #     task_zilli = ParserZilli(link_zilli, self.Session())
        #     await task_zilli.main()
        for link_dior in self.links_dior:
            task_dior = ParserDior(link_dior, self.Session())
            await task_dior.main()


if __name__ == '__main__':
    parser = Parser()
    asyncio.run(parser.start_all_parsers())
