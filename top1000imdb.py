# top1000imdb.py
# Name: Toan Minh Do
# CS 483 - Assignment 1
# September 10th, 2019
# Prof. Ben McCamish

import datetime
import pandas as pd
import requests
import csv
from bs4 import BeautifulSoup

# Collects the current date and time
d = datetime.datetime.today()
# Open a blank csv file
csvFile = csv.writer(open('data.csv', 'w'))
# Specify how many pages needed to be scraped
pages = 20
# URL for imdb's most popular crime films/shows/games
# Users can modify the text after '?genres=' to any other genres if desired
url = 'http://www.imdb.com/search/title?genres=crime'
# Counter for debugging
i = 1

# Arrays for storing data 
# A = Titles, B = Release Year, C = Genre, D = URL
A=[]
B=[]
C=[]
D=[]

print("***IMDb Top 1000 Popular Crime Films/Shows/Games Scraper***")
print("")
print("Now collecting data...")

# Loop for collecting data on multiple pages
while pages > 0:
	request = requests.get(url).text
	soup = BeautifulSoup(request, 'lxml')

	# Scrape all related data and store them in arrays
	for product in soup.find_all('div', class_='lister-item-content'):
		# Scrape titles
		name = product.a.text
		A.append(name)
		# Collects the title's URL
		imdbURL = product.a.get('href')
		if not imdbURL.startswith("http://www.imdb.com"):
			imdbURL = "http://www.imdb.com" + imdbURL
		# Scrape year
		year = product.find('span', class_='lister-item-year').text
		B.append(year)
		# Scrape genre
		genre = product.find('span', class_='genre').text
		C.append(genre)
		D.append(imdbURL)

		# Creates a pandas dataframe and export csv file with data from the arrays
		df = pd.DataFrame(A, columns=['Title'])
		df['Release Year'] = B
		df['Genre'] = C
		df['IMDb Page Link'] = D
		df.to_csv('data.csv')

	# Finds the next page's URL in order to re-scrape
	nexturl = soup.find('a', class_="lister-page-next").get('href')
	url = "http://www.imdb.com" + nexturl
	pages = pages - 1
	# Debug counter
	i = i + 1
	
print("Exported data to CSV file!")
print("")
print("Database has been updated on ", d)
print("Scraping complete!")

