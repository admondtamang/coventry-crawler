
import db
import os
import time
import requests
from bs4 import BeautifulSoup

from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import scoring
import robotexclusionrulesparser

index_path = "indexdir"
rerp = robotexclusionrulesparser.RobotExclusionRulesParser()

def crawl_website(url):
    response= requests.get(url)

    # Initialize Whoosh index
    schema = Schema(title=TEXT(stored=True), authors=TEXT(stored=True), year=ID(stored=True))
    
    if not os.path.exists(index_path):
        os.mkdir(index_path)
        
    ix = create_in(index_path, schema)
    writer = ix.writer()

    results = []

    # scraping data and storing it in csv file
    if response.status_code == 200:

        responseText= response.text

        # parse the robots.txt file 
        if responseText.is_allowed("*", url):
            # Fetch the page if allowed by robots.txt
            response = requests.get(url)
            
        soup= BeautifulSoup(responseText, 'html.parser')

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
            # data={'Year': year, 'Title': title, 'Link': link, 'Authors': authors}
            # db.insert_data( data)
            # Append results to the list
            
            results.append({
                'title': title,
                'authors': authors,
                'year': year,
                'link': link,
            })

        # Commit changes to the Whoosh index
        writer.commit()
        time.sleep(1)



def search_publications(query):
    # Open the existing Whoosh index
    ix = open_dir(index_path)
    final_results = []
    with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
        # Parse the query to search in multiple fields
        query_parser = MultifieldParser(["title", "authors"], ix.schema)
        query = query_parser.parse(query)
        
        # Perform the search and retrieve results
        results = searcher.search(query, terms=True)
        for result in results:
            final_results.append({
                "title": result['title'],
                "authors": result['authors'],
                "year": result['year'],
            })

    return final_results