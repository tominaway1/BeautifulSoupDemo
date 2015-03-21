# Data System Engineers at YipitData need to be able to extract messy data
# from external websites in a clean and robust manner.

# The assignment is to write a script to scrape the budgets of the Academy
# Award Best Picture winners from Wikipedia. Your script should go the
# the Wikipedia
# page for the award
# http://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture#1920s, follow
# the link for each years winner, grab the budget from the box on the right
# of the page, and print out each Year-Title-Budget combination. After
# printing each combination, it should print the average budget at the end.

# If you encounter any edge cases, feel free to use your best judgement and
# add a comment with your conclusion. This code should be written to
# production standards.

# You can use any language you want, but there is a strong preference for a
# language where we will be able to reproduce your results (any modern,
# semi-popular language will be fine). Please add instructions about any
# additional libraries that may be necessary along with versions.

from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import re, urllib

# Make HTML parsers
class DateParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.is_valid = False
		self.dates = []

	def resets(self):
		self.is_valid = False
		self.dates = []

	def handle_starttag(self, tag, attrs):
		for a in attrs:
			if a[0] == 'title':
				s = re.findall(r"[^#]+(?=in film)", a[1])
				for item in s:
					item.strip()
					# print item
					if item not in self.dates:
						self.dates.append(item.strip())
# make a parser that can get information from one line of html
class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.starttag = None
		self.attrs = {}
		self.data = ''

	def handle_starttag(self, tag, attrs):
		self.starttag = (tag)
		for attr in attrs:
			if len(attr)==2:
				# print attr
				self.attrs[attr[0]] = attr[1]
	def handle_data(self, data):
		self.data += data+' '
	def resets(self):
		self.starttag = None
		self.attrs = {}
		self.data = ''


#checks to see if a film is in the right date range
def find_date(arr,parser):
	parser.resets()
	for link in arr:
		parser.feed(str(link))
	return '-'.join(parser.dates)

def get_html_from_link(link):
	return urllib.urlopen(link).read()

def get_links(soup):
	# initate variables
	film_links = {}

	# initialize parser objects
	parser = DateParser()
	parser1 = MyHTMLParser()

	#iterate through tables of movies and get all movies between begin and end
	for item in soup.find_all('table', {'class':'wikitable'}):
		if not item:
			continue
		#find dates corresponding to links
		date = find_date(item.find_all('a'),parser)
		#Go through all films and parse out the url
		for film in item.find_all('tr')[1:]:
			film_list = film.contents
			for x in film_list:
				if not str(x).strip():
					film_list.remove(x)
			parser1.feed(str(film_list[0]))
			if parser1.attrs['href'].startswith('#endnote'):
				continue
			film_links[parser1.attrs['title']] = ("{0}{1}".format('http://en.wikipedia.org',parser1.attrs['href']),date)
	return film_links

def get_info(url):
	# initialize parser objects
	attr = {}
	# print url
	targetCategory = ['Release dates','Budget']
	parser = MyHTMLParser()

	#initiate soup object from url
	htmlDoc = get_html_from_link(url).decode("utf8")
	soup = BeautifulSoup(htmlDoc)
	
	# print soup.prettify()
	for item in soup.find_all('table', {'class':'infobox vevent'}):
		for row in item.find_all('tr'):
			row_list = row.contents
			for x in row_list:
				try:
					if not str(x).strip():
						row_list.remove(x)
				except:
					pass
			if len(row_list) == 2:
				# get information 
				parser.resets()
				parser.feed(str(row_list[0]))
				category = parser.data
				category = re.sub(r"\n", "", category)
				category = category.strip()
				if category not in targetCategory:
					continue

				# get the data and clean it
				parser.resets()
				parser.feed(str(row_list[1]))
				data = parser.data
				data = data.replace('\xc2\xa0',' ')
				data = data.replace("\xe2\x80\x93",'-')
				data = ''.join(data.split('\n'))
				data = ' '.join(data.split())
				data = re.sub(r'\[[^)]*\]', '', data)
				attr[category] = data
		if 'Budget' in attr:
			print attr['Budget']
		return attr

def main():
	# initialize variables
	film_links = {}
	film_data = {}

	#parse the link and get the source code
	html_doc = get_html_from_link('http://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture')

	#initiate soup object
	soup = BeautifulSoup(html_doc)
	
	#get all films
	film_links = get_links(soup)


	# get relevant information for all films
	for film in film_links:
		# try:
		film_data[film] = get_info(film_links[film][0])
		# except:
			# pass
		# break
	print
	for key in film_data:
		if 'Budget' in film_data[key]:
			temp = film_data[key]['Budget']
			# temp = re.findall(r"\$?\\xe2?\d+million?", temp)
			if '\xc2\xa3' in temp and '$' not in temp:
				print temp

if __name__ == '__main__':
	main()

