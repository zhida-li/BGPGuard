
import os
import csv
import re


files = [];

for (dirpath, dirnames, filenames) in os.walk("./res_run"):

    files.extend(filenames)
    break

parent_dirname = os.path.basename(os.path.abspath('.'));


sum_time=0.0;


for f in files:

	xx = open("./res_run/" + f, "r");
	ss = xx.readline();
	ss = re.findall('\d+\.\d+', ss);
	sum_time = sum_time + float(ss[0]);
	
print(sum_time/3600.0) ;

