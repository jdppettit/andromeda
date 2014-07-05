from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import *

from credentials import *
from password import *
import datetime
import json
import requests
from pytz import timezone
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
connectionString = "mysql://%s:%s@%s:3306/%s" % (USERNAME, PASSWORD, HOSTNAME, DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = connectionString
db = SQLAlchemy(app)
app.secret_key = SECRET_KEY

class BedroomHumidity(db.Model):
	__tablename__ = "bedroom_humidity"

	id = db.Column(db.Integer, primary_key=True)
	humidity = db.Column(db.Integer)
	date = db.Column(db.Date)

	def __init__(self, id, humidity, date):
		self.id = id
		self.humidity = humidity
		self.date = date

class OutsideHumidity(db.Model):
        __tablename__ = "outside_humidity"

        id = db.Column(db.Integer, primary_key=True)
        humidity = db.Column(db.Integer)
        date = db.Column(db.Date)

        def __init__(self, id, humidity, date):
                self.id = id
                self.humidity = humidity
                self.date = date

class OutsideTemperature(db.Model):
        __tablename__ = "outside_temp"

        id = db.Column(db.Integer, primary_key=True)
        temp = db.Column(db.Integer)
        date = db.Column(db.Date)

        def __init__(self, id, temp, date):
                self.id = id
                self.temp = temp
                self.date = date

class BedroomTemperature(db.Model):
        __tablename__ = "bedroom_temp"

        id = db.Column(db.Integer, primary_key=True)
        temp = db.Column(db.Integer)
        date = db.Column(db.Date)

        def __init__(self, id, temp, date):
                self.id = id
                self.temp = temp
                self.date = date

class ClosetTemperature(db.Model):
        __tablename__ = "closet_temp"

        id = db.Column(db.Integer, primary_key=True)
        temp = db.Column(db.Integer)
        date = db.Column(db.Date)

        def __init__(self, id, temp, date):
                self.id = id
                self.temp = temp
                self.date = date


class HouseTemperature(db.Model):
        __tablename__ = "house_temp"

        id = db.Column(db.Integer, primary_key=True)
        temp = db.Column(db.Integer)
        date = db.Column(db.Date)

        def __init__(self, id, temp, date):
                self.id = id
                self.temp = temp
                self.date = date

class Pressure(db.Model):
        __tablename__ = "pressure"

        id = db.Column(db.Integer, primary_key=True)
        pressure = db.Column(db.Integer)
        date = db.Column(db.Date)

        def __init__(self, id, pressure, date):
                self.id = id
                self.pressure = pressure
                self.date = date

def getPressure():
	pressureData = Pressure.query.order_by(Pressure.id.asc()).limit(720).all() 
	return pressureData

def getOutsideTemp():
	outsidetemp = OutsideTemperature.query.order_by(OutsideTemperature.id.asc()).limit(720).all()
	return outsidetemp

def getOutsideHumidity():
	outsidehumidity = OutsideHumidity.query.order_by(OutsideHumidity.id.asc()).limit(720).all()
	return outsidehumidity

def getBedroomHumidity():
	bedroomhumidity = BedroomHumidity.query.order_by(BedroomHumidity.id.asc()).limit(720).all()
	return bedroomhumidity

def getBedroomTemp():
	bedroomtemp = BedroomTemperature.query.order_by(BedroomTemperature.id.asc()).limit(720).all()
	return bedroomtemp

def getHouseTemp():
	housetemp = HouseTemperature.query.order_by(HouseTemperature.id.asc()).limit(720).all()
	return housetemp

def getClosetTemp():
	closettemp = ClosetTemperature.query.order_by(ClosetTemperature.id.asc()).limit(720).all()
	return closettemp

# ------------

def getPressureLast():
        pressureData = Pressure.query.order_by(Pressure.id.desc()).limit(1).first()
        return pressureData

def getOutsideTempLast():
        outsidetemp = OutsideTemperature.query.order_by(OutsideTemperature.id.desc()).limit(1).first()
        return outsidetemp

def getOutsideHumidityLast():
        outsidehumidity = OutsideHumidity.query.order_by(OutsideHumidity.id.desc()).limit(1).first()
        return outsidehumidity

def getBedroomHumidityLast():
        bedroomhumidity = BedroomHumidity.query.order_by(BedroomHumidity.id.desc()).limit(1).first()
        return bedroomhumidity

def getBedroomTempLast():
        bedroomtemp = BedroomTemperature.query.order_by(BedroomTemperature.id.desc()).limit(1).first()
        return bedroomtemp

def getHouseTempLast():
        housetemp = HouseTemperature.query.order_by(HouseTemperature.id.desc()).limit(1).first()
        return housetemp

def getClosetTempLast():
        closettemp = ClosetTemperature.query.order_by(ClosetTemperature.id.desc()).limit(1).first()
        return closettemp

# ------------

def isOkay(record):
	lastDateObj = record.date 
	warnTime = lastDateObj + datetime.timedelta(minutes=5)

	try:
		currentValue = record.humidity
	except:
		pass
	
	try: 
		currentValue = record.temp
	except:
		pass

	try:
		currentValue = record.pressure
	except:
		pass
	
	if warnTime < datetime.datetime.now():
		return False, str(lastDateObj), str(currentValue)
	else:
		return True, str(lastDateObj), str(currentValue)

def getHighLowPressure(hrs):
	time = datetime.datetime.now() - datetime.timedelta(hours=hrs)
	high = Pressure.query.filter(Pressure.date>=time).order_by(Pressure.pressure.asc()).first()
	low = Pressure.query.filter(Pressure.date>=time).order_by(Pressure.pressure.desc()).first()
	return high.pressure, low.pressure

def getHighLowTemp(thing, hrs):
	if thing == "ht":
		time = datetime.datetime.now() - datetime.timedelta(hours=hrs)
		high = HouseTemperature.query.filter(HouseTemperature.date>=time).order_by(HouseTemperature.temp.asc()).first()
		low = HouseTemperature.query.filter(HouseTemperature.date>=time).order_by(HouseTemperature.temp.desc()).first()
		return high.temp, low.temp
	elif thing == "bt":
		time = datetime.datetime.now() - datetime.timedelta(hours=hrs)
                high = BedroomTemperature.query.filter(BedroomTemperature.date>=time).order_by(BedroomTemperature.temp.asc()).first()
                low = BedroomTemperature.query.filter(BedroomTemperature.date>=time).order_by(BedroomTemperature.temp.desc()).first()
                return high.temp, low.temp
	elif thing == "ot":
		time = datetime.datetime.now() - datetime.timedelta(hours=hrs)
                high = OutsideTemperature.query.filter(OutsideTemperature.date>=time).order_by(OutsideTemperature.temp.asc()).first()
                low = OutsideTemperature.query.filter(OutsideTemperature.date>=time).order_by(OutsideTemperature.temp.desc()).first()
                return high.temp, low.temp
	elif thing == "ct":
		time = datetime.datetime.now() - datetime.timedelta(hours=hrs)
                high = ClosetTemperature.query.filter(ClosetTemperature.date>=time).order_by(ClosetTemperature.temp.asc()).first()
                low = ClosetTemperature.query.filter(ClosetTemperature.date>=time).order_by(ClosetTemperature.temp.desc()).first()
                return high.temp, low.temp

def getHighLowHumidity(thing, hrs):
	if thing == "bh":
		time = datetime.datetime.now() - datetime.timedelta(hours=hrs)
		high = BedroomHumidity.query.filter(BedroomHumidity.date>=time).order_by(BedroomHumidity.humidity.asc()).first()
		low = BedroomHumidity.query.filter(BedroomHumidity.date>=time).order_by(BedroomHumidity.humidity.desc()).first()
		return high.humidity, low.humidity
	elif thing == "oh":
		time = datetime.datetime.now() - datetime.timedelta(hours=hrs)
		high = OutsideHumidity.query.filter(OutsideHumidity.date>=time).order_by(OutsideHumidity.humidity.asc()).first()
                low = OutsideHumidity.query.filter(OutsideHumidity.date>=time).order_by(OutsideHumidity.humidity.desc()).first()
                return high.humidity, low.humidity

def getAllPressure(hrs):
	time = datetime.datetime.now() - datetime.timedelta(hours=hrs)
        allPressure = Pressure.query.filter(Pressure.date>=time).order_by(Pressure.pressure.asc()).all()
        return allPressure

def getPressureTrend():
	time = datetime.datetime.now() - datetime.timedelta(hours=6)
	pressureData = Pressure.query.filter(Pressure.date>=time).all()
	numIncreased = 0
	numDecreased = 0
	highHold = 0
	lowHold = 0
	for row in pressureData:
		if row.pressure > highHold:
			highHold = row.pressure
			numIncreased = numIncreased + 1
		if row.pressure < lowHold:
			lowHold = row.pressure
			numDecreased = numDecreased + 1
	if numIncreased > numDecreased:
		return 1
	elif numDecreased > numIncreased:
		return 0
	else:
		return 2

def getNagiosJSON():
	requestString = "https://andromeda.pettitservers.com:8080/state/"
	r = requests.get(requestString)
	json = r.json()
	nagiosStatus = {}
	for host in json['hosts']:
		nagiosStatus[json['hosts'][host]['host_name']] = json['hosts'][host]['current_state']
	return nagiosStatus

@app.route('/graphs')
def graphs():
	pressure6hr = getAllPressure(6)
	pressure24hr = getAllPressure(24)
	return render_template("graphs.html", pressure6hr = pressure6hr, pressure24hr = pressure24hr)

@app.route('/dashboard')
@app.route('/')
def index():
	nagiosStatus = getNagiosJSON()

	ht = getHouseTemp()
	ct = getClosetTemp()
	bt = getBedroomTemp()
	bh = getBedroomHumidity()
	ot = getOutsideTemp()
	oh = getOutsideHumidity()
	p = getPressure()
	
	htStat, htLast, htCurrent = isOkay(getHouseTempLast())
	ctStat, ctLast, ctCurrent = isOkay(getClosetTempLast())
	btStat, btLast, btCurrent = isOkay(getBedroomTempLast())
	bhStat, bhLast, bhCurrent = isOkay(getBedroomHumidityLast())
	otStat, otLast, otCurrent = isOkay(getOutsideTempLast())
	ohStat, ohLast, ohCurrent = isOkay(getOutsideHumidityLast())
	pStat, pLast, pCurrent = isOkay(getPressureLast())
	
	ohHigh, ohLow = getHighLowHumidity("oh", 24)
	bhHigh, bhLow = getHighLowHumidity("bh", 24)
	htHigh, htLow = getHighLowTemp("ht", 24)
	btHigh, btLow = getHighLowTemp("bt", 24)
	otHigh, otLow = getHighLowTemp("ot", 24)
	pHigh, pLow = getHighLowPressure()	
	ctHigh, ctLow = getHighLowTemp("ct", 24)

	trend = getPressureTrend()	

	return render_template('index.html', htStat=htStat, ctStat=ctStat, btStat=btStat, bhStat=bhStat, otStat=otStat, ohStat=ohStat, htLast=htLast, ctLast=ctLast, btLast=btLast, bhLast=bhLast, otLast=otLast, ohLast=ohLast, pHigh = pHigh, pLow = pLow, pStat = pStat, pLast = pLast, pCurrent = pCurrent, htCurrent = htCurrent, ctCurrent = ctCurrent, btCurrent = btCurrent, bhCurrent = bhCurrent, otCurrent = otCurrent, ohCurrent = ohCurrent, ohHigh = ohHigh, ohLow = ohLow, bhHigh = bhHigh, bhLow = bhLow, htHigh = htHigh, htLow = htLow, btHigh = btHigh, btLow = btLow, otHigh = otHigh, otLow = otLow, nagiosStatus=nagiosStatus, trend=trend, ctHigh = ctHigh, ctLow = ctLow)

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80, debug=True)

