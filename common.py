#!/usr/local/bin/python
import sys;
import string;
import collections;
import math;

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


def entry_filter(entry):
	if entry[nppes_provider_zip].isdigit() == True:
		if entry[nppes_provider_country] == 'US':
			if entry[nppes_entity_code] == 'I':
				return True;
	return False;

def strip_quotes(entry):
	i = 0;
	for i in range(len(entry)):
		if entry[i].find('"') >= 0:
			entry[i] = entry[i][entry[i].find('"')+1:entry[i].rfind('"')];
	return entry;

	# clean zip code: create a 5-digit zip code field

def abbreviate_street_type(line, full_name, abbreviation):
	line.replace(' ' + full_name + ' ',' ' + abbreviation + ' ');
	return line;

def standardize_street_address(line):
	line = ' ' + line.upper() + ' ';
	for c in string.punctuation:
		line = line.replace(c,"");

	line = abbreviate_street_type(line, 'NORTH', 'N');
	line = abbreviate_street_type(line, 'NORTHEAST', 'NE');
	line = abbreviate_street_type(line, 'NORTHWEST', 'NW');
	line = abbreviate_street_type(line, 'WEST', 'W');
	line = abbreviate_street_type(line, 'EAST', 'E');
	line = abbreviate_street_type(line, 'SOUTH', 'S');
	line = abbreviate_street_type(line, 'SOUTHEAST', 'SE');
	line = abbreviate_street_type(line, 'SOUTHWEST', 'SW');
	line = abbreviate_street_type(line, 'ALLEY', 'ALY');
	line = abbreviate_street_type(line, 'ANNEX', 'ANX');
	line = abbreviate_street_type(line, 'ARCADE', 'ARC');
	line = abbreviate_street_type(line, 'AVENUE', 'AVE');
	line = abbreviate_street_type(line, 'BAYOO', 'BYU');
	line = abbreviate_street_type(line, 'BEACH', 'BCH');
	line = abbreviate_street_type(line, 'BEND', 'BND');
	line = abbreviate_street_type(line, 'BLUFF', 'BLF');
	line = abbreviate_street_type(line, 'BLUFFS', 'BLFS');
	line = abbreviate_street_type(line, 'BOTTOM', 'BTM');
	line = abbreviate_street_type(line, 'BOULEVARD', 'BLVD');
	line = abbreviate_street_type(line, 'BRANCH', 'BR');
	line = abbreviate_street_type(line, 'BRIDGE', 'BRG');
	line = abbreviate_street_type(line, 'BROOK', 'BRK');
	line = abbreviate_street_type(line, 'BROOKS', 'BRKS');
	line = abbreviate_street_type(line, 'BURG', 'BG');
	line = abbreviate_street_type(line, 'BURGS', 'BGS');
	line = abbreviate_street_type(line, 'BYPASS', 'BYP');
	line = abbreviate_street_type(line, 'CAMP', 'CP');
	line = abbreviate_street_type(line, 'CANYON', 'CYN');
	line = abbreviate_street_type(line, 'CAPE', 'CPE');
	line = abbreviate_street_type(line, 'CAUSEWAY', 'CSWY');
	line = abbreviate_street_type(line, 'CENTER', 'CTR');
	line = abbreviate_street_type(line, 'CENTERS', 'CTRS');
	line = abbreviate_street_type(line, 'CIRCLE', 'CIR');
	line = abbreviate_street_type(line, 'CIRCLES', 'CIRS');
	line = abbreviate_street_type(line, 'CLIFF', 'CLF');
	line = abbreviate_street_type(line, 'CLIFFS', 'CLFS');
	line = abbreviate_street_type(line, 'CLUB', 'CLB');
	line = abbreviate_street_type(line, 'COMMON', 'CMN');
	line = abbreviate_street_type(line, 'CORNER', 'COR');
	line = abbreviate_street_type(line, 'CORNERS', 'CORS');
	line = abbreviate_street_type(line, 'COURSE', 'CRSE');
	line = abbreviate_street_type(line, 'COURT', 'CT');
	line = abbreviate_street_type(line, 'COURTS', 'CTS');
	line = abbreviate_street_type(line, 'COVE', 'CV');
	line = abbreviate_street_type(line, 'COVES', 'CVS');
	line = abbreviate_street_type(line, 'CREEK', 'CRK');
	line = abbreviate_street_type(line, 'CRESCENT', 'CRES');
	line = abbreviate_street_type(line, 'CREST', 'CRST');
	line = abbreviate_street_type(line, 'CROSSING', 'XING');
	line = abbreviate_street_type(line, 'CROSSROAD', 'XRD');
	line = abbreviate_street_type(line, 'CURVE', 'CURV');
	line = abbreviate_street_type(line, 'DALE', 'DL');
	line = abbreviate_street_type(line, 'DAM', 'DM');
	line = abbreviate_street_type(line, 'DIVIDE', 'DV');
	line = abbreviate_street_type(line, 'DRIVE', 'DR');
	line = abbreviate_street_type(line, 'DRIVES', 'DRS');
	line = abbreviate_street_type(line, 'ESTATE', 'EST');
	line = abbreviate_street_type(line, 'ESTATES', 'ESTS');
	line = abbreviate_street_type(line, 'EXPRESSWAY', 'EXPY');
	line = abbreviate_street_type(line, 'EXTENSION', 'EXT');
	line = abbreviate_street_type(line, 'EXTENSIONS', 'EXTS');
	line = abbreviate_street_type(line, 'FALLS', 'FLS');
	line = abbreviate_street_type(line, 'FERRY', 'FRY');
	line = abbreviate_street_type(line, 'FIELD', 'FLD');
	line = abbreviate_street_type(line, 'FIELDS', 'FLDS');
	line = abbreviate_street_type(line, 'FLAT', 'FLT');
	line = abbreviate_street_type(line, 'FLATS', 'FLTS');
	line = abbreviate_street_type(line, 'FORD', 'FRD');
	line = abbreviate_street_type(line, 'FORDS', 'FRDS');
	line = abbreviate_street_type(line, 'FOREST', 'FRST');
	line = abbreviate_street_type(line, 'FORGE', 'FRG');
	line = abbreviate_street_type(line, 'FORGES', 'FRGS');
	line = abbreviate_street_type(line, 'FORK', 'FRK');
	line = abbreviate_street_type(line, 'FORKS', 'FRKS');
	line = abbreviate_street_type(line, 'FORT', 'FT');
	line = abbreviate_street_type(line, 'FREEWAY', 'FWY');
	line = abbreviate_street_type(line, 'GARDEN', 'GDN');
	line = abbreviate_street_type(line, 'GARDENS', 'GDNS');
	line = abbreviate_street_type(line, 'GATEWAY', 'GTWY');
	line = abbreviate_street_type(line, 'GLEN', 'GLN');
	line = abbreviate_street_type(line, 'GLENS', 'GLNS');
	line = abbreviate_street_type(line, 'GREEN', 'GRN');
	line = abbreviate_street_type(line, 'GREENS', 'GRNS');
	line = abbreviate_street_type(line, 'GROVE', 'GRV');
	line = abbreviate_street_type(line, 'GROVES', 'GRVS');
	line = abbreviate_street_type(line, 'HARBOR', 'HBR');
	line = abbreviate_street_type(line, 'HARBORS', 'HBRS');
	line = abbreviate_street_type(line, 'HAVEN', 'HVN');
	line = abbreviate_street_type(line, 'HEIGHTS', 'HTS');
	line = abbreviate_street_type(line, 'HIGHWAY', 'HWY');
	line = abbreviate_street_type(line, 'HILL', 'HL');
	line = abbreviate_street_type(line, 'HILLS', 'HLS');
	line = abbreviate_street_type(line, 'HOLLOW', 'HOLW');
	line = abbreviate_street_type(line, 'INLET', 'INLT');
	line = abbreviate_street_type(line, 'ISLAND', 'IS');
	line = abbreviate_street_type(line, 'ISLANDS', 'ISS');
	line = abbreviate_street_type(line, 'ISLE', 'ISLE');
	line = abbreviate_street_type(line, 'JUNCTION', 'JCT');
	line = abbreviate_street_type(line, 'JUNCTIONS', 'JCTS');
	line = abbreviate_street_type(line, 'KEY', 'KY');
	line = abbreviate_street_type(line, 'KEYS', 'KYS');
	line = abbreviate_street_type(line, 'KNOLL', 'KNL');
	line = abbreviate_street_type(line, 'KNOLLS', 'KNLS');
	line = abbreviate_street_type(line, 'LAKE', 'LK');
	line = abbreviate_street_type(line, 'LAKES', 'LKS');
	line = abbreviate_street_type(line, 'LAND', 'LAND');
	line = abbreviate_street_type(line, 'LANDING', 'LNDG');
	line = abbreviate_street_type(line, 'LANE', 'LN');
	line = abbreviate_street_type(line, 'LIGHT', 'LGT');
	line = abbreviate_street_type(line, 'LIGHTS', 'LGTS');
	line = abbreviate_street_type(line, 'LOAF', 'LF');
	line = abbreviate_street_type(line, 'LOCK', 'LCK');
	line = abbreviate_street_type(line, 'LOCKS', 'LCKS');
	line = abbreviate_street_type(line, 'LODGE', 'LDG');
	line = abbreviate_street_type(line, 'LOOP', 'LOOP');
	line = abbreviate_street_type(line, 'MALL', 'MALL');
	line = abbreviate_street_type(line, 'MANOR', 'MNR');
	line = abbreviate_street_type(line, 'MANORS', 'MNRS');
	line = abbreviate_street_type(line, 'MEADOW', 'MDW');
	line = abbreviate_street_type(line, 'MEADOWS', 'MDWS');
	line = abbreviate_street_type(line, 'MEWS', 'MEWS');
	line = abbreviate_street_type(line, 'MILL', 'ML');
	line = abbreviate_street_type(line, 'MILLS', 'MLS');
	line = abbreviate_street_type(line, 'MISSION', 'MSN');
	line = abbreviate_street_type(line, 'MOTORWAY', 'MTWY');
	line = abbreviate_street_type(line, 'MOUNT', 'MT');
	line = abbreviate_street_type(line, 'MOUNTAIN', 'MTN');
	line = abbreviate_street_type(line, 'MOUNTAINS', 'MTNS');
	line = abbreviate_street_type(line, 'NECK', 'NCK');
	line = abbreviate_street_type(line, 'ORCHARD', 'ORCH');
	line = abbreviate_street_type(line, 'OVERPASS', 'OPAS');
	line = abbreviate_street_type(line, 'PARKS', 'PARK');
	line = abbreviate_street_type(line, 'PARKWAY', 'PKWY');
	line = abbreviate_street_type(line, 'PARKWAYS', 'PKWY');
	line = abbreviate_street_type(line, 'PASS', 'PASS');
	line = abbreviate_street_type(line, 'PASSAGE', 'PSGE');
	line = abbreviate_street_type(line, 'PINE', 'PNE');
	line = abbreviate_street_type(line, 'PINES', 'PNES');
	line = abbreviate_street_type(line, 'PLACE', 'PL');
	line = abbreviate_street_type(line, 'PLAIN', 'PLN');
	line = abbreviate_street_type(line, 'PLAINS', 'PLNS');
	line = abbreviate_street_type(line, 'PLAZA', 'PLZ');
	line = abbreviate_street_type(line, 'POINT', 'PT');
	line = abbreviate_street_type(line, 'POINTS', 'PTS');
	line = abbreviate_street_type(line, 'PORT', 'PRT');
	line = abbreviate_street_type(line, 'PORTS', 'PRTS');
	line = abbreviate_street_type(line, 'PRAIRIE', 'PR');
	line = abbreviate_street_type(line, 'RADIAL', 'RADL');
	line = abbreviate_street_type(line, 'RANCH', 'RNCH');
	line = abbreviate_street_type(line, 'RAPID', 'RPD');
	line = abbreviate_street_type(line, 'RAPIDS', 'RPDS');
	line = abbreviate_street_type(line, 'REST', 'RST');
	line = abbreviate_street_type(line, 'RIDGE', 'RDG');
	line = abbreviate_street_type(line, 'RIDGES', 'RDGS');
	line = abbreviate_street_type(line, 'RIVER', 'RIV');
	line = abbreviate_street_type(line, 'ROAD', 'RD');
	line = abbreviate_street_type(line, 'ROADS', 'RDS');
	line = abbreviate_street_type(line, 'ROUTE', 'RTE');
	line = abbreviate_street_type(line, 'SHOAL', 'SHL');
	line = abbreviate_street_type(line, 'SHOALS', 'SHLS');
	line = abbreviate_street_type(line, 'SHORE', 'SHR');
	line = abbreviate_street_type(line, 'SHORES', 'SHRS');
	line = abbreviate_street_type(line, 'SKYWAY', 'SKWY');
	line = abbreviate_street_type(line, 'SPRING', 'SPG');
	line = abbreviate_street_type(line, 'SPRINGS', 'SPGS');
	line = abbreviate_street_type(line, 'SPURS', 'SPUR');
	line = abbreviate_street_type(line, 'SQUARE', 'SQ');
	line = abbreviate_street_type(line, 'SQUARES', 'SQS');
	line = abbreviate_street_type(line, 'STATION', 'STA');
	line = abbreviate_street_type(line, 'STRAVENUE', 'STRA');
	line = abbreviate_street_type(line, 'STREAM', 'STRM');
	line = abbreviate_street_type(line, 'STREET', 'ST');
	line = abbreviate_street_type(line, 'STREETS', 'STS');
	line = abbreviate_street_type(line, 'SUMMIT', 'SMT');
	line = abbreviate_street_type(line, 'TERRACE', 'TER');
	line = abbreviate_street_type(line, 'THROUGHWAY', 'TRWY');
	line = abbreviate_street_type(line, 'TRACE', 'TRCE');
	line = abbreviate_street_type(line, 'TRACK', 'TRAK');
	line = abbreviate_street_type(line, 'TRAFFICWAY', 'TRFY');
	line = abbreviate_street_type(line, 'TRAIL', 'TRL');
	line = abbreviate_street_type(line, 'TUNNEL', 'TUNL');
	line = abbreviate_street_type(line, 'TURNPIKE', 'TPKE');
	line = abbreviate_street_type(line, 'UNDERPASS', 'UPAS');
	line = abbreviate_street_type(line, 'UNION', 'UN');
	line = abbreviate_street_type(line, 'UNIONS', 'UNS');
	line = abbreviate_street_type(line, 'VALLEY', 'VLY');
	line = abbreviate_street_type(line, 'VALLEYS', 'VLYS');
	line = abbreviate_street_type(line, 'VIADUCT', 'VIA');
	line = abbreviate_street_type(line, 'VIEW', 'VW');
	line = abbreviate_street_type(line, 'VIEWS', 'VWS');
	line = abbreviate_street_type(line, 'VILLAGE', 'VLG');
	line = abbreviate_street_type(line, 'VILLAGES', 'VLGS');
	line = abbreviate_street_type(line, 'VILLE', 'VL');
	line = abbreviate_street_type(line, 'VISTA', 'VIS');
	line = abbreviate_street_type(line, 'WALKS', 'WALK');
	line = abbreviate_street_type(line, 'WELL', 'WL');
	line = abbreviate_street_type(line, 'WELLS', 'WLS');
	line = abbreviate_street_type(line, 'ALLEE', 'ALY');
	line = abbreviate_street_type(line, 'ALLY', 'ALY');
	line = abbreviate_street_type(line, 'ANEX', 'ANX');
	line = abbreviate_street_type(line, 'AV', 'AVE');
	line = abbreviate_street_type(line, 'AVEN', 'AVE');
	line = abbreviate_street_type(line, 'AVENU', 'AVE');
	line = abbreviate_street_type(line, 'AVN', 'AVE');
	line = abbreviate_street_type(line, 'AVNUE', 'AVE');
	line = abbreviate_street_type(line, 'BAYOU', 'BYU');
	line = abbreviate_street_type(line, 'BLUF', 'BLF');
	line = abbreviate_street_type(line, 'BOT', 'BTM');
	line = abbreviate_street_type(line, 'BOTTM', 'BTM');
	line = abbreviate_street_type(line, 'BOUL', 'BLVD');
	line = abbreviate_street_type(line, 'BOULV', 'BLVD');
	line = abbreviate_street_type(line, 'BRNCH', 'BR');
	line = abbreviate_street_type(line, 'BRDGE', 'BRG');
	line = abbreviate_street_type(line, 'BYPA', 'BYP');
	line = abbreviate_street_type(line, 'BYPAS', 'BYP');
	line = abbreviate_street_type(line, 'BYPS', 'BYP');
	line = abbreviate_street_type(line, 'CMP', 'CP');
	line = abbreviate_street_type(line, 'CANYN', 'CYN');
	line = abbreviate_street_type(line, 'CNYN', 'CYN');
	line = abbreviate_street_type(line, 'CAUSWAY', 'CSWY');
	line = abbreviate_street_type(line, 'CEN', 'CTR');
	line = abbreviate_street_type(line, 'CENT', 'CTR');
	line = abbreviate_street_type(line, 'CENTR', 'CTR');
	line = abbreviate_street_type(line, 'CENTRE', 'CTR');
	line = abbreviate_street_type(line, 'CNTER', 'CTR');
	line = abbreviate_street_type(line, 'CNTR', 'CTR');
	line = abbreviate_street_type(line, 'CIRC', 'CIR');
	line = abbreviate_street_type(line, 'CIRCL', 'CIR');
	line = abbreviate_street_type(line, 'CRCL', 'CIR');
	line = abbreviate_street_type(line, 'CRCLE', 'CIR');
	line = abbreviate_street_type(line, 'CRT', 'CT');
	line = abbreviate_street_type(line, 'CT', 'CTS');
	line = abbreviate_street_type(line, 'CK', 'CRK');
	line = abbreviate_street_type(line, 'CR', 'CRK');
	line = abbreviate_street_type(line, 'CRECENT', 'CRES');
	line = abbreviate_street_type(line, 'CRESENT', 'CRES');
	line = abbreviate_street_type(line, 'CRSCNT', 'CRES');
	line = abbreviate_street_type(line, 'CRSENT', 'CRES');
	line = abbreviate_street_type(line, 'CRSNT', 'CRES');
	line = abbreviate_street_type(line, 'CRSSING', 'XING');
	line = abbreviate_street_type(line, 'CRSSNG', 'XING');
	line = abbreviate_street_type(line, 'DIV', 'DV');
	line = abbreviate_street_type(line, 'DVD', 'DV');
	line = abbreviate_street_type(line, 'DRIV', 'DR');
	line = abbreviate_street_type(line, 'DRV', 'DR');
	line = abbreviate_street_type(line, 'EXP', 'EXPY');
	line = abbreviate_street_type(line, 'EXPR', 'EXPY');
	line = abbreviate_street_type(line, 'EXPRESS', 'EXPY');
	line = abbreviate_street_type(line, 'EXPW', 'EXPY');
	line = abbreviate_street_type(line, 'EXTN', 'EXT');
	line = abbreviate_street_type(line, 'EXTNSN', 'EXT');
	line = abbreviate_street_type(line, 'FRRY', 'FRY');
	line = abbreviate_street_type(line, 'FORESTS', 'FRST');
	line = abbreviate_street_type(line, 'FORG', 'FRG');
	line = abbreviate_street_type(line, 'FRT', 'FT');
	line = abbreviate_street_type(line, 'FREEWY', 'FWY');
	line = abbreviate_street_type(line, 'FRWAY', 'FWY');
	line = abbreviate_street_type(line, 'FRWY', 'FWY');
	line = abbreviate_street_type(line, 'GARDN', 'GDN');
	line = abbreviate_street_type(line, 'GRDEN', 'GDN');
	line = abbreviate_street_type(line, 'GRDN', 'GDN');
	line = abbreviate_street_type(line, 'GRDNS', 'GDNS');
	line = abbreviate_street_type(line, 'GATEWY', 'GTWY');
	line = abbreviate_street_type(line, 'GATWAY', 'GTWY');
	line = abbreviate_street_type(line, 'GTWAY', 'GTWY');
	line = abbreviate_street_type(line, 'GROV', 'GRV');
	line = abbreviate_street_type(line, 'HARB', 'HBR');
	line = abbreviate_street_type(line, 'HARBR', 'HBR');
	line = abbreviate_street_type(line, 'HRBOR', 'HBR');
	line = abbreviate_street_type(line, 'HAVN', 'HVN');
	line = abbreviate_street_type(line, 'HEIGHT', 'HTS');
	line = abbreviate_street_type(line, 'HGTS', 'HTS');
	line = abbreviate_street_type(line, 'HT', 'HTS');
	line = abbreviate_street_type(line, 'HIGHWY', 'HWY');
	line = abbreviate_street_type(line, 'HIWAY', 'HWY');
	line = abbreviate_street_type(line, 'HIWY', 'HWY');
	line = abbreviate_street_type(line, 'HWAY', 'HWY');
	line = abbreviate_street_type(line, 'HLLW', 'HOLW');
	line = abbreviate_street_type(line, 'HOLLOWS', 'HOLW');
	line = abbreviate_street_type(line, 'HOLWS', 'HOLW');
	line = abbreviate_street_type(line, 'ISLND', 'IS');
	line = abbreviate_street_type(line, 'ISLNDS', 'ISS');
	line = abbreviate_street_type(line, 'ISLES', 'ISLE');
	line = abbreviate_street_type(line, 'JCTION', 'JCT');
	line = abbreviate_street_type(line, 'JCTN', 'JCT');
	line = abbreviate_street_type(line, 'JUNCTN', 'JCT');
	line = abbreviate_street_type(line, 'JUNCTON', 'JCT');
	line = abbreviate_street_type(line, 'JCTNS', 'JCTS');
	line = abbreviate_street_type(line, 'KNOL', 'KNL');
	line = abbreviate_street_type(line, 'LNDNG', 'LNDG');
	line = abbreviate_street_type(line, 'LA', 'LN');
	line = abbreviate_street_type(line, 'LANES', 'LN');
	line = abbreviate_street_type(line, 'LDGE', 'LDG');
	line = abbreviate_street_type(line, 'LODG', 'LDG');
	line = abbreviate_street_type(line, 'LOOPS', 'LOOP');
	line = abbreviate_street_type(line, 'MEDOWS', 'MDWS');
	line = abbreviate_street_type(line, 'MISSN', 'MSN');
	line = abbreviate_street_type(line, 'MSSN', 'MSN');
	line = abbreviate_street_type(line, 'MNT', 'MT');
	line = abbreviate_street_type(line, 'MNTAIN', 'MTN');
	line = abbreviate_street_type(line, 'MNTN', 'MTN');
	line = abbreviate_street_type(line, 'MOUNTIN', 'MTN');
	line = abbreviate_street_type(line, 'MTIN', 'MTN');
	line = abbreviate_street_type(line, 'MNTNS', 'MTNS');
	line = abbreviate_street_type(line, 'ORCHRD', 'ORCH');
	line = abbreviate_street_type(line, 'OVL', 'OVAL');
	line = abbreviate_street_type(line, 'PK', 'PARK');
	line = abbreviate_street_type(line, 'PRK', 'PARK');
	line = abbreviate_street_type(line, 'PARKWY', 'PKWY');
	line = abbreviate_street_type(line, 'PKWAY', 'PKWY');
	line = abbreviate_street_type(line, 'PKY', 'PKWY');
	line = abbreviate_street_type(line, 'PKWYS', 'PKWY');
	line = abbreviate_street_type(line, 'PATHS', 'PATH');
	line = abbreviate_street_type(line, 'PIKES', 'PIKE');
	line = abbreviate_street_type(line, 'PLAINES', 'PLNS');
	line = abbreviate_street_type(line, 'PLZA', 'PLZ');
	line = abbreviate_street_type(line, 'PRARIE', 'PR');
	line = abbreviate_street_type(line, 'PRR', 'PR');
	line = abbreviate_street_type(line, 'RAD', 'RADL');
	line = abbreviate_street_type(line, 'RADIEL', 'RADL');
	line = abbreviate_street_type(line, 'RANCHES', 'RNCH');
	line = abbreviate_street_type(line, 'RNCHS', 'RNCH');
	line = abbreviate_street_type(line, 'RDGE', 'RDG');
	line = abbreviate_street_type(line, 'RIVR', 'RIV');
	line = abbreviate_street_type(line, 'RVR', 'RIV');
	line = abbreviate_street_type(line, 'SHOAR', 'SHR');
	line = abbreviate_street_type(line, 'SHOARS', 'SHRS');
	line = abbreviate_street_type(line, 'SPNG', 'SPG');
	line = abbreviate_street_type(line, 'SPRNG', 'SPG');
	line = abbreviate_street_type(line, 'SPNGS', 'SPGS');
	line = abbreviate_street_type(line, 'SPRNGS', 'SPGS');
	line = abbreviate_street_type(line, 'SQR', 'SQ');
	line = abbreviate_street_type(line, 'SQRE', 'SQ');
	line = abbreviate_street_type(line, 'SQU', 'SQ');
	line = abbreviate_street_type(line, 'SQRS', 'SQS');
	line = abbreviate_street_type(line, 'STATN', 'STA');
	line = abbreviate_street_type(line, 'STN', 'STA');
	line = abbreviate_street_type(line, 'STRAV', 'STRA');
	line = abbreviate_street_type(line, 'STRAVE', 'STRA');
	line = abbreviate_street_type(line, 'STRAVEN', 'STRA');
	line = abbreviate_street_type(line, 'STRAVN', 'STRA');
	line = abbreviate_street_type(line, 'STRVN', 'STRA');
	line = abbreviate_street_type(line, 'STRVNUE', 'STRA');
	line = abbreviate_street_type(line, 'STREME', 'STRM');
	line = abbreviate_street_type(line, 'STR', 'ST');
	line = abbreviate_street_type(line, 'STRT', 'ST');
	line = abbreviate_street_type(line, 'SUMIT', 'SMT');
	line = abbreviate_street_type(line, 'SUMITT', 'SMT');
	line = abbreviate_street_type(line, 'TERR', 'TER');
	line = abbreviate_street_type(line, 'TRACES', 'TRCE');
	line = abbreviate_street_type(line, 'TRACKS', 'TRAK');
	line = abbreviate_street_type(line, 'TRK', 'TRAK');
	line = abbreviate_street_type(line, 'TRKS', 'TRAK');
	line = abbreviate_street_type(line, 'TR', 'TRL');
	line = abbreviate_street_type(line, 'TRAILS', 'TRL');
	line = abbreviate_street_type(line, 'TRLS', 'TRL');
	line = abbreviate_street_type(line, 'TUNEL', 'TUNL');
	line = abbreviate_street_type(line, 'TUNLS', 'TUNL');
	line = abbreviate_street_type(line, 'TUNNELS', 'TUNL');
	line = abbreviate_street_type(line, 'TUNNL', 'TUNL');
	line = abbreviate_street_type(line, 'TPK', 'TPKE');
	line = abbreviate_street_type(line, 'TRNPK', 'TPKE');
	line = abbreviate_street_type(line, 'TRPK', 'TPKE');
	line = abbreviate_street_type(line, 'TURNPK', 'TPKE');
	line = abbreviate_street_type(line, 'VALLY', 'VLY');
	line = abbreviate_street_type(line, 'VLLY', 'VLY');
	line = abbreviate_street_type(line, 'VDCT', 'VIA');
	line = abbreviate_street_type(line, 'VIADCT', 'VIA');
	line = abbreviate_street_type(line, 'VILL', 'VLG');
	line = abbreviate_street_type(line, 'VILLAG', 'VLG');
	line = abbreviate_street_type(line, 'VILLG', 'VLG');
	line = abbreviate_street_type(line, 'VILLIAGE', 'VLG');
	line = abbreviate_street_type(line, 'VIST', 'VIS');
	line = abbreviate_street_type(line, 'VST', 'VIS');
	line = abbreviate_street_type(line, 'VSTA', 'VIS');
	line = abbreviate_street_type(line, 'WY', 'WAY');
	line = abbreviate_street_type(line, 'APARTMENT', 'APT');
	line = abbreviate_street_type(line, 'BASEMENT', 'BSMT');
	line = abbreviate_street_type(line, 'BUILDING', 'BLDG');
	line = abbreviate_street_type(line, 'DEPARTMENT', 'DEPT');
	line = abbreviate_street_type(line, 'FLOOR', 'FL');
	line = abbreviate_street_type(line, 'FRONT', 'FRNT');
	line = abbreviate_street_type(line, 'HANGAR', 'HNGR');
	line = abbreviate_street_type(line, 'LOBBY', 'LBBY');
	line = abbreviate_street_type(line, 'LOWER', 'LOWR');
	line = abbreviate_street_type(line, 'OFFICE', 'OFC');
	line = abbreviate_street_type(line, 'PENTHOUSE', 'PH');
	line = abbreviate_street_type(line, 'ROOM', 'RM');
	line = abbreviate_street_type(line, 'SPACE', 'SPC');
	line = abbreviate_street_type(line, 'SUITE', 'STE');
	line = abbreviate_street_type(line, 'TRAILER', 'TRLR');
	line = abbreviate_street_type(line, 'UPPER', 'UPPR');

