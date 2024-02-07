import db
import crawl
import const
import schedule
import time
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

# This function is called every week to crawl the website and store the data in the database
def execute_weekly_job(connection, cursor):
    db.create_table_if_not_exists(connection, cursor)
    crawl.crawl_website(connection, cursor, const.URL)


def run_schedule():
    # schedule every monday at 00:00 weekly job
    schedule.every().monday.do(execute_weekly_job)
    
    # for testing in every 10 minutes
    # schedule.every(10).seconds.do(execute_weekly_job, connection, cursor)

    while True:
        schedule.run_pending()
        time.sleep(1)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    # get the search term from the query string in query parameter 'q'
    search_term = request.args.get('q')
    print(search_term,"search_term")
    results = db.search_query(search_term)
    return jsonify(results)


if __name__ == "__app__":
      # Start a separate thread to run the schedule
    import threading
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()


