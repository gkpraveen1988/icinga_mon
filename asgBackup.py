#!/bin/bash/python
import sys,asgFunction
MYDICT =  {}

# Function for passing the correct option and get the option values
def getArgs():
    parser = asgFunction.argparse.ArgumentParser(
        description='Script for taking the required data and pushing the influxdb')
    parser.add_argument(
        '-s', '--server', type=str, help='End server')
    parser.add_argument(
        '-f', '--files', type=int, help='Number of files')
    parser.add_argument(
        '-b', '--nmbytes', type=int, help='Number of bytes')
    parser.add_argument(
        '-d', '--duration', type=int, help='Duration')

    args = parser.parse_args()
    return args

# Checking whether the lenght of argv
if len(sys.argv) > 1:
    cmdLineArgs = getArgs()
    MYDICT['server'] = cmdLineArgs.server
    MYDICT['files'] = cmdLineArgs.files
    MYDICT['nmbytes'] = cmdLineArgs.nmbytes
    MYDICT['duration'] = cmdLineArgs.duration
    MYDICT['startTime'] = asgFunction.now.strftime("%Y-%m-%dT%H:00:00Z")
    asgFunction.pointsList.append( asgFunction.createPoint( MYDICT ) )
    asgFunction.client.write_points( asgFunction.pointsList )
else:
    asgFunction.sqlWriteInfluxDb()

