
import sqlite3
import sys

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
	curs.execute("""DELETE FROM temperatures""") 
	curs.execute("""DELETE FROM humidities""")
	curs.execute("""VACUUM""")
	curs.execute(""" CREATE TABLE humidities (rDatetime datetime, sensorID text, hum numeric) """ )
        curs.execute(""" CREATE TABLE temperatures (rDatetime datetime, sensorID text, temp numeric) """)
	conn.commit()
	conn.close()

