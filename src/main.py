import requests
import csv
import json
import sys

from bs4 import BeautifulSoup

class Crawler():

	def __init__(self, url):
		
		self.url = url

		page = requests.get(self.url)
		self.soup = BeautifulSoup(page.text, "lxml")


	def get_items_list(self):
		search_list = self.soup.find(class_="srp-results")
		raw_items = search_list.find_all("li", class_="s-item__pl-on-bottom")
		return raw_items

	def get_data(self, raw_items):
		
		item_list = []
		for item in raw_items:

			raw_name = item.find(class_="s-item__title").text
			if "New Listing" in raw_name:
				slicer = slice(11, 45)
				name = raw_name[slicer]
			else:
				name = raw_name

			condition = item.find(class_="s-item__subtitle").text
			cost = item.find(class_="s-item__price").text
			try:
				rating = item.find(class_="s-item__reviews").find(class_="clipped").text
			except AttributeError:
				rating = None

			href = item.find(class_="s-item__link").get('href')

			item_list.append([name, condition, rating, cost, href])
		return item_list


	def next_page(self):

		pass
		# new_url = self.soup.find(class_="pagination__next icon-link").get("href")
		# next_page = requests.get(new_url)
		# self.soup = (next_page.text, "lxml")
		# items = self.get_items_list()
		# item_list = self.get_data(items)

	def loop(self):
		pass
		# self.next_page()


	def make_xml(self, item_list):

		for item in item_list:
			print(item[0])


if __name__ == "__main__":
	sys.stdout.reconfigure(encoding='utf-8')
	main = Crawler("https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=graphics+card&_sacat=0&_fsrp=1&rt=nc&_odkw=graphics+card&_osacat=0&_dcat=27386&_oaa=1")
	items = main.get_items_list()
	item_list = main.get_data(items)
	# main.next_page()
	# main.loop()
	# main.make_xml(item_list)