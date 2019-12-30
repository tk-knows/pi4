
import sqlite3
import sys
import Adafruit_DHT

def truncate_tables():
	conn=sqlite3.connect('/var/www/lab_app/lab_app.db')  #It is important to provide an
							     #absolute path to the database
							     #file, otherwise Cron won't be
							     #able to find it!
	# For the time-related code (record timestamps and time-date calculations) to work 
	# correctly, it is important to ensure that your Raspberry Pi is set to UTC.
	# This is done by default!
	# In general, servers are assumed to be in UTC.
	curs=conn.cursor()
	curs.execute("""truncate table temperatures""") 
	curs.execute("""truncate table humidities values""")
	conn.commit()
	conn.close()


