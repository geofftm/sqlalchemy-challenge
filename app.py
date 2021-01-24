import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

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
    f"/api/v1.0/[start_date formatted as yyyy-mm-dd]/[end_date formatted as 'yyyy-mm-dd']<br/>")


# 4. Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23').\
                filter(Measurement.station == 'USC00519281').all()
    
    session.close()

    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

#Tobs

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station, Station.name).order_by(Station.station).all()
    
    session.close()

    all_stations = list(np.ravel(results))
   
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23').\
    filter(Measurement.station == 'USC00519281').all()
    
    session.close()

    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
   
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), 
              func.max(Measurement.tobs),
              func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    
    session.close()

    all_start_dates = []
    for min_tobs, max_tobs, avg_tobs in results:
        mma_tobs_dict = {}
        mma_tobs_dict["min tobs"] = min_tobs
        mma_tobs_dict["max tobs"] = max_tobs
        mma_tobs_dict["avg tobs"] = avg_tobs

        all_start_dates.append(mma_tobs_dict)
   
    return jsonify(all_start_dates)


@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), 
              func.max(Measurement.tobs),
              func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    session.close()

    all_start_end = []
    for min_tobs, max_tobs, avg_tobs in results:
        se_mma_tobs_dict = {}
        se_mma_tobs_dict["min tobs"] = min_tobs
        se_mma_tobs_dict["max tobs"] = max_tobs
        se_mma_tobs_dict["avg tobs"] = avg_tobs

        all_start_end.append(se_mma_tobs_dict)
   
    return jsonify(all_start_end)


if __name__ == '__main__':
    app.run(debug=True)