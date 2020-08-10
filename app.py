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
   marsData = scraping.scrapeAll()
   mars.update({}, marsData, upsert=True)
   return render_template("scrape.html")

@app.route("/hemispheres/<title>")
def hemisphere1(title):
   
   mars = mongo.db.mars.find_one()
   url = None
   if title == mars["hemisphere1_title"]:
      url = mars["hemisphere1_url"]
   elif title == mars["hemisphere2_title"]:
      url = mars["hemisphere2_url"]
   elif title == mars["hemisphere3_title"]:
      url = mars["hemisphere3_url"]
   elif title == mars["hemisphere4_title"]:
      url = mars["hemisphere4_url"]

   return render_template("hemisphere.html", title=title,url=url,mars=mars )

#%%
if __name__ == "__main__":
   app.run()