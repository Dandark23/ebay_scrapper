import requests
import csv
import json
import sys
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


class Crawler():

	def __init__(self, url):
		
		self.url = url
		self.driver = webdriver.Firefox()
		self.driver.get(url)


	def make_soup(self):

		html = self.driver.page_source
		self.soup = BeautifulSoup(html, "lxml")



	def get_items_list(self):
		# get a list of interest from url
		
		search_list = self.soup.find(class_="srp-results")
		raw_items = search_list.find_all("li", class_="s-item__pl-on-bottom")
		return raw_items

	def get_data(self, raw_items):
		# crawl raw data for xml 
		
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
		# go to next page
		btn = self.driver.find_element(By.CLASS_NAME, "pagination__next")
		self.driver.execute_script("arguments[0].click();", btn)


	def __get_items_from_list__(self, list_items):

		ready_list_item = []
		for items in list_items:
			for item in items:
				name = item[0]
				condition = item[1]
				rating = item[2]
				cost = item[3]
				href = item[4]
				ready_list_item.append([name, condition, rating, cost, href])

		return ready_list_item


	def loop(self):
		list_items = [] 
		for i in range(0, 2):
			self.make_soup()
			raw_items = self.get_items_list()
			items = self.get_data(raw_items)
			time.sleep(4)
			self.next_page()
			list_items.append(items)
			i += 1

		ready_item = self.__get_items_from_list__(list_items)

		return ready_item


	def make_xml(self, item_list):

		pass

	def exit_driver(self):

		self.driver.close()


if __name__ == "__main__":
	sys.stdout.reconfigure(encoding='utf-8')
	crawler = Crawler("https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=graphics+card&_sacat=0&_fsrp=1&rt=nc&_odkw=graphics+card&_osacat=0&_dcat=27386&_oaa=1")
	# crawler.make_soup()
	# items = crawler.get_items_list()
	# item_list = crawler.get_data(items)
	items = crawler.loop()
	print(items)
	# crawler.exit_driver()
	# main.loop()
	# main.make_xml(item_list)