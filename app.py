##################################################################################
## SQL and database prep

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import os

# Engine to hawaii.sqlite
path = os.path.join("Resources", "hawaii.sqlite")
engine = create_engine(f"sqlite:///{path}")

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

##################################################################################

# Flask to host the API
from flask import Flask, jsonify

app = Flask(__name__)

################
#### ROUTES ####
################
@app.route("/")
def home():
    body = "<div><b>Options</b></div>\
        <ul>\
            <li><a href='/api/v1.0/precipitation'>Precipitation Data</li>\
            <li><a href='/api/v1.0/station'>Station Data</li>\
            <li><a href='/api/v1.0/tobs'>Temperature Data</li>\
            <li>Date Range: substitute a starting date and an optional ending date into the following link\
                <li>/api/v1.0/<start>/<end><\li>\
            </li>\
        </ul>"
    return body

@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    session.close()

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    session.close()

@app.route("/api/v1.0/tobs")
def temp():
    session = Session(engine)
    session.close()

@app.route("/api/v1.0/<start>/<end>")
def rangedata():
    session = Session(engine)
    session.close()

################
## END ROUTES ##
################

if __name__ == "__main__":
    app.run(debug=True)
