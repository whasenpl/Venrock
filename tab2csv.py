#!/usr/local/bin/python
import sys;
import string;

if len(sys.argv) == 1:
	print "Usage:"
	print str(sys.argv[0]) + " input_file output_file"
else:

	ifile = open(str(sys.argv[1]),'r');
	ofile = open(str(sys.argv[2]),'w');

	for lines in ifile:
		line = lines.replace("\t",",").replace("\"","");
		ofile.write(line);

