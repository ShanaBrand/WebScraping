from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/weather_app"
mongo = PyMongo(app)


#conn = 'mongodb://localhost:27017'

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.marsDb
db.scrapeMars.drop()


@app.route("/")
def index():
    # write a statement that finds all the items in the db and sets it to a variable

   scrapeMars = mongo.db.collection.find()
    # render an index.html template and pass it the data you retrieved from the database
   return render_template("marsIndex.html", scrapeMars=scrapeMars)


@app.route("/scrape")

def scrape_info():

    # Run scraped functions
    myScrape = scrape_mars.scrape()

    # Store results into a dictionary
    marsdata = {
        "news": myScrape["latest_News"],
        "featuredImage": myScrape["feaured_Img"],
        "marsWeather": myScrape["latest_weather"],
        "marsFacts": myScrape["marsFacts"],
        "marHemisphere": myScrape["mars_hemisphere"]
    }

    # Insert forecast into database
    mongo.db.collection.insert_one(marsdata)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)