####################################
# File name: wiki_parser.py        #
# Author: Tommy Inouye             #
# Date: 03/24/12                   #
# Description:  write a script to  #
# scrape the budgets of the Academy#
# Award Best Picture winners from  #
# Wikipedia.                       #
####################################

from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
from eval_cost import convert_to_euros, parse_to_float, parse_string
import re, urllib, csv


# Parser that looks for the date using regular expressions
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

#This function will strip the first subscript from html string
def remove_subs(x):
	#remove superscript tag
	temp = re.findall(r'(<sup(.*?)</sup>)',x)
	if not temp:
		return x
	if len(temp) > 0:
		if len(temp[0])>0:
			x = x.replace(str(temp[0][0]),'')
	return x


#checks to see if a film is in the right date range
def find_date(arr,parser):
	parser.resets()
	for link in arr:
		parser.feed(str(link))
	return '-'.join(parser.dates)

# gets the html from a url
def get_html_from_link(link):
	return urllib.urlopen(link).read()

#will get url and date associated to a film 
def get_links(soup):
	# initate variables
	filmLinks = {}
	dateLinks = {}

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
			filmList = film.contents
			for x in filmList:
				if not str(x).strip():
					filmList.remove(x)
			parser1.feed(str(filmList[0]))
			if parser1.attrs['href'].startswith('#endnote'):
				continue
			#update all relevant dictionaries
			filmLinks[parser1.attrs['title']] = "{0}{1}".format('http://en.wikipedia.org',parser1.attrs['href'])
			dateLinks.setdefault(date,[])
			dateLinks[date].append(parser1.attrs['title'])
	return filmLinks, dateLinks

#given a url, will go to that page and parse the infobox for the budget and release date
def get_info(url):
	# initialize variables
	attr = {}
	targetCategory = ['Release dates','Budget']

	# initialize parser objects
	parser = MyHTMLParser()

	#initiate soup object from url
	htmlDoc = get_html_from_link(url).decode("utf8")
	soup = BeautifulSoup(htmlDoc)
	
	#parse through every element in infobox
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
				# get information and put through html parser
				parser.resets()
				#get the category and clean it
				parser.feed(str(row_list[0]))
				category = parser.data
				category = re.sub(r"\n", "", category)
				category = category.strip()
				#check to see if in target category (aka release date or budget)
				if category not in targetCategory:
					continue

				# get the data and clean it
				parser.resets()
				parser.feed(remove_subs(str(row_list[1])))
				data = parser.data
				data = data.replace('\xc2\xa0',' ')
				data = data.replace("\xe2\x80\x93",'-')
				data = ''.join(data.split('\n'))
				data = ' '.join(data.split())
				data = re.sub(r'\[[^)]*\]', '', data)
				attr[category] = data
		return attr

#given all dictionaries, create the output csv file
def make_csv(links,data,dates):
	# initialize variables
	csv_name = 'output.csv'
	total = 0
	number = 0

	#make general output file
	with open(csv_name,'wb') as fp:
		a = csv.writer(fp,delimiter=',')
		a.writerow(['Name','Release-date','Budget','Estimated budget (in Dollars)','link'])
		#sort films by date
		for date in sorted(dates):
			a.writerow([date])
			#initialize average variables
			avg = 0
			num = 0
			#output all relevant information about film
			for key in dates[date]:
				arr = []
				arr.append(key)
				d = data[key]
				if 'Release dates' in d:
					arr.append(d['Release dates'])
				else:
					arr.append('N/A')
				if 'Budget' in d:
					arr.append(d['Budget'])
					arr.append(d['Cost'])
					avg += d['Cost']
					num += 1
					total += d['Cost']
					number += 1
				else:
					arr.append('N/A')
					arr.append('N/A')
				arr.append(links[key])
				a.writerow(arr)
			# write out the average if it exists
			if num == 0:
				a.writerow(['None of the budgets were available for this period'])
			else:
				a.writerow(['The average for this period was ${0:.2f}'.format(avg/num)])
			a.writerow([])
		#write total average over all years
		a.writerow(['The total average for all films was ${0:.2f}'.format(total/number)])

def main():
	print "Stage 1: Parsing through wikipedia page and getting the date and url of every film"
	# initialize variables
	filmLinks = {}
	filmData = {}

	#parse the link and get the source code
	html_doc = get_html_from_link('http://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture')

	#initiate soup object
	soup = BeautifulSoup(html_doc)
	
	#get all dictionary of urls and dates
	filmLinks,dateLinks = get_links(soup)

	print "Stage 2: Retrieving the budget and release date of every film from their respective urls"
	# get relevant information for all films
	for film in filmLinks:
		try:
			filmData[film] = get_info(filmLinks[film])
		except:
			pass
	#estimate the cost from budget information
	for key in filmData:
		if 'Budget' in filmData[key]:
			temp = filmData[key]['Budget']
			val, is_euro = parse_string(temp)
			if not val:
				continue
			filmData[key]['Cost'] = parse_to_float(val,is_euro)
	
	#make the csv file with all relevant information
	print "Stage 3: Creating Output.csv which is a csv file with all relevant information"
	make_csv(filmLinks,filmData,dateLinks)
	print "Done."
	
if __name__ == '__main__':
	main()

