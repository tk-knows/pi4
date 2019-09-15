from flask import Flask, request, render_template
import time
import datetime
import sys
import Adafruit_DHT
import sqlite3

app = Flask(__name__)
app.debug = True


@app.route("/")
def hello():
    return render_template('hello.html', message='freom Template rednder Flask' )

@app.route("/example")
def example():
    return "this is an example"

@app.route("/lab_temp")
def lab_temp():
    # humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
    humidity, temperature = Adafruit_DHT.read_retry(11, 17)
    temperature = temperature * (9/5) + 32 
    if humidity is not None and temperature is not None:
        return render_template('lab_temp.html',hum=humidity, temp=temperature)
    else:
        return render_template("no_sensor.html")

@app.route("/lab_env_db", methods=['GET'] )
def lab_env_db():
    temperatures, humidities, from_date_str, to_date_str = get_records()
    return render_template("lab_env_db.html",temp=temperatures,hum=humidities, temp_items=len(temperatures), hum_items=len(humidities))

def get_records():
    from_date_str = request.args.get('from', time.strftime('%Y-%m-%d 00:00')) # if from not given, get cur date
    to_date_str   = request.args.get('to',   time.strftime('%Y-%m-%d %H:%M')) # if to not given, get cur date, cur hour, cur min

    range_h_form    = request.args.get('range_h','');  #This will return a string, if field range_h exists in the request
    range_h_int     = "nan"  #initialise this variable with not a number
    try: 
        range_h_int = int(range_h_form)
    except:
        print ("range_h_form not a number")
        
    if not validate_date(from_date_str):            # Validate date before sending it to the DB
        from_date_str   = time.strftime("%Y-%m-%d 00:00")
    if not validate_date(to_date_str):
        to_date_str     = time.strftime("%Y-%m-%d %H:%M")

    if isinstance(range_h_int,int): 
        time_now        = datetime.datetime.now()
        time_from       = time_now - datetime.timedelta(hours = range_h_int)
        time_to         = time_now
        from_date_str   = time_from.strftime("%Y-%m-%d %H:%M")
        to_date_str     = time_to.strftime("%Y-%m-%d %H:%M")        

    print('from = {}, to = {}'.format(from_date_str, to_date_str))

    print('after validate_date called. from = {}, to = {}'.format(from_date_str, to_date_str))

    sql_where_str = ' where rDatetime between \"{}\" and \"{}\"'.format(from_date_str, to_date_str) 

    conn=sqlite3.connect('/var/www/lab_app/lab_app.db')
    curs=conn.cursor()

    if sql_where_str is not None:
        sql_temp_str = 'SELECT * FROM temperatures {}'.format(sql_where_str)
    else:
        sql_temp_str =  'SELECT * FROM temperatures'

    print("sql_temp_str {}".format(sql_temp_str))
    curs.execute(sql_temp_str)
    temperatures = curs.fetchall()

    if sql_where_str is not None:
        sql_hum_str = 'SELECT * FROM humidities {}'.format(sql_where_str)
    else:
        sql_hum_str =  'SELECT * FROM humidities'

    print("sql_hum_str {}".format(sql_hum_str))    
    curs.execute(sql_hum_str)
    humidities = curs.fetchall()

    conn.close()

    return [temperatures, humidities, from_date_str, to_date_str]

def validate_date(d):
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False

if __name__ =="__main__":
    app.run(host="0.0.0.0", port=8080)
