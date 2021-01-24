from flask import Flask, jsonify

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
#route is where you tell your content to go and execute
@app.route("/")
def home():
    return ("Here are the available routes: "
    "/api/v1.0/precipitation"
    "api/v1.0/stations"
    "/api/v1.0/tobs")


# 4. Define what to do when a user hits the /about route
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

@app.route("/ding")
def ding():
    print("Server received request for 'About' page...")
    #return "Welcome to my 'About' page!"
    

if __name__ == "__main__":
    app.run(debug=True)