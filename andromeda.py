from flask import *
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import *

from credentials import *
from password import *
import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
connectionString = "mysql://%s:%s@%s:3306/%s" % (USERNAME, PASSWORD, HOSTNAME, DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = connectionString
db = SQLAlchemy(app)
app.secret_key = SECRET_KEY

class BedroomHumidity(db.Model):
	__tablename__ = "bedroom_humidity"

	id = db.Column(db.Integer, primary_key=True)
	humidity = db.Column(db.String(15))
	date = db.Column(db.String(30))

	def __init__(self, id, humidity, date):
		self.id = id
		self.humidity = humidity
		self.date = date

class OutsideHumidity(db.Model):
        __tablename__ = "outside_humidity"

        id = db.Column(db.Integer, primary_key=True)
        humidity = db.Column(db.Integer)
        date = db.Column(db.String(30))

        def __init__(self, id, humidity, date):
                self.id = id
                self.humidity = humidity
                self.date = date

class OutsideTemperature(db.Model):
        __tablename__ = "outside_temp"

        id = db.Column(db.Integer, primary_key=True)
        temp = db.Column(db.String(15))
        date = db.Column(db.String(30))

        def __init__(self, id, temp, date):
                self.id = id
                self.temp = temp
                self.date = date

class BedroomTemperature(db.Model):
        __tablename__ = "bedroom_temp"

        id = db.Column(db.Integer, primary_key=True)
        temp = db.Column(db.String(15))
        date = db.Column(db.String(30))

        def __init__(self, id, temp, date):
                self.id = id
                self.temp = temp
                self.date = date

class ClosetTemperature(db.Model):
        __tablename__ = "closet_temp"

        id = db.Column(db.Integer, primary_key=True)
        temp = db.Column(db.String(15))
        date = db.Column(db.String(30))

        def __init__(self, id, temp, date):
                self.id = id
                self.temp = temp
                self.date = date


class HouseTemperature(db.Model):
        __tablename__ = "house_temp"

        id = db.Column(db.Integer, primary_key=True)
        temp = db.Column(db.String(15))
        date = db.Column(db.String(30))

        def __init__(self, id, temp, date):
                self.id = id
                self.temp = temp
                self.date = date

class Pressure(db.Model):
        __tablename__ = "pressure"

        id = db.Column(db.Integer, primary_key=True)
        pressure = db.Column(db.Integer)
        date = db.Column(db.String(30))

        def __init__(self, id, pressure, date):
                self.id = id
                self.pressure = pressure
                self.date = date

def getPressure():
	return Pressure.query.order_by(Pressure.id.asc()).first()

def getOutsideTemp():
	return OutsideTemperature.query.order_by(OutsideTemperature.id.asc()).first()

def getOutsideHumidity():
	return OutsideHumidity.query.order_by(OutsideHumidity.id.asc()).first()

def getBedroomHumidity():
	return BedroomHumidity.query.order_by(BedroomHumidity.id.asc()).first()

def getBedroomTemp():
	return BedroomTemperature.query.order_by(BedroomTemperature.id.asc()).first()

def getHouseTemp():
	return HouseTemperature.query.order_by(HouseTemperature.id.asc()).first()

def getClosetTemp():
	return ClosetTemperature.query.order_by(ClosetTemperature.id.asc()).first()

def isOkay(queryItem):
        lastDate = queryItem.date
	lastDateObj = datetime.datetime.strptime(lastDate, '%Y-%m-%d %X.%f')
	warnTime = lastDateObj + datetime.timedelta(minutes=5)
	if warnTime < datetime.datetime.now():
		return False, lastDate
	else:
		return True, lastDate

def highLowHInt(queryItem):
	high = 0
	low = 0
        if queryItem.humidity > high:
                high = queryItem.humidity
        if queryItem.humidity < low:
                low = queryItem.humidity
	return high, low

@app.route('/')
def index():
	ht = getHouseTemp()
	ct = getClosetTemp()
	bt = getBedroomTemp()
	bh = getBedroomHumidity()
	ot = getOutsideTemp()
	oh = getOutsideHumidity()
	p = getPressure()

	htStat, htLast = isOkay(ht)
	ctStat, ctLast = isOkay(ct)
	btStat, btLast = isOkay(bt)
	bhStat, bhLast = isOkay(bh)
	otStat, otLast = isOkay(ot)
	ohStat, ohLast = isOkay(oh)
	pStat, pLast = isOkay(p)

	ohHigh, ohLow = highLowHInt(oh)

	return render_template('index.html', htStat=htStat, ctStat=ctStat, btStat=btStat, bhStat=bhStat, otStat=otStat, ohStat=ohStat, pStat=pStat, htLast=htLast, ctLast=ctLast, btLast=btLast, bhLast=bhLast, otLast=otLast, ohLast=ohLast,pLast=pLast, ohHigh = ohHigh, ohLow = ohLow)

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80, debug=True)
