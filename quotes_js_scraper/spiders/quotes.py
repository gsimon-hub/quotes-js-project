import scrapy
from ..items import QuoteItem
from scrapy_playwright.page import PageMethod


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # allowed_domains = ["quotes.toscrape.com"]
    # start_urls = ["http://quotes.toscrape.com/"]

    def start_requests(self):
        url = "https://quotes.toscrape.com/js/"
        # yield scrapy.Request(url, meta={"playwright": True})
        yield scrapy.Request(
            url,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[PageMethod("waitForSelector", "div.quote")],
                errback=self.errback,
            ),
        )

    def parse(self, response):
        for quote in response.css("div.quote"):
            quote_item = QuoteItem()
            quote_item["text"] = quote.css("span.text::text").get()
            quote_item["author"] = quote.css("span small.author::text").get()
            quote_item["tags"] = quote.css("div.tags a.tag::text").getall()

            yield quote_item

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        # self.logger.error(repr(failure))
        await page.close()
