from condos.items import CondosItem
from scrapy import Spider, Request
import math

class CondosSpider(Spider):
	name = 'condos_spider'
	allowed_urls = ['https://condos.ca/toronto']
	start_urls = ['https://condos.ca/toronto/condos-for-sale?map_bounds=-79.63897526264293,43.56808747493062,-79.11338328514107,43.86768972866193']

	def parse(self, response):
		items_per_page = len(response.xpath('//div[@class="AdoKE _1l2Kt RwCNM styles___ListingPreview-sc-1c409cv-0 bQdjGe"]'))
		num_items = int(response.xpath('//span[@class="styles___ListingCount-sc-ij90fh-22 kafcpM"]/text()').extract_first())
		num_pages = math.ceil(num_items / items_per_page)

		result_urls = [f'https://condos.ca/toronto/condos-for-sale?map_bounds=-79.63897526264293%2C43.56808747493062%2C-79.11338328514107%2C43.86768972866193&page={i+1}' for i in range(num_pages)]

		for url in result_urls[:2]:
			yield Request(url=url, callback=self.parse_results_page)

	def parse_results_page(self, response):
		condo_urls = response.xpath('//a[@class="styles___Link-sc-54qk44-1 cncVOT"]/@href').extract()
		condo_urls = ['https://condos.ca' + url for url in condo_urls]

		#print('='*55)
		#print(len(condo_urls))
		#print('='*55)

		for url in condo_urls[:2]:
			yield Request(url=url, callback=self.parse_condo_page)

	def parse_condo_page(self, response):
		item_url = response.url

		try:
			price = response.xpath('//div[@class="styles___Price-sc-ka5njm-23 iRyAnp"]/div/text()').extract_first()
		except: 
			price = "-1"

		try:
			floorplan = response.xpath('//span[@class="styles___BlurCont-sc-qq1hs5-0"]/text()').extract()
			if len(floorplan) <= 4:

				floorplan_bd = str(floorplan[0])
				floorplan_ba = floorplan[1]
				floorplan_pk = floorplan[2]
				tax = floorplan[-1]

			else:
				print('the floorplan is:' +  floorplan)

				floorplan_bd = "-1"
				floorplan_ba = "-1"
				floorplan_pk = "-1"
				tax = "-1"

		except:
			floorplan_bd = "-1"
			floorplan_ba = "-1"
			floorplan_pk = "-1"
			tax = "-1"


		try:
			location = response.xpath('//a[@class="styles___AddressInlineLink-sc-ka5njm-29 kgiSGX"]/text()').extract_first()

		except:
			location = "-1"
		
		try:
			sqm = response.xpath('//div[@class="styles___ValueDiv-sc-1cv9cf1-5 cbTzmD"]/text()').extract()[-1]

		except: 
			sqm = "-1"
		
		try:
			main_fee = response.xpath('//div[@class="styles___ValueDiv-sc-1cv9cf1-5 cbTzmD"]/text()').extract()[1]

		except:
			main_fee = "-1"

		meta = {'price': price,
				'floorplan_bd': floorplan_bd,
				'floorplan_ba': floorplan_ba,
				'floorplan_pk': floorplan_pk,
				'sqm': sqm,
				'tax': tax,
				'location': location,}

		print('='*55)
		print(meta)
		print('='*55)

		yield Request(url=item_url, callback=self.parse_item_page, meta=meta)

	def parse_item_page(self, response):
		
		
		price = response.meta['price']
		floorplan_bd = response.meta['floorplan_bd']
		floorplan_ba = response.meta['floorplan_ba']
		floorplan_pk = response.meta['floorplan_pk']
		sqm = response.meta['sqm']
		tax = response.meta['tax']
		location = response.meta['location']



		item = CondosItem()
		item['price'] = price
		item['floorplan_bd'] = floorplan_bd
		item['floorplan_ba'] = floorplan_ba
		item['floorplan_pk'] = floorplan_pk
		item['sqm'] = sqm
		item['tax'] = tax
		item['location'] = location

		yield item






		
