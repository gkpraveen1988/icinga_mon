#!/usr/bin/python
import os,sys, argparse, datetime, sqlite3                   # Importing the required modules
from influxdb import InfluxDBClient     # Importing the influxdb client module
DB_NAME = 'ServerStats'                   # Database name
#DB_SERVER = 'serverstats'                 # Server Name
#SQLITE_DB = '/asg_backup/backup.db'       # SQLITE3 DB
DB_MEASUREMENT = 'asg_backup'		   # MEASUREMENT
DB_SERVER = 'localhost'                 # Server Name
SQLITE_DB = 'arista.db'                 # SQLITE3 DB
client = InfluxDBClient( DB_SERVER, 8086, '', '', DB_NAME ) # Influx DB connection
MYDICT =  {}
now = datetime.datetime.now()
pointsList = []

# CREATING THE JSON AND PUSHING THE DATA POINTS
def createPoint( MYDICT ):
   jsonCreate = {
                "measurement": DB_MEASUREMENT,
                "tags": {
                    "server": MYDICT['server']
                },
                "time": MYDICT['startTime'],
                "fields": {
                    "files": MYDICT['files'],
                    "bytes": MYDICT['nmbytes'],
                    "duration": MYDICT['duration']
                }
        }
   return jsonCreate

# FUNCTION TO CALCULATE THE DURATION
def calTimeDifference( starttime, endtime ):
   start_dt = datetime.datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%SZ') 
   end_dt = datetime.datetime.strptime(endtime, '%Y-%m-%dT%H:%M:%SZ')
   diff = (end_dt - start_dt)
   return (diff.days * 24 * 60 * 60) + (diff.seconds / 60)

# Function to add the data to sqlite3
def addPointsSqlite(server, files, size, startTime, endTime, uploaded):
   if os.path.isfile( SQLITE_DB ):                       # Checking for the SQLITE DB
      conn = sqlite3.connect( SQLITE_DB )
      cursor = conn.cursor()
      cursor.execute('''INSERT INTO drive_info(server,files,bytes,starttime,endtime,uploaded)
                  VALUES(?,?,?,?,?,?)''', (server, files, size, startTime, endTime,uploaded))
      conn.commit()
      conn.close()
   else:
      print "Error: Database %s not exists" % SQLITE_DB
      sys.exit( 1 )

# Function to push the data to Influx for UPLOADED record in SQLITE3 is 0
def addPointsSqlToInfluxdb():
   global pointsList
   if os.path.isfile( SQLITE_DB ):			# Checking for the SQLITE DB
      conn = sqlite3.connect( SQLITE_DB )
      cursor = conn.execute("select * from drive_info where NOT uploaded;") # Fetch Sqlite data to cursor
      for row in cursor:
         MYDICT['server'] = row[1]
         MYDICT['files'] = row[2]
         MYDICT['nmbytes'] = row[3]
         MYDICT['duration'] = calTimeDifference( row[4], row[5] )
         MYDICT['startTime'] = (datetime.datetime.strptime(row[4], '%Y-%m-%dT%H:%M:%SZ')).strftime("%Y-%m-%dT%H:00:00Z")
         jsonCreate = createPoint(MYDICT) 
         pointsList.append(jsonCreate) # Creating list of dictionary and passing the whole list to ind
         conn.execute("update drive_info set uploaded=1 where uploaded=0;")
         conn.commit()
      client.write_points( pointsList )
      conn.close()
   else:
      print "Error: Database %s not exists" % SQLITE_DB
      sys.exit( 1 )

