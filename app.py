#%%
from flask import Flask, render_template
from flask_pymongo import PyMongo
import missionToMarsScraping as scraping

# %%
# Create Flask app 
app = Flask(__name__)

#%%
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# %%
# Define the home page of the Flask app
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Define the scraping route of the Flask app
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   marsData = scraping.scrape_all()
   mars.update({}, marsData, upsert=True)
   return "Scraping Successful!"

if __name__ == "__main__":
   app.run()