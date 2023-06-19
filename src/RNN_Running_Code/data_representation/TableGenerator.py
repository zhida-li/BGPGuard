
import os
import csv
import re


files = [];

for (dirpath, dirnames, filenames) in os.walk("./res_acc"):

    files.extend(filenames)
    break

parent_dirname = os.path.basename(os.path.abspath('.'));





header_list = [
	"lstm_2layer",
	"lstm_3layer",
	"lstm_4layer",

	"gru_2layer",
	"gru_3layer",
	"gru_4layer"
];






curr_files = [];




batch5_t = -1;
batch10_t = -1;
batch20_t = -1;

batch5_f = -1;
batch10_f = -1;
batch20_f = -1;



complete = 0;

with open(parent_dirname + "_table.csv", "w") as csvfile: #python 2.7 wb python3.6 w
	

	#spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL);
	spamwriter = csv.writer(csvfile, delimiter=',');

	for header in header_list:
		spamwriter.writerow( [header] + ["batch5_test"] + ["batch5_f-score"] + ["batch10_test"] + ["batch10_f-score"] + ["batch20_test"] + ["batch20_f-score"]);

		for f in files:


			if (header in f):
				

				if "batch5" in f:
					xx = open("./res_acc/" + f, "r");
					ss = xx.readline();
					ss = re.findall('\d+\.\d+', ss);
					batch5_t = ss[0];
					batch5_f = ss[1];

			
				elif "batch10" in f:
					xx = open("./res_acc/" + f, "r");
					ss = xx.readline();
					ss = re.findall('\d+\.\d+', ss);
					batch10_t = ss[0];
					batch10_f = ss[1];

				elif "batch20" in f:
					xx = open("./res_acc/" + f, "r");
					ss = xx.readline();
					ss = re.findall('\d+\.\d+', ss);
					batch20_t = ss[0];
					batch20_f = ss[1];

				if (batch5_t != -1) and (batch10_t != -1) and (batch20_t != -1):
					spamwriter.writerow( [""] + \
					 [batch5_t] + [batch5_f] + [batch10_t] \
					 + [batch10_f] + [batch20_t] + [batch20_f]);

					batch5_t = -1;
					batch10_t = -1;
					batch20_t = -1;

					batch5_f = -1;
					batch10_f = -1;
					batch20_f = -1;

					complete = 1;

					break;


		if complete != 1:
			print("miss entry")
			print(f);

		complete = 0;







