# pm25frm_to_smat

Python script converts list of FRM PM2.5 values for MATS "Official" monitoring data input file. 
"Unoffical" monitoring file based directly on Official file can be produced as well.

## Input

FRM monitor location data used by the script is included (monitor_locations.csv)

Script also needs two files _not_ included in this repo:
1) Daily PM2.5 data for each monitor
2) Rank (and concentration) of 98-percentile value (e.g., '8' for 8th high)

## Output

A monitoring data file (CSV) formated specifically for EPA's SMAT-CE tool is output by the script
