#!/usr/bin/python
import os
import csv
import time
import calendar

#Global
Feed = {}

#Functions
#Setting up working directory to_dict on all files in folder
def start():
	global Feed
	apath = raw_input("Insert location of GTFS Folder Unzipped... ")
	print timestamp() # Start Timer
	os.chdir(apath)
	Feed = to_feed(file_walk(apath))
	return None
	
#Finds all .txt Files in a Folder
def file_walk(s):
	txtFiles = []
	for root, dirs, files in os.walk(s):
		for f in files:
			if f.endswith('.txt'):
				txtFiles.append(f)
	return txtFiles
	
#Makes a Dictionary Entry e.g. "{stops.txt":[["...","...","..."]["...","...","..."]]}
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
		output.append(Feed[file][0]) #Retain Top Line
		for arg in args:
			hit_list.append(str(arg))
		for row in Feed[file]:
			if row[indexer(file,field)] in hit_list:
				output.append(row)
	except:
		print "File Search Failed"
	return [output, file]

#Removes All Rows with Entries in a Fields that Match Args
def remove_rows(file, field, *args):
	global Feed
	output = []
	remove_list = []
	try:
		for arg in args:
			remove_list.append(str(arg))
		for row in Feed[file]:
			if row[indexer(file,field)] not in remove_list:
				output.append(row)
			else:
				pass
	except:
		print "Remove Failed"
	return [output, file]
			
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
			filematch.append(Feed[items][0]) #Populates Top Line
			count = 0
			for row in Feed[items]:
				for item in row:
					if item in hit_list:
						count += 1
						filematch.append(row)
			if count == 0:
				filematch.pop(0) #Pop's Off Top Line if List is Otherwise Empty
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
		print "Saving File!"
		try:
			filename = "%s_%s.txt" % (timestamp(),str(s[1]))
			with open(filename, 'wb') as f:
				writer = csv.writer(f)
				for row in s[0]:
					writer.writerow(row)
		except:
			print "Save List to File Failed"
			
	elif isinstance(s, dict) == True:
		print "Saving Files!"
		try:
			for item in s:
				if s[item] != []: # Prevents Writing Empty Files
					filename = "%s_%s" % (timestamp(), item)
					with open(filename, 'wb') as f:
						writer = csv.writer(f)
						writer.writerows(s[item][0:])
		except:
			print "Save Dict to File Failed!"

	else:
		pass
		
#Feed Validation Tools
#Checks For Unused Stops by comparing the stop_times.txt & the stops.txt
def check_unused():
	stop_list = []
	unused_stops = []
	unused_stop_count = 0
	try:
		for row in Feed["stop_times.txt"]:
			if row[indexer("stop_times.txt","stop_id")] not in stop_list:
				stop_list.append(row[indexer("stop_times.txt","stop_id")])
		for row in Feed["stops.txt"]:
			if row[indexer("stops.txt","stop_id")] not in stop_list:
				unused_stops.append(row)
				unused_stop_count += 1
		if unused_stop_count > 0:
			print str(unused_stop_count) + " unused stops detected!"
		return unused_stops
	except:
		print "check_unused failed!"
		
""" Feed statistics
# Number of Agencies
# Number of Routes
# Number of trips
# Number of stops
# Number of stop times
"""
def feed_statistics():
	agency_list = []
	route_list = []
	trip_list = []
	stop_list = []
	stop_times_list = []
	agency_count = 0
	route_count = 0
	trip_count = 0
	stop_count = 0
	stop_times_count = 0
	for row in Feed["agency.txt"]:
		if row[indexer("agency.txt", "agency_name")] not in agency_list:
			agency_count += 1
			agency_list.append(row[indexer("agency.txt", "agency_name")])
	for row in Feed["routes.txt"]:
		if row[indexer("routes.txt", "route_id")] not in route_list:
			route_count += 1
			route_list.append(row[indexer("routes.txt", "route_id")])
	for row in Feed["trips.txt"]:
		if row[indexer("trips.txt", "trip_id")] not in trip_list:
			trip_count += 1
			trip_list.append(row[indexer("trips.txt", "trip_id")])
	for row in Feed["stops.txt"]:
		if row[indexer("stops.txt", "stop_id")] not in stop_list:
			stop_count += 1
			stop_list.append(row[indexer("stops.txt", "stop_id")])
	
	for row in Feed["stop_times.txt"]:
		stop_times_count += 1
			
	print "Agency Count: " + str(agency_count), "Route Count: " + str(route_count), "Trip Count: " + str(trip_count), "Stop Count: " + str(stop_count), "Stop times: " + str(stop_times_count)
	return {"Agency Count": str(agency_count), "Route Count": str(route_count), "Trip Count": str(trip_count), "Stop Count": str(stop_count), "Stop Times Count": str(stop_times_count)}

#Initialize Fuctions / Feed		
start()
feed_statistics()
check_unused()
print timestamp()


#Script Samples
#Remove any Number of rows Based on Matching in One Field.
#print remove_rows("fare_attributes.txt", "price", "1.25")

#File Search any Number of Items Based on Matching in One Field.
#print file_search("stops.txt", "stop_id", "NANAA", "DADAN")
#print file_search("trips.txt", "route_id", "AAMV")

#write to file Writes "output_" + timestamp.csv to Working Directory / Feed Location
#write_to_file(remove_rows("stop_times.txt", "trip_id", "CITY2", "CITY1"))
#write_to_file(remove_rows("frequencies.txt", "headway_secs" , "1800"))

#write_to_file(file_search("routes.txt", "agency_id", "DTA"))
#write_to_file(file_search("frequencies.txt", "headway_secs" , "600", "1800"))

"""
#Function Calls to Test Speed
feed_search("AB")
remove_rows("frequencies.txt", "headway_secs" , "1800")
remove_rows("frequencies.txt", "headway_secs" , "1800")
remove_rows("stops.txt", "stop_name", "King St and S West St", "Mt Vernon Ave and E Mason Ave", "King St Metro Station - Bay B")
file_search("stops.txt" , "stop_id" , "NANAA" , "BULLFROG" , "FUR_CREEK_RES")
file_search("trips.txt" , "route_id" , "STBA" , "AB" , "BFC")

print timestamp()# End Timer

#Showing How Some of The Data in Feed Looks
#Print First Five Rows of all Entries in Global Feed
for item in Feed:
	print Feed[item][0:5]
	
#Print First Row of all Entries in Global Feed
for item in Feed:
	print Feed[item][0]
"""
#This is fun glitch art. Prints out the contents of the file. Ctrl+ C for KeyboardInterrupt.
#print Feed["stops.txt"][0:]
#print Feed["trips.txt"][0:]
#print Feed["stops.txt"][0:]
#print Feed["agency.txt"][0:]
#print Feed["stop_times.txt"][0:]
