import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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

session = Session(engine)

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
    raw_data = session.query(Measurement.date, Measurement.prcp).all()

    result_list = []

    for row in raw_data:
        result_dict = {}
        result_dict["date"] = row.date
        result_dict["prcp"] = row.prcp
        result_list.append(result_dict)

    return(jsonify(result_list))

@app.route("/api/v1.0/stations")
def stations():
    raw_data = session.query(Station).all()

    result_list = []

    for row in raw_data:
        result_dict = {}
        result_dict["id"] = row.id
        result_dict["station"] = row.station
        result_dict["name"] = row.name
        result_list.append(result_dict)

    return(jsonify(result_list))

if __name__ == '__main__':
    app.run(debug=True)
