from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import *
from functools import wraps

from credentials import *
from password import *
import datetime
import json
import requests
from numpy import *
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


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == ADMIN_USER and password == ADMIN_PASSWORD

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

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

def getAllRecordsFiltered(hrs):
	time = datetime.datetime.now() - datetime.timedelta(hours=hrs)
	bt = BedroomTemperature.query.filter(BedroomTemperature.date>=time).all()
        bh = BedroomHumidity.query.filter(BedroomHumidity.date>=time).all()
        ot = OutsideTemperature.query.filter(OutsideTemperature.date>=time).all()
        oh = OutsideHumidity.query.filter(OutsideHumidity.date>=time).all()
        ct = ClosetTemperature.query.filter(ClosetTemperature.date>=time).all()
        ht = HouseTemperature.query.filter(HouseTemperature.date>=time).all()
        p = Pressure.query.filter(Pressure.date>=time).all()

        return bt, bh, ot, oh, ct, ht, p

def getAllRecords():
	bt = BedroomTemperature.query.all()
	bh = BedroomHumidity.query.all()
	ot = OutsideTemperature.query.all()
	oh = OutsideHumidity.query.all()
	ct = ClosetTemperature.query.all()
	ht = HouseTemperature.query.all()
	p = Pressure.query.all()

	return bt, bh, ot, oh, ct, ht, p

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

def stripOutliers(queryItem, itemType, magnitude):
	stdevh = 0
	counter = 0
	if itemType == "temp":
		ean, length = getTemperatureMean(queryItem)
		stdevh = std(list(item.temp for item in queryItem))
	        effectivestdev = stdevh * magnitude
		for item in queryItem:
			if item.temp > mean + effectivestdev or item.temp < mean - effectivestdev:
				pass
			else:
				db.session.delete(item)
				counter += 1
		db.session.commit()
		return counter
	elif itemType == "humidity":
		ean, length = getHumidityMean(queryItem)
		stdevh = std(list(item.humidity for item in queryItem))
	        effectivestdev = stdevh * magnitude
		for item in queryItem:
			if item.humidity > mean + effectivestdev or item.humidity < mean - effectivestdev:
				pass
			else:
				db.session.delete(item)
				counter += 1
		db.session.commit()
		return counter
	elif itemType == "pressure":
		ean, length = getPressureMean(queryItem)
		stdevh = std(list(item.pressure for item in queryItem))
	        effectivestdev = stdevh * magnitude
		for item in queryItem:
                        if item.pressure != 0:
                                pass
                        else:
                                db.session.delete(item)
				counter += 1
		db.session.commit()
		return counter

def getHumidityMean(queryItem):
	itemLength = len(queryItem)
	total = 0
	for item in queryItem:
		total = total + item.humidity
	mean = total / itemLength
	return mean, itemLength	

def getTemperatureMean(queryItem):
	itemLength = len(queryItem)
        total = 0
        for item in queryItem:
                total = total + int(item.temp)
        mean = total / itemLength
        return mean, itemLength

def getPressureMean(queryItem):
	itemLength = len(queryItem)
        total = 0
        for item in queryItem:
                total = total + item.pressure
        mean = total / itemLength
        return mean, itemLength

def getNagiosJSON():
	requestString = "https://andromeda.pettitservers.com:8080/state/"
	r = requests.get(requestString)
	json = r.json()
	nagiosStatus = {}
	for host in json['hosts']:
		nagiosStatus[json['hosts'][host]['host_name']] = json['hosts'][host]['current_state']
	return nagiosStatus

@app.route('/graphs')
@requires_auth
def graphs():
	bt6hr, bh6hr, ot6hr, oh6hr, ct6hr, ht6hr, p6hr = getAllRecordsFiltered(6)
	bt24hr, bh24hr, ot24hr, oh24hr, ct24hr, ht24hr, p24hr = getAllRecordsFiltered(24)
	bt7day, bh7day, ot7day, oh7day, ct7day, ht7day, p7day = getAllRecordsFiltered(168)
	
	return render_template("graphs.html", pressure6hr = p6hr, pressure24hr = p24hr, pressure7day = p7day, bt6hr = bt6hr, bt24hr = bt24hr, bt7day = bt7day)

@app.route('/dashboard')
@app.route('/')
@requires_auth
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
	pHigh, pLow = getHighLowPressure(24)	
	ctHigh, ctLow = getHighLowTemp("ct", 24)

	trend = getPressureTrend()	

	return render_template('index.html', htStat=htStat, ctStat=ctStat, btStat=btStat, bhStat=bhStat, otStat=otStat, ohStat=ohStat, htLast=htLast, ctLast=ctLast, btLast=btLast, bhLast=bhLast, otLast=otLast, ohLast=ohLast, pHigh = pHigh, pLow = pLow, pStat = pStat, pLast = pLast, pCurrent = pCurrent, htCurrent = htCurrent, ctCurrent = ctCurrent, btCurrent = btCurrent, bhCurrent = bhCurrent, otCurrent = otCurrent, ohCurrent = ohCurrent, ohHigh = ohHigh, ohLow = ohLow, bhHigh = bhHigh, bhLow = bhLow, htHigh = htHigh, htLow = htLow, btHigh = btHigh, btLow = btLow, otHigh = otHigh, otLow = otLow, nagiosStatus=nagiosStatus, trend=trend, ctHigh = ctHigh, ctLow = ctLow)

@app.route('/utils/outliers')
@requires_auth
def outliers():
	bt, bh, ot, oh, ct, ht, pa = getAllRecordsFiltered(24)
	bb, ba, bc, bd, be, bf, p = getAllRecords()

	ctPressure = stripOutliers(p, "pressure", 1)

	return "Deleted %i rows" % ctPressure
	
if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80, debug=True)

