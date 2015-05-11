README.txt

The goal is to write a script to scrape the budgets of the Academy
Award Best Picture winners from Wikipedia. It must use the page 
http://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture#1920s, follow the link for each year’s winner,
and grab the budget from the box on the right of the page, and print out each 
Year-Title-Budget combination. After printing each combination, it should print 
the average budget at the end.


Libraries/Languages that I used:
I decided to use Python for this assignment. I have Python 2.7.6 installed. 

Below are the libraries that I used.
1) Beautiful soup v4.3.2  -> http://www.crummy.com/software/BeautifulSoup/bs4/doc/
2) HTMLParser, re, urllib and csv from python library

How do I run the program:
The main file is wiki_parser.py and can be run by running "python wiki_parser.py" in terminal.
This file will visit http://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture, get all the films
in the page, and visit every associated page and parse out relevant information. Then it creates 
an output csv file called "output.csv" which can be opened in excel. Every film is separated by 
the year[s] it came out and prints out the average budget for all the films that year. 

Approach: 
My initial thought was to use the Wikipedia API. This wound
up being a horrible idea. The API was not able to give back nearly enough information and was not 
useful for this assignment. So instead, I decided to work with the source code of the page. Looking 
at the HTML code of the page, I realized that it was really easy to parse through the HTML and 
to iterate through the tables. Through a little research, I found that BeautifulSoup was a very
efficient library for the task as it had very good documentation and many features. 

Edge cases and roadblocks:
I had a few edge cases and roadblocks in this assignment. The really obvious edge case was the fact 
that not all films had a budget on their wikipedia page. I handled this by just specifying that these 
prices were not available and not including it in the calculations for the average costs. The other 
complications were how I handled the budget prices. It was rarely just a price and half the time 
included "million". I handled all the cases using the regular expression library to parse out all 
strings that were in the correct form. Another complication was that half the budgets were in euros 
so I had to convert it to dollars when calculating the averages. There was one case where there was 
a subscript in the way that interfered with parsing the html and to resolve it, I created a function 
that will remove any substring that is in within the tag <sup </sup>. 

