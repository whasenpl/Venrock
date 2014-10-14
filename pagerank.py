#!/usr/local/bin/python
import sys;
import string;
import collections;
import math;
import fpformat;
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
	print "Usage:"
	print str(sys.argv[0]) + " procedure_file referral_file output_file"
else:

	ifile1 = open(str(sys.argv[1]),'r');
	ifile2 = open(str(sys.argv[2]),'r');
	ofile = open(str(sys.argv[3]),'w');

	print 'Gathering statistics on doctors';
	header = ifile1.readline();
	for lines in ifile1:
		entry = strip_quotes(lines.split("\t"));
		if entry_filter(entry) == True:
			gender[entry[npi]] = entry[nppes_provider_gender];
			entity[entry[npi]] = entry[nppes_entity_code];
			npi_set_tmp.add(entry[npi]);
			service_count[entry[npi]] += float(entry[line_srvc_cnt]);
			unique_count[entry[npi]] += float(entry[bene_unique_cnt]);
	print str(len(npi_set_tmp)) + ' total doctors';

	print 'Initializing graph';
	npi_set = frozenset(npi_set_tmp);
	page_rank = dict();
	initial_page_rank = 1/float(len(npi_set));
	in_edges = dict();
	for s in npi_set:
		in_edges[s] = set();
		page_rank[s] = initial_page_rank;

	in_degree = collections.defaultdict(int);
	out_degree = collections.defaultdict(int);
	in_entropy = collections.defaultdict(int);
	out_entropy = collections.defaultdict(int);
	in_referrals = collections.defaultdict(int);
	out_referrals = collections.defaultdict(int);
	in_male_referrals = collections.defaultdict(int);
	out_male_referrals = collections.defaultdict(int);
	in_organization_referrals = collections.defaultdict(int);
	out_organization_referrals = collections.defaultdict(int);

	num_lines = 0;					
	num_edges = 0;	
	for lines in ifile2:
		num_lines += 1;
		entry = lines.split(",");
		s = entry[0];
		t = entry[1];
		w = float(entry[2]);
		if (s in npi_set) and (t in npi_set):
			num_edges += 1;
			in_edges[t].add((s,w));
			in_entropy[t] -= w*math.log(w,2);
			out_entropy[s] -= w*math.log(w,2);
			in_referrals[t] += w;
			out_referrals[s] += w;
			in_degree[t] += 1;
			out_degree[s] += 1;
			if entity[s] == 'O':
				in_organization_referrals[t] += w;
			elif gender[s] == 'M':
				in_male_referrals[t] += w;

			if entity[t] == 'O':
				out_organization_referrals[s] += w;
			elif gender[t] == 'M':
				out_male_referrals[s] += w;

	print 'number of doctors (vertices): ' + str(len(npi_set));
	print 'number of referral relationships (edges): ' + str(num_edges);
	d = .85;
	even_weight = dict();
	for s in npi_set:
		if out_referrals[s] > 0:
			even_weight[s] = d/out_referrals[s];
			out_entropy[s] += out_referrals[s]*math.log(out_referrals[s],2);
			out_entropy[s] /= out_referrals[s];
			out_male_referrals[s] /= (out_referrals[s]-out_organization_referrals[s]);
		else:
			even_weight[s] = 0;
			out_entropy[s] = 0;
		if in_referrals[s] > 0:
			in_entropy[s] += in_referrals[s]*math.log(in_referrals[s],2);
			in_entropy[s] /= in_referrals[s];
			in_male_referrals[s] /= (in_referrals[s]-in_organization_referrals[s]);
		else:
			in_entropy[s] = 0;

	mix = .95;
	one_minus_d_over_N = (1-d)/float(len(npi_set));
	num_iterations = 16;
	for i in range(num_iterations):
		epsilon = 0;
		for t in npi_set:
			old_page_rank = page_rank[t];
			new_page_rank = one_minus_d_over_N;
			for (s,w) in in_edges[t]:
				new_page_rank += page_rank[s]*even_weight[s]*w;
			page_rank[t] = mix*new_page_rank + (1-mix)*old_page_rank;
			epsilon = max(epsilon,abs(page_rank[t] - old_page_rank)/old_page_rank);
		print 'max relative pagerank difference: ' + str(100*epsilon) + '%';

	page_rank_total = 0;
	for s in npi_set:
		page_rank_total += page_rank[s];
	page_rank_scaling = float(len(npi_set))/page_rank_total;

	print 'Writing stats file';
	header = 'npi,in_degree,out_degree,in_entropy,out_entropy,in_referrals,out_referrals,';
	header += 'in_organization_referrals,out_organization_referrals,';
	header += 'in_male_referrals,out_male_referrals,page_rank\n';
	ofile.write(header);
	for s in npi_set:
		line = s + ',';
		line += str(in_degree[s]) + ',' + str(out_degree[s]) + ',';
		line += str(in_entropy[s]) + ',' + str(out_entropy[s]) + ',';
		line += str(in_referrals[s]) + ',' + str(out_referrals[s]) + ',';
		line += str(in_organization_referrals[s]) + ',' + str(out_organization_referrals[s]) + ',';
		line += str(in_male_referrals[s]) + ',' + str(out_male_referrals[s]) + ',';
		line += str(page_rank_scaling*page_rank[s]) + '\n';
		ofile.write(line);

	ifile1.close();
	ifile2.close();
	ofile.close();
	# write ofile

