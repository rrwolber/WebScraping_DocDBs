from flask import Flask, render_template, redirect
from scrape_mars import scrape
import pymongo



app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.marsDB



@app.route("/")
def index():
    mars = db.marsDB.find_one()
    return render_template("index.html", mars = mars)



@app.route("/scrape")
def scraper():
    db.marsDB.drop()
    mars_data = scrape()
    db.marsDB.update(
        {},
       mars_data,
       upsert=True
    )
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
