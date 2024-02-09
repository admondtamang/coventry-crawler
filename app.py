import db
import jobs
from flask import Flask, render_template, request, jsonify

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Add a job to the scheduler function every week
scheduler = BackgroundScheduler()
scheduler.add_job(func=jobs.execute_weekly_job, trigger="interval", weeks=1)
scheduler.start()

# serve the home page
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


if __name__ == '__main__':
    app.run(debug=True)