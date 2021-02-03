from flask import Flask, jsonify

app = Flask(__name__)

################
#### ROUTES ####
################
@app.route("/")
def home():
    menu = "<div><b>Options</b></div>\
        <p><a href='/api/v1.0/precipitation'>Precipitation Data</p>\
        <p><a href='/api/v1.0/station'>Station Data</p>\
        <p><a href='/api/v1.0/tobs'>Temperature Data</p>\
        <p><a href='/api/v1.0/daterange'>Date Range</p>"
    return menu

@app.route("/api/v1.0/precipitation")
def precip():
    pass

@app.route("/api/v1.0/stations")
def station():
    pass

@app.route("/api/v1.0/tobs")
def temp():
    pass

@app.route("/api/v1.0/daterange")
def range():
    pass

@app.route("/api/v1.0/<start>/<end>")
def range():
    pass

################
## END ROUTES ##
################

if __name__ == "__main__":
    app.run(debug=True)
