import db
import crawl
import const

# This function is called every week to crawl the website and store the data in the database
def execute_weekly_job():
    connection= db.create_connection()
    if connection is None:
        exit()

    # Create a cursor
    cursor = connection.cursor()
    
    # Create the table if it does not exist
    db.create_table_if_not_exists()

    # Crawl the website and store the data in the database
    crawl.crawl_website(connection, cursor, const.URL)
