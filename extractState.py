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
# pagerank of each nip

npi_set = set();

if len(sys.argv) != 4:
	print "Usage:"
	print str(sys.argv[0]) + " input_file output_file two_letter_state_abbreviation"
else:

	ifile = open(str(sys.argv[1]),'r');
	ofile = open(str(sys.argv[2]),'w');

	header = ifile.readline();
	ofile.write(header);
	for lines in ifile:
		entry = strip_quotes(lines.split("\t"));
		if entry_filter(entry) == True:
			if entry[nppes_provider_state] == str(sys.argv[3]):
				npi_set.add(entry[npi]);
				ofile.write(lines);


	print len(npi_set);
	ifile.close();
	ofile.close();

	

