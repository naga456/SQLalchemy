from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import datetime as dt
from datetime import timedelta, date
from datetime import datetime

app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine,reflect=True)
# Save reference to tables
Measurement = Base.classes.measurement
Station =Base.classes.station



@app.route("/")
def home():
    return "<strong> Routes </strong>  \
    <br>  /api/v1.0/precipitation \
    <br>  /api/v1.0/stations   \
    <br>  /api/v1.0/tobs    \
    <br> /api/v1.0/start \
    <br>   /api/v1.0/start/end "

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of percipitation at date 
    """
    # Query all date and percipitation
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.prcp).all()

    all_prcp = []
    for date, prcp in results:
        prcp_dict ={}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)


    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    """
    Return a JSON list of stations
    """
    #Query the station dataset
    session = Session(engine)
    results= session.query(Station.name).all()
    #convert list of tuples into normal list
    all_names = list(np.ravel(results))
    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    """
    Return a JSON list of tobs from the measurement table
    """
    #Query the station dataset    
    session = Session(engine)
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date_dt = datetime.strptime('2017-08-23','%Y-%m-%d')
    year_ago = latest_date_dt- dt.timedelta(days=365)   #a year prior to the lastest date point
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > year_ago).order_by(Measurement.date).all()

    #convert list of tuples into normal list
    all_names = list(np.ravel(results))
    return jsonify(all_names)
    

@app.route("/api/v1.0/<start>")
def start(start):
    start_date = datetime.strptime(start,'%Y-%m-%d')
    # Query all date and percipitation
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    #convert list of tuples into normal list
    all_temps = list(np.ravel(results))
    return jsonify(all_temps)
    #return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def end(start,end):
    start_date = datetime.strptime(start,'%Y-%m-%d')
    end_date = datetime.strptime(end,'%Y-%m-%d')
    # Query all date and percipitation
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    #convert list of tuples into normal list
    all_temps = list(np.ravel(results))
    return jsonify(all_temps)



if __name__ == "__main__":
    app.run(debug=True)

