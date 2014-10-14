#!/usr/local/bin/python
import sys;
import string;
import collections;
import math;
from common import entry_filter, strip_quotes;

npi = 0;
nppes_provider_last_org_name = 1;
nppes_provider_first_name = 2;
nppes_provider_mi = 3;
nppes_credentials = 4;
nppes_provider_gender = 5;
nppes_entity_code = 6;
nppes_provider_street1 = 7;
nppes_provider_street2 = 8;
nppes_provider_city = 9;
nppes_provider_zip = 10;
nppes_provider_state = 11;
nppes_provider_country = 12;
provider_type = 13;
medicare_participation_indicator = 14;
place_of_service = 15;
hcpcs_code = 16;
line_srvc_cnt = 17;
bene_unique_cnt = 18;
bene_day_srvc_cnt = 19;
average_Medicare_allowed_amt = 20;
stdev_Medicare_allowed_amt = 21;
average_submitted_chrg_amt = 22;
stdev_submitted_chrg_amt = 23;
average_Medicare_payment_amt = 24;
stdev_Medicare_payment_amt = 25;

# Notes: 
# filter:
# only valid zip codes
# only country == US
# nip common to 2012 and 2011

# calculated fields:
# mean / std for I and O entities for each cost type
# count of referrers and referrees
# count of total incoming and outgoing referrals
# entropy of referrers and referrees weighted by refer count
# fraction male incoming and outgoing weighted by refer count
# fraction individual (vs. organization) by refer count
# pagerank of each npi


gender = collections.defaultdict(int);
entity = collections.defaultdict(int);
service_count = collections.defaultdict(int);
unique_count = collections.defaultdict(int);
npi_set_tmp = set();

if len(sys.argv) != 4:
	print "Extracts the subgraph of the referral graph with the subset of doctors in the procedure file."
	print "Usage:"
	print str(sys.argv[0]) + " procedure_file referral_file output_file"
else:

	ifile1 = open(str(sys.argv[1]),'r');
	ifile2 = open(str(sys.argv[2]),'r');
	ofile = open(str(sys.argv[3]),'w');

	print 'Finding NPI (Doctor ID) set';
	header = ifile1.readline();
	for lines in ifile1:
		entry = strip_quotes(lines.split("\t"));
		if entry_filter(entry) == True:
			npi_set_tmp.add(entry[npi]);
	print str(len(npi_set_tmp)) + ' total doctors';

	print 'Keeping only referrals within NPI set'
	npi_set = frozenset(npi_set_tmp);
	num_lines = 0;					
	num_edges = 0;	
	for lines in ifile2:
		num_lines += 1;
		entry = lines.split(",");
		if len(entry) == 3:
			s = entry[0];
			t = entry[1];
			w = float(entry[2]);
			if (s in npi_set) and (t in npi_set):
				num_edges += 1;
				ofile.write(lines);
		elif len(lines) > 3:
			print "Error on line number: " + str(num_lines);
			print lines;

	print "number of doctors (vertices) = " + str(len(npi_set));
	print "number of referral relationships (edges) = " + str(num_edges);
	ifile1.close();
	ifile2.close();
	ofile.close();
	# write ofile

