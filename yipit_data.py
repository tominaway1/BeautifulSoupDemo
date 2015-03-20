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
	def __init__(self,start,end):
		HTMLParser.__init__(self)
		self.is_valid = False
		self.start = int(start)
		self.end = int(end)

	def resets(self):
		self.is_valid = False

	def handle_starttag(self, tag, attrs):
		for a in attrs:
			if a[0] == 'title':
				s = re.findall(r"[^#]+(?=in film)", a[1])
				for item in s:
					item.strip()
					# print item
					try:
						if int(item) > self.start and int(item)< self.end:
							self.is_valid = True
						else:
							self.is_valid = False
							return
					except:
						pass

class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.starttag = None
		self.attrs = {}
		self.data = None

	def handle_starttag(self, tag, attrs):
		self.starttag = (tag)
		for attr in attrs:
			if len(attr)==2:
				# print attr
				self.attrs[attr[0]] = attr[1]
	def handle_data(self, data):
		self.data = data

parser = DateParser(1920,1930)
parser1 = MyHTMLParser()

#checks to see if a film is in the right date range
def validate_date(arr):
	parser.resets()
	for link in arr:
		parser.feed(str(link))
	return parser.is_valid


def main():
	# initialize variables
	film_links = {}
	fild_data = {}

	#parse the link and get the source code
	link = 'http://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture'
	f = urllib.urlopen(link)
	html_doc = f.read()

	#initiate soup object
	soup = BeautifulSoup(html_doc)
	# print soup.prettify
	
	#iterate through tables of movies and get all movies between 1920-1930
	for item in soup.find_all('table', {'class':'wikitable'}):
		if not item:
			continue
		#validate that the dates for all films in table are between right dates
		if validate_date(item.find_all('a')):
			#Go through all films and parse out the url
			for film in item.find_all('tr')[1:]:
				film_list = film.contents
				for x in film_list:
					if not str(x).strip():
						film_list.remove(x)
				parser1.feed(str(film_list[0]))
				film_links[parser1.attrs['title']] = "{0}{1}".format('http://en.wikipedia.org',parser1.attrs['href'])
	print film_links
	print len(film_links)
	

if __name__ == '__main__':
	main()

