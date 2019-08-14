# import dependancies

import numpy as np

import sqlalchemy

from sqlalchemy.ext.automap import automap_base

from sqlalchemy.orm import Session

from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

# Setup database & Create engine

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect database and tables

Base = automap_base()

Base.prepare(engine, reflect=True)

# save reference to the table

Measurement = Base.classes.measurement

Station = Base.classes.station

# create session

session = Session(engine)

# Setup Flask

app = Flask(__name__)

# Routes:


@app.route("/")
def welcome():

# List all routes:

    return (

        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>")


# precipitation

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Return a list of rainfall by date
    # Query all precipitation
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Create a dictionary from the row data and append to a list
    all_Measurements = []
    for date, precipitation in results:
        Measurements_dict = {}
        Measurements_dict["date"] = date
        Measurements_dict["prcp"] = precipitation
        all_Measurements.append(Measurements_dict)

    return jsonify(all_Measurements)

#  Stations


@app.route("/api/v1.0/stations")
def stations():
    # Return a list of all stations names
    # Query all stations
    session = Session(engine)
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

#   tobs

@app.route("/api/v1.0/tobs")
def yeartemps():

    yr_temps = []
    session = Session(engine)
    # lastday = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    tobs_data = session.query(func.strftime("%Y-%m-%d", Measurement.date), Measurement.tobs).filter(func.strftime("%Y-%m-%d", Measurement.date) >= dt.date(2016, 8, 23)).all()
    yr_temps=list(np.ravel(tobs_data))
    return jsonify(yr_temps)



@app.route("/api/v1.0/<start_date>/<end_date>")
#/api/v1.0/2019-08-10/2019-08-12
#/api/v1.0/2019-08-10

def trip(start_date, end_date = dt.date.today()):
    round_trip_temps = []

    session = Session(engine)

    results_min = session.query(func.min(Measurement.tobs)).filter(func.strftime("%Y-%m-%d", Measurement.date) >= dt.datetime.strptime(start_date, '%Y-%m-%d'), func.strftime("%Y-%m-%d", Measurement.date) <= dt.datetime.strptime(end_date, '%Y-%m-%d')).all()
    results_max = session.query(func.max(Measurement.tobs)).filter(func.strftime("%Y-%m-%d", Measurement.date) >= dt.datetime.strptime(start_date, '%Y-%m-%d'), func.strftime("%Y-%m-%d", Measurement.date) <= dt.datetime.strptime(end_date, '%Y-%m-%d')).all()
    results_avg = session.query(func.avg(Measurement.tobs)).filter(func.strftime("%Y-%m-%d", Measurement.date) >= dt.datetime.strptime(start_date, '%Y-%m-%d'), func.strftime("%Y-%m-%d", Measurement.date) <= dt.datetime.strptime(end_date, '%Y-%m-%d')).all()
    
    round_trip_temps= {
        "min": results_min, 
        "max": results_max, 
        "avg": results_avg
        }
    
    return jsonify(round_trip_temps)


if __name__ == '__main__':
    app.run(debug=True)
