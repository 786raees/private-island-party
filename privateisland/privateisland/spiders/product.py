import scrapy


class ProductSpider(scrapy.Spider):
    name = 'product'
    start_urls = ['https://privateislandparty.com/']

    def parse(self, response):
        cat_links = response.xpath('//*[@id="emthemesModez-verticalCategories-sidebar"]/ul/li/a/@href').getall()
        for cat_link in cat_links:
            yield scrapy.Request(cat_link, self.parse_products_page)
    
    def parse_products_page(self, response):
        products = response.xpath('//*[@id="product-listing-container"]/form/ul/li/article/div[1]/h4/a/@href').getall()
        for product in products:
            yield scrapy.Request(product, self.parse_product_details)
        next_page = response.xpath('//li[@class="pagination-item pagination-item--next"]/a/@href').get()
        if next_page:
            yield scrapy.Request(next_page, self.parse_products_page)

    def parse_product_details(self, response):
        Title = response.xpath('//h1[@class="productView-title"]/text()').get()
        UPC = response.xpath('//dd[@class="productView-info-value productView-info-value--upc"]/text()').get()
        Price = response.xpath('//*[@id="topOfPage"]/div[6]/div[1]/div/main/div[1]/div[1]/div[1]/div[1]/section[3]/div[1]/div[1]/div[2]/span[3]/text()').get()
        SKU = response.xpath('//dd[@class="productView-info-value productView-info-value--sku"]/text()').get()
        yield {
            'Title':Title,
            'UPC':UPC,
            'Price':Price,
            'SKU':SKU,
        }
        # TODOS
        """test all the things are ok for every products and scrape image link"""
        # Image_URL = response.xpath('//h1[@class="productView-title"]/text()').get()