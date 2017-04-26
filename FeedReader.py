#!/usr/bin/python
import os
import csv
import time
import calendar

#Global
Feed = {}

#Functions
#Finds all .txt Files in a Folder
def file_walk(s):
	txtFiles = []
	for root, dirs, files in os.walk(s):
		for f in files:
			if f.endswith('.txt'):
				txtFiles.append(f)
	return txtFiles
	
#Makes a Dictionary Entry e.g. {"stops.txt":["...","...","..."]
def to_dict(s):
	f_dict = {}
	f_list = []
	tmp_list = csv.reader(open(s, "rb"))
	for row in tmp_list:
		f_list.append(row)
	f_dict = {s: f_list}
	#print f_dict[] # Check Top Line Values
	return f_dict

#Calls to_dict and Updates Global Feed
def to_feed(s):
	global Feed
	local_feed = {}
	for item in s:
		tmp_entry = to_dict(item)
		Feed.update(tmp_entry)
		local_feed.update(tmp_entry)
	return local_feed
	
#Finds the Column of a Field in the Top Line
def indexer(file, field):
	topline = Feed[file][0]
	loc = topline.index(field)
	return loc
	
#Search File for all args / One or Many
def file_search(file, field, *args):
	global Feed
	output = []
	hit_list = []
	try:
		#output.append([Feed[file][0]]) #Retain Top Line
		for arg in args:
			hit_list.append(str(arg))
		for row in Feed[file]:
			if row[indexer(file,field)] in hit_list:
				output.append([row])
	except:
		print "File Search Failed"
	return output

#Removes All Rows with Entries in a Fields that Match Args
def remove(file, field, *args):
	global Feed
	output = []
	remove_list = []
	try:
		for arg in args:
			remove_list.append(str(arg))
		for row in Feed[file]:
			if row[indexer(file,field)] not in remove_list:
				output.append([row])
			else:
				pass
	except:
		print "Remove Failed"
	return output
			
def feed_search(*args):
	global Feed
	hits = {}
	filematch = []
	hit_list = []
	try:
		for arg in args:
			hit_list.append(arg)
		for items in Feed:
			filematch = []
			for row in Feed[items]:
				for item in row:
					if item in hit_list:
						filematch.append([row])
			match = {items: filematch}
			hits.update(match)
	except:
		print "Feed Search Failed"
	return hits
	
#Returns a String of Seconds from The Unix Epoch
def timestamp():
	timestamp = str(calendar.timegm(time.gmtime()))
	return timestamp

#Writes a list or a dict to File Folder	
def write_to_file(s):
	if isinstance(s, list) == True:
		with open("output.csv", "wb") as f:
			writer = csv.writer(f)
	elif isinstance(s, dict) == True:
		for item in s:
			if s[item] != []: # Prevents Writing Empty Files
				filename = "%s_%s" % (timestamp(), item )
				with open(filename, "wb") as f:
					writer = csv.writer(f)
					for item in s[item]:
						writer.writerows(item)
	else:
		pass
			

#Should be __init__?
#Setting up Working Directory & Running Functions
apath = raw_input("Insert location of GTFS Folder Unzipped... ")
print timestamp() # Start Timer
os.chdir(apath)
to_feed(file_walk(apath)) #feed read __init__?

#Script Samples
#Remove any Number of rows Based on Matching in One Field.
#print remove("fare_attributes.txt", "price", "1.25")

#File Search any Number of Items Based on Matching in One Field.
#print file_search("stops.txt", "stop_id", "NANAA", "DADAN")
#print file_search("trips.txt", "route_id", "AAMV")

#write to file Writes "output_" + timestamp.csv to Working Directory / Feed Location
#write_to_file(remove("stop_times.txt", "trip_id", "CITY2", "CITY1))
#write_to_file(remove("routes.txt" , "route_id" , "BFC")

#write_to_file(file_search("routes.txt", "agency_id", "DTA"))
#write_to_file(file_search("frequencies.txt", "headway_secs" , "600", "1800"))

#Random Search to Test Speed
feed_search("-116.751677")
remove("frequencies.txt", "headway_secs" , "600", "1800")
file_search("stops.txt" , "stop_id" , "NANAA" , "BULLFROG" , "FUR_CREEK_RES")
file_search("trips.txt" , "route_id" , "STBA" , "AB" , "BFC")

print timestamp()# End Timer

"""
#Showing How Some of The Data in Feed Looks
#Print First Five Rows of all Entries in Global Feed
for item in Feed:
	print Feed[item][0:5]
#Print First Row of all Entries in Global Feed
for item in Feed:
	print Feed[item][0]

#This is fun glitch art. Prints out the contents of the file. Ctrl+ C for KeyboardInterrupt.
print Feed["stops.txt"][0:]
#print Feed["trips.txt"][0:]
#print Feed["stops.txt"][0:]
#print Feed["agency.txt"][0:]
#print Feed["stop_times.txt"][0:]
"""