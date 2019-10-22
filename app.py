from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")
# # Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
# mongo = PyMongo(app)

# Create a root route / that will query your Mongo database and pass the mars data into an HTML template to display the data.
# Use Pymongo for CRUD applications for your database. For this homework, you can simply overwrite the existing document each time the /scrape url is visited and new data is obtained.

# ======= test run for a new scrape function =======
# Error: jinja2.exceptions.UndefinedError: 'None' has no attribute 'hemisphere_dictlist'
# Due to DB is empty or has partial record columns not all columns values which are needed by index.html to render the page
# artial record columns: like new data 'hemisphere_dictlist' is the result of new scrape function, still not exist in Mango DB 'mars' yet.
# Because: this route "/" is directly search from MongoDB 'mars'
# after new scrape code is developed the first test run should run "/scrape" to generate the new data and write it into DB by rounte "/scrape".
# ================================================== 

# Route to render index.html template using data from Mongo
@app.route("/")
def home():


    # Find one record of data from the mongo database collection mars
    marsdata_mgl = mongo.db.mars.find_one()
    # teams = list(db.team.find())
    # Return template and data
    return render_template("index.html", marsdata_html = marsdata_mgl)



# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    marsdata_scrp = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars.update({}, marsdata_scrp, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
