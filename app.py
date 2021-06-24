import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
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
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    
    raw_data = session.query(Measurement.date, Measurement.prcp).all()

    result_list = []

    for row in raw_data:
        result_dict = {}
        result_dict[row.date] = row.prcp
        result_list.append(result_dict)

    session.close()
    
    return(jsonify(result_list))

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    raw_data = session.query(Station).all()

    result_list = []

    for row in raw_data:
        result_dict = {}
        result_dict["id"] = row.id
        result_dict["station"] = row.station
        result_dict["name"] = row.name
        result_list.append(result_dict)

    session.close()

    return(jsonify(result_list))

@app.route("/api/v1.0/tobs")
def temps():
    session = Session(engine)
    
    dates_ordered = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()

    last_date = str(dates_ordered[0])
    last_date_dt = dt.datetime.strptime(last_date, "%Y-%m-%d")
    year_ago = last_date_dt - dt.timedelta(days=365)
    
    station_use = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()

    most_active = station_use[0][0]

    data_last_year = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active).\
        filter(Measurement.date > year_ago).\
        filter(Measurement.date <= last_date_dt).all()

    result_list = []

    for row in data_last_year:
        result_dict = {}
        result_dict["date"] = row.date
        result_dict["tobs"] = row.tobs
        result_list.append(result_dict)

    session.close()
    
    return(jsonify(result_list))

if __name__ == '__main__':
    app.run(debug=True)
