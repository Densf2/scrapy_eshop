import scrapy


class ItemsSpider(scrapy.Spider):
    name = "items"
    start_url = 'https://prego.ua/uk/muzhskaya-obuv/{}'

    def start_requests(self):

        keywords = ['myzskie-sliponi', 'sandalii']
        for keyword in keywords:
            url = self.start_url.format(keyword)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        blocks = response.css('div.article_frame')
        for block in blocks:
            data = {
                'product_name': block.css('div.product_name::text').get(),
                'product_model': block.css('div.product_name p::text').get(),
                'product_price': block.css('div.price-wrap').css('.new-price span::text').get()
            }
            yield data

        yield from response.follow_all(css='ul.paginator__list a', callback=self.parse)
