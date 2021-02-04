##################################################
## SQL and database prep

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import os
import datetime as dt

from sqlalchemy.sql.expression import null

# Engine to hawaii.sqlite
path = os.path.join("Resources", "hawaii.sqlite")
engine = create_engine(f"sqlite:///{path}")

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

## SQL and database prep
##################################################

###########
## Flask ##
###########

# Flask to host the API
from flask import Flask, jsonify
app = Flask(__name__)

############
## ROUTES ##

@app.route("/")
def home():
    body = "<div><b>Options</b></div>\
        <ul>\
            <li><a href='/api/v1.0/precipitation'>Precipitation Data</li>\
            <li><a href='/api/v1.0/stations'>Station Data</li>\
            <li><a href='/api/v1.0/tobs'>Temperature Data</li></a>\
            <li>Date Range: substitute a starting date and an optional ending date into the following link** -- /api/v1.0/startdate/enddate</li>\
        </ul>\
        <p>** Please use YYYY-MM-DD format for dates</p>"
    return body

@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    # Get all precipitation data averaged per day
    precip = session.query(Measurement.date, func.round(func.avg(Measurement.prcp),2)).\
        group_by(Measurement.date).all()
    session.close()
    return jsonify(dict(precip))

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    # Get all station names
    stations = session.query(Station.name).all()
    session.close()
    stations = [x[0] for x in stations] # unpack the tuples
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp():
    session = Session(engine)
    # Get most recent data point in the database
    end_date = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).\
        limit(1).all()[0][0]

    # Calculate the date one year from the last date in data set
    start_date = dt.date.isoformat(dt.date.fromisoformat(end_date) - dt.timedelta(days=365))

    # Get the most active station ID
    most_active = engine.execute("\
        SELECT s.station, count(s.name) AS count\
        FROM measurement m\
        JOIN station s\
            ON m.station = s.station\
        GROUP BY s.name\
        ORDER BY count DESC\
        LIMIT 1").fetchall()[0][0]
    
    # Perform a query to retrieve the data and temp from the most active station
    temp_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start_date).filter(Measurement.station == most_active).all()
    
    session.close()
    return jsonify(dict(temp_data))

@app.route("/api/v1.0/<start>/", defaults={"end": null})
@app.route("/api/v1.0/<start>/<end>")
def rangedata(start, end):
    session = Session(engine)

    # Perform a query to retrieve the data and temp from the most active station
    if end is null:
        temp_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    else:
        temp_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    keys = ("min","max","avg")
    temp_dict = dict(zip(keys, *temp_data))

    session.close()
    return jsonify(temp_dict)

## END ROUTES ##
################

if __name__ == "__main__":
    app.run(debug=True)
