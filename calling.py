import asgFunction

#asgFunction.addBackupPoint(server='mysqli2', files=200, size=100, startTime='2016-10-10T12:17:01Z', endTime='2016-10-20T12:56:27Z')
asgFunction.sqlWriteInfluxDb(server='sqlite3385', files=200, size=100, startTime='2016-10-21T09:10:00Z', endTime='2016-10-20T12:56:27Z',uploaded=0)
#asgFunction.dataWriteSqlite(server='mysqlite156', files=200, size=100, startTime='2016-10-21T08:10:00Z', endTime='2016-10-20T12:56:27Z',uploaded=0)

