# Purpose #
those scripts extract SMA 4000TL solar production data and upload them into www.pvoutput.org at end of the day in batch mode.

here is my daily output at pvoutput.org

http://www.pvoutput.org/list.jsp?userid=1865

Developed in Python.


### Usage 1 ###
extract current SMA data after inverter stop working and upload data into pvoutput.org

D:\sma\smaeoduploader>python sma\_eod\_loader.py -e -r

parameters:

-e -- extract, by default no extract, upload only

-r -- upload in reverse order, be default in time order


![http://img.acianetmedia.com/i/smaeodaia.png](http://img.acianetmedia.com/i/smaeodaia.png)

### Usage 2 ###
extract past date SMA data and upload into pvoutput.org

parameters:

-d -- date, need specify which date want to extract and/or upload

-e -- extract, by default no extract, upload only

-r -- upload in reverse order, be default in time order

![http://img.acianetmedia.com/i/smaeodltl.png](http://img.acianetmedia.com/i/smaeodltl.png)

### Usage 3, release 1, default ###
upload in batch

![http://img.acianetmedia.com/i/smaeodzgz.png](http://img.acianetmedia.com/i/smaeodzgz.png)

