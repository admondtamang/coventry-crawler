
import db
import requests
from bs4 import BeautifulSoup

def crawl_website( connection, cursor, url):
    response= requests.get(url)

    # scraping data and storing it in csv file
    if response.status_code == 200:
        soup= BeautifulSoup(response.text, 'html.parser')

        # get all publications from the page
        publications_elements= soup.find_all('div', class_='result-container')

        for publication in publications_elements:
            # title  
            titleElement= publication.find('h3', class_='title')
            if titleElement:
                title= titleElement.get_text(strip=True)

            # authors
            authorsElement= publication.find_all('a', class_='link person')
            authors = [author.get_text(strip=True) for author in authorsElement] if authorsElement else None

            # convert array of string to string and validate string
            authors= ', '.join(authors) if authors else None

            # year  
            publiicationYearElement= publication.find('span', class_='date')
            if publiicationYearElement:
                year= publiicationYearElement.get_text(strip=True)
            
            # link
            publiicationLinkElement= publication.find('a', class_='link')
            if publiicationLinkElement:
                link= publiicationLinkElement['href']


            # Insert to database
            data={'Year': year, 'Title': title, 'Link': link, 'Authors': authors}
            db.insert_data( data)
