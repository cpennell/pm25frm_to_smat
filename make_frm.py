# make_frm.py
# Converts list of FRM PM2.5 values for MATS "Official FRM" input file
# Can also make Unoffical monitoring file based directly on Official file

import csv

make_unofficial = True  # Make "Unofficial" FRM file based on "Official" data

in_file = 'DV_2012_to_2017.csv'  # Raw list of FRM PM2.5 values to format for MATS
outfile = 'fOfficial_2012_2017_21mar2018.csv' # Final output file for use in MATS
unoffFile = 'unOfficial_2012_2017_21mar2018.csv'  # Unofficial file; make_unofficial == True
tmpfile = 'temp_frm_file.csv'       # Interim file; has no flags for 98percentile, rank98
locations_file = 'monitor_locations.csv'    # List of monitor locations (lat, long)
dvfile = 'annual_dv_21mar2018.csv'    # List of annual design values (DV's, rank98)

# Defualts; will replace as apprpriate in outfile:
_98_percentile = '0'
rank98 = '1'

# Let's not bother with these monitors; Scarce data for the 2012-2016 period
skip_these_monitors = [
    '490353013' # H3, Herriman, only starts feb2016
    ]

monitor_locations = {}
with open(locations_file, 'r') as ifh:
    dat = csv.reader(ifh)
    for row in dat:
        _id, lat, lon = row
        monitor_locations[_id] = (lat, lon)

county_map = {
    '003':'Box Elder',
    '005':'Cache',
    '011':'Davis',
    '035':'Salt Lake',
    '045':'Tooele',
    '049':'Utah',
    '057':'Weber'
    }

header = """Day
_ID, _TYPE, LAT, LONG, DATE, PM25, 98_PERCENTILE, EPA_FLAG, COMPLETION_CODE, _STATE_NAME, _COUNTY_NAME, RANK98"""

text_list = []
with open(in_file, 'r') as ifh:
    dat = csv.reader(ifh)
    for i, row in enumerate(dat):
        if i == 0:
            continue

        try:
            monitor_id, date, pm25 = row
        except ValueError:
            print "Problem with inputting the following row!"
            print row
            
        if monitor_id in skip_these_monitors:
            continue

        if pm25 == "":
            continue
        
        county_name = county_map[monitor_id[2:5]]
        lat, lon = monitor_locations[monitor_id]
        st = [monitor_id, 'FRM', lat, lon, date, pm25, _98_percentile, '0', '2', 'Utah', county_name, rank98]
        text_list.append( ','.join(st) + '\n' )
        
ofh = open(tmpfile, 'w')
ofh.write(header + '\n')
for line in sorted(text_list):
    ofh.write(line)

ofh.close()

# Add 98percentile flag and rank98

# Load annual design value and rank98 information
dv_table = {}
with open(dvfile, 'r') as ih:
    dat = csv.reader(ih)
    for row in dat:
        if row[0] == 'Year':
            continue

        year, _id, _98perc, rank = row
        # Don't use monitors with missing values:
        if _98perc == '':
            continue
        
        key = (_id, year)
        val = (_98perc, rank)
        dv_table[key] = val

# Adds quotes to string values for MATS format
def addQuotes(s):
    return '"' + s + '"'

# If we already have an annual dv, we don't need another one
annual_dv_check = {}

oh = open(outfile, 'w')

with open(tmpfile, 'r') as ih:
    dat = csv.reader(ih)
    for i, row in enumerate(dat):
        if i < 2:
            oh.write( ','.join(row) + '\n' )
            continue
        
        _id = row[0]
        year = row[4][:4]
        if (_id, year) in dv_table:
            _98perc, rank = dv_table[(_id, year)]
            pm = row[5]
            # Update rank98 column
            row[11] = rank
            if (_98perc == pm):
                if (_id, year) not in annual_dv_check:
                    # Update 98percentile flag
                    row[6] = '1'
                    annual_dv_check[(_id, year)]=1

        row[0]=addQuotes(row[0])
        row[1]=addQuotes(row[1])
        row[9]=addQuotes(row[9])
        row[10]=addQuotes(row[10])
        oh.write( ','.join(row) + '\n' )

oh.close()

if make_unofficial:
    oh = open(unoffFile, 'w')
    header = """Day
_ID,_TYPE,LAT,LONG,DATE,PM25,EPA_FLAG,USER_FLAG"""

    oh.write(header + '\n')
    with open(outfile, 'r') as ifh:
        dat = csv.reader(ifh)
        for i,row in enumerate(dat):
            if i < 2:
                continue
            
            _id,_type,lat,lon,date,pm25 = row[0:6]
            line=','.join([_id,_type,lat,lon,date,pm25,'0','0'])
            oh.write(line + '\n')

    oh.close()


        
        
        
