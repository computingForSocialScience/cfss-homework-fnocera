''' This script gets the data on the companies we want from a MySQL database using 1) which_company, 
2) company_info_dict makes dictionaries of dates and classes (needs to use pre_saved dictionaries, these are very long so have to save and reopen locally)
3) loat_to_sql uploads clean info to MySQL
4) retreive_dicts retreives the class and dates dictionary for a company from MySQL (this is used in script network_project.py)

'''
import cPickle
import re
import MySQLdb
import csv
from itertools import cycle
from itertools import islice

""" Here I use a database on aws so I cannot put the login on github
"""
dbname="fnocera"
host="klab.c3se0dtaabmj.us-west-2.rds.amazonaws.com"
user=""
passwd=""
db=MySQLdb.connect(db=dbname, host=host, user=user,passwd=passwd)

def which_company(input_name):
	'''Pulls data from our database for the three companies mentioned, makes a dictionary of patent ids for the companies and a list of these ids
	'''
	if input_name == "Nokia":
		sql = """SELECT wku, OrgName, Country FROM uspatents.Assignee WHERE (Assignee.OrgName LIKE "nokia%" AND Assignee.wku NOT LIKE "D%");"""
		cur = db.cursor()
		cur.execute(sql)
		wkus = cur.fetchall()
	
	elif input_name == "Apple":
		sql = """SELECT wku, OrgName, Country FROM uspatents.Assignee WHERE (Assignee.OrgName LIKE "apple %" AND Assignee.wku NOT LIKE "D%");"""
		cur = db.cursor()
		cur.execute(sql)
		wkus = cur.fetchall()

	elif input_name == "Blackberry": 
		sql = """SELECT wku, OrgName, Country FROM uspatents.Assignee 
		WHERE ((Assignee.OrgName LIKE 'research in motion%'AND Assignee.wku NOT LIKE 'D%') OR (Assignee.OrgName LIKE 'blackberry%'AND Assignee.wku NOT LIKE 'D%'));"""
		cur = db.cursor()
		cur.execute(sql)
		wkus = cur.fetchall()

	wku_list = []
	for i in range(len(wkus)):
		wku = wkus[i][0]
		wku_list.append(wku)
	dictionary = dict(zip(wku_list, wku_list))
	return dictionary, wku_list


def company_info_dicts(input_dictionary,wku_list):
	''' This function makes dates and class dictionaries for a company and saves as a cPickle
	'''
	file_open = open("dates_dict.plk", "rb")
	dates_dict = cPickle.load(file_open)
	output_dates_dict = {}
	for wku in input_dictionary:
		if wku in dates_dict:
			date = dates_dict[wku]
			clean_date = date[0:4]
			output_dates_dict[wku] = clean_date
	print "length of dates", len(output_dates_dict) # is 6770

	file_open = open('class_dict.plk', 'rb')
	class_dict = cPickle.load(file_open)

	company_class_list = []
	for i in range(len(wku_list)):
		wku = wku_list[i]
		if wku in class_dict:
			class_ = class_dict[wku]
			class_1 = (wku, class_)
			company_class_list.append(class_1)
	company_class_dict = dict(company_class_list)
	print "length of classes", len(company_class_dict) 
	
	return output_dates_dict, company_class_dict

def load_to_sql(input_name, dates_dict, class_dict):
	''' This file saves date_dict and class_dict data given an input name to classes_project and dates_project tables on MySQL database
	'''
	company_name = input_name
	cur = db.cursor()
	make_dates_table = '''CREATE TABLE IF NOT EXISTS dates_project (company VARCHAR(128), wku VARCHAR(128), dates VARCHAR(128));'''
	make_class_table = '''CREATE TABLE IF NOT EXISTS classes_project (company VARCHAR(128), wku VARCHAR(128), class INTEGER);'''
	cur.execute(make_dates_table)
	cur.execute(make_class_table)

	for key in dates_dict:
		WKU = key
		Dates = dates_dict[key]
		req_1 = """INSERT INTO dates_project (company, wku, dates) VALUES (%s, %s, %s)"""
		cur.execute(req_1,(company_name, WKU, Dates))
        db.commit()

	class_list = []
	for key in class_dict:
		values = class_dict[key]
		for i in range(len(values)):
			value = values[i]
			tupl = (key,value)
			class_list.append(tupl)

	for i in range(len(class_list)):
		WKU = class_list[i][0]
		Class = class_list[i][1]
		data = """INSERT INTO classes_project (company, wku, class) VALUES (%s, %s, %s)"""
		cur.execute(data,(company_name, WKU, Class))
        db.commit()

def retreive_dicts(input_name):
	''' Function to extract the data from MySQL and create date_dict and class_dict
	'''
	company_name = input_name
	cur = db.cursor()
	cur.execute("SELECT wku, dates FROM dates_project WHERE company LIKE (%s);",[company_name])
	wkus_dates = cur.fetchall()
	date_dictionary = dict(wkus_dates)
	#print date_dictionary

	com = "SELECT wku, class FROM classes_project WHERE company LIKE (%s);"
	cur = db.cursor()
	cur.execute(com,[company_name])
	wkus_classes = cur.fetchall()
	class_dict = {}
	for i in range(len(wkus_classes)):
		wku = wkus_classes[i][0]
		clas = wkus_classes[i][1]
		class_dict.setdefault(wku,[]).append(clas)
	#print class_dict

	return date_dictionary, class_dict 

''' 
#This is to run the script for the three companies that we have coded for
names_of_company = ["Nokia", "Apple", "Blackberry"]
for name in names_of_company:
	dic, wku = which_company(name)
	dates_out, classes = company_info_dicts(dic,wku)
	save_sql = load_to_sql(name, dates_out,classes)
'''

#This is extra code to add class_names and class_colours to the database that was added at a later point (03/16/2015)
file_open = open("class_name_dict.plk", "rb")
class_name_dict = cPickle.load(file_open)
open_file = open('classes_to_colour.txt', 'r') 
cur = db.cursor()
make_name_table = "CREATE TABLE IF NOT EXISTS name_project (class VARCHAR(128), name VARCHAR(560))"
cur.execute(make_name_table)
make_color_table = "CREATE TABLE IF NOT EXISTS color_project (class VARCHAR(128), color VARCHAR(128))"
cur.execute(make_color_table)

for name in class_name_dict:
	WKU = name
	class_name = class_name_dict[name]
	req_name = "INSERT INTO name_project (class, name) VALUES (%s, %s)"
	cur.execute(req_name,(WKU, class_name))
	db.commit()

for line in open_file:
	clas = line[0:3]
	if clas = ""
	color = line[4:7]
	cur = db.cursor()
	print color, clas
	req_col = "INSERT INTO color_project (class, color) VALUES (%s, %s)"
	cur.execute(req_col,(clas, color))
	db.commit()
