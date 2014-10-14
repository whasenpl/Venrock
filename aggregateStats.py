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
hcpcs_code = 16;stdev_submitted_chrg_amt = 23;
average_Medicare_payment_amt = 24;
stdev_Medicare_payment_amt = 25;
line_srvc_cnt = 17;
bene_unique_cnt = 18;
bene_day_srvc_cnt = 19;
average_Medicare_allowed_amt = 20;
stdev_Medicare_allowed_amt = 21;
average_submitted_chrg_amt = 22;

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

gender = collections.defaultdict(int);
entity = collections.defaultdict(int);
mu_payment = collections.defaultdict(float);
mu_submitted = collections.defaultdict(float);
mu_allowed = collections.defaultdict(float);
sig_payment = collections.defaultdict(float);
sig_submitted = collections.defaultdict(float);
sig_allowed = collections.defaultdict(float);
service_count = collections.defaultdict(float);
unique_count = collections.defaultdict(float);
hcpcs_codes = set();

if len(sys.argv) != 3:
	print "Usage:"
	print str(sys.argv[0]) + " input_file output_file"
else:

	ifile = open(str(sys.argv[1]),'r');
	ofile = open(str(sys.argv[2]),'w');

	print 'gathering statistics';
	header = ifile.readline();
	for lines in ifile:
		entry = strip_quotes(lines.split("\t"));
		if entry_filter(entry) == True:
			gender[entry[npi]] = entry[nppes_provider_gender];
			entity[entry[npi]] = entry[nppes_entity_code];
			hcpcs_codes.add(entry[hcpcs_code]);
			mu_payment[entry[hcpcs_code]] += float(entry[average_Medicare_payment_amt])*float(entry[line_srvc_cnt]);
			mu_submitted[entry[hcpcs_code]] += float(entry[average_submitted_chrg_amt])*float(entry[line_srvc_cnt]);
			mu_allowed[entry[hcpcs_code]] += float(entry[average_Medicare_allowed_amt])*float(entry[line_srvc_cnt]);
			sig_payment[entry[hcpcs_code]] += pow(float(entry[stdev_Medicare_payment_amt]),2)*float(entry[line_srvc_cnt]);
			sig_submitted[entry[hcpcs_code]] += pow(float(entry[stdev_submitted_chrg_amt]),2)*float(entry[line_srvc_cnt]);
			sig_allowed[entry[hcpcs_code]] += pow(float(entry[stdev_Medicare_allowed_amt]),2)*float(entry[line_srvc_cnt]);
			service_count[entry[hcpcs_code]] += float(entry[line_srvc_cnt]);
			unique_count[entry[hcpcs_code]] += float(entry[bene_unique_cnt]);
	
	print 'writing per HCPCS code statistics'
	ofile.write('hcpcs_code,average_payment,average_submitted,average_allowed,stdev_payment,stdev_submitted,stdev_allowed,service_count,unique_count\n');
	for s in hcpcs_codes:
		mu_payment[s] = mu_payment[s]/service_count[s];
		mu_submitted[s] = mu_submitted[s]/service_count[s];
		mu_allowed[s] = mu_allowed[s]/service_count[s];
		sig_payment[s] = math.sqrt(sig_payment[s]/service_count[s]);
		sig_submitted[s] = math.sqrt(sig_submitted[s]/service_count[s]);
		sig_allowed[s] = math.sqrt(sig_allowed[s]/service_count[s]);
		line = s + ",";
		line += str(mu_payment[s]) + ",";
		line += str(mu_allowed[s]) + ",";
		line += str(mu_submitted[s]) + ",";
		line += str(sig_payment[s]) + ",";
		line += str(sig_allowed[s]) + ",";
		line += str(sig_submitted[s]) + ",";
		line += str(service_count[s]) + ",";
		line += str(unique_count[s]) + "\n";
		ofile.write(line);

	ifile.close();
	ofile.close();
	

