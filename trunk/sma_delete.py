import csv
import time
import datetime
import subprocess
import getopt
import sys

## global variables
from conf import *


def delete_data(data_file,key,id,r):
    """
     load  SMA data from data file and upload into www.pvoutput.org
    """
    count = 0
    index = 0
    sma_data = []
    reader = csv.reader(open(data_file,"r"),delimiter=";")

    ## load SMA data in single run
    for i in reader:
                count = count + 1
                ## a, ignore 1st 9 lines
                ##print i
                if count > 9 and float(i[2]) == 0:
                        sma_data.append( (i[0][6:10] + i[0][3:5] + i[0][0:2], i[0][11:16], float(i[1]),float(i[2]) ) )
                        index = index + 1
    ## reverse data
    if r:
        sma_data.reverse()

    ## upload SMA data to pvoutput.org
    for i in sma_data:
                ## filter only for 10 mins interval
                if i[1][3:5] in ('00','10','20','30','40','50'):
                        print i
                        try:
                                subprocess.check_call(["curl.exe",\
                                            "-d", "d=%s" % i[0], \
                                            "-d", "t=%s" % i[1], \
                                            "-H", "X-Pvoutput-Apikey:%s" % key,\
                                            "-H", "X-Pvoutput-SystemId:%d" % id,\
                                            "http://pvoutput.org/service/r1/deletestatus.jsp"])
                                ## sleep here, required by www.pvoutput.org
                                time.sleep(sleep_time)
                        except subprocess.CalledProcessError:
                                print "error: " 
                                print subprocess.STDOUT
                                break


def main():
    today = datetime.date.today().strftime("%Y%m%d")
    rev = False
    ext = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:r")
    except getopt.GetoptError, err:
        print str(err) 
        print "usage: prog -d yyyymmdd {default: today} -e {extract from plant, default: No} -r {reverse data during load, default: No}"
        sys.exit(2)

    for o, a in opts:
        if o == "-d":
            today = a
        elif o == "-r":
            rev = True

    ## data file name with full path
    data_file = data_path + "/" + sys_name + "-" + today + ".csv"
    print "delete data ...  " + data_file
    ##
    delete_data(data_file,key,id,rev)

if __name__ == "__main__":
    main()