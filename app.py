import numpy 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask

# #################################################
# # Database Setup
# #################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (f"Here are the available routes: <br/>"
    f"/api/v1.0/precipitation<br/>"
    f"api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/[start_date formatted as yyyy-mm-dd]<br/>"
    f"/api/v1.0/[start_date formatted as yyyy-mm-dd]/[end_date formatted as 'yyyy-mm-dd'<br/>")


# 4. Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23').\
                filter(Measurement.station == 'USC00519281').all()
    
    session.close()

    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)
