''' Makes network and other outputs needed by interface.py which is our app. 
Contains the functions 1) retreive_dicts which retreives date_dict, class_dict and a list of patentIDs for a given company name input
2 + 3) date_Range and get_patents_classes were initially written to split the patent data into two dependent on a time_value, however this is not used.
4) make_network takes the inputs: dates_dict,class_dict, input_name, it is a long function which makes a Counter of the number of patents in each 
patent class (like a patent technology category) and makes an edge list for classes that are co-cited within patents. This is to create our bipartite
network between patents and classes but projected simply into the class space. patent_count returns the numbers of patents in each class which is the node_size
of the nodes in the network graph. 
'''
import cPickle
import MySQLdb
import igraph
import cairo
from itertools import combinations
from collections import Counter
import networkx as nx
from networkx.readwrite import json_graph
import json
import os

""" Here I use a database on aws so I cannot put the login on github
"""
dbname="fnocera"
host="klab.c3se0dtaabmj.us-west-2.rds.amazonaws.com"
user=""
passwd=""
db=MySQLdb.connect(db=dbname, host=host, user=user,passwd=passwd)

def retreive_dicts(input_name):
	company_name = input_name
	sql = """SELECT wku, dates FROM dates_project WHERE company LIKE (%s);"""
	cur = db.cursor()
	cur.execute(sql,[company_name])
	wkus_dates = cur.fetchall()
	date_dictionary = dict(wkus_dates)

	com = "SELECT wku, class FROM classes_project WHERE company LIKE (%s);"
	cur = db.cursor()
	cur.execute(com,[company_name])
	wkus_classes = cur.fetchall()
	class_dict = {}
	for i in range(len(wkus_classes)):
		wku = wkus_classes[i][0]
		clas = wkus_classes[i][1]
		class_dict.setdefault(wku,[]).append(clas)
	return date_dictionary, class_dict, wkus_classes 


def date_Range(limit_value, dates_dict):
	first_dates= []
	second_dates = []
	for key, value in dates_dict.iteritems():
		if limit_value >= value:
			tupl = (key, value)
			first_dates.append(tupl)
		elif limit_value < value:
			tupl = (key, value)
			second_dates.append(tupl)
	return first_dates, second_dates


def get_patents_classes(date_patents,company_class_dict):
	list_to_use = []
	for (patent, date) in date_patents:
		classes_in = company_class_dict[patent]
		patent_and_class = (patent, classes_in)
		list_to_use.append(patent_and_class)
	return list_to_use
#print list_to_use


def make_network(dates_dict,class_dict, input_name):
	''' Here we make our network of classes given the co-citation of the classes within patents of a given company 
	'''
	edgeCounts = Counter()
	patentCounts = Counter()
	patentindexCounts = Counter()

	list_to_use = class_dict.items()
	class_list = []
	class_to_index = {}
	index_to_class = {}
	index = 0
	for patent in list_to_use:
		for i in range(len(patent[1])):
			item = patent[1][i]
			item = int(item)
			patentCounts[item] +=1
			if item not in class_list:
				class_list.append(item)
				class_to_index[item] = index
				index_to_class[index] = item
				index += 1
		for catpair in combinations(patent[1],2):
			cat_1, cat_2 = catpair
			cat_1_index = class_to_index[cat_1]
			cat_2_index = class_to_index[cat_2]
			new_catpair = (cat_1_index, cat_2_index)
			sortedpair = tuple(sorted(new_catpair))
			edgeCounts[sortedpair] +=1

	for key in patentCounts:
		ind = class_to_index[key]
		patentindexCounts[ind] = patentCounts[key]

	patent_count = []
	for i in range(len(patentindexCounts)):
		node_count = patentindexCounts[i]
		patent_count.append(int(node_count))
	#print patent_count

	node_number = len(class_list)
	edges = edgeCounts.keys()
	edge_weights = edgeCounts.values()
	nodes = patentCounts.keys()
	
	class_name = []
	sql = "SELECT class, name FROM name_project;"
	cur = db.cursor()
	cur.execute(sql)
	name_dict = dict(cur.fetchall())
	for clas in class_list:
		if str(clas) in name_dict:
			name = name_dict[str(clas)]
			class_name.append(name)
		else:
			name = 'None'
			class_name.append(name)
	#print class_name
	#print edgeCounts, class_list
	
	'''
	#This is a part of the code that is not used but uses a categorization devised by me instead of clustering to color the nodes
	sql = "SELECT class, color FROM color_project;"
	cur = db.cursor()
	cur.execute(sql)
	colours = cur.fetchall()

	colour_dict = {}
	for i in range(len(colours)):
		clas = colours[i][0]
		col = colours[i][1]
		if col == 'bla':
			key = clas
			value = 1
			colour_dict[key] = value
		elif col == "":
			key = clas
			value = 1
			colour_dict[key] = value
		elif col == 'blu':
			key = clas
			value = 2
			colour_dict[key] = value
		elif col == 'red':
			key = clas
			value = 3
			colour_dict[key] = value
		elif col == 'yel':
			key = clas
			value = 4
			colour_dict[key] = value
		elif col == 'cya':
			key = clas
			value = 5
			colour_dict[key] = value
		elif col == 'gre':
			key = clas
			value = 6
			colour_dict[key] = value
	
	#print colour_dict
	#These are in the same order so is okay 
	colour_groups = []
	for node in range(node_number):
		#if node in index_to_class:
		clas = index_to_class[node]
		clas = str(clas)
		if clas in colour_dict: 
			group = colour_dict[clas]
			colour_groups.append(group)
		else:
			group = 1
			colour_groups.append(group)
	'''

	#Here we make an igraph network first to obtain eigenvector_centrality, betweenness and community structure which we then feed to our interface.py
	g = igraph.Graph()
	g.add_vertices(node_number)
	g.add_edges(edges)
	g.es["weight"] = edge_weights
	layout = g.layout_kamada_kawai()
	g.vs["class_number"] = class_list
	#g.vs["class_name"] = class_name
	node_size = patent_count
	g.vs["node_size"] = node_size
	#If we wanted to plot the igraph, just need to unhash below
	#igraph.plot(g, layout = layout, edge_width=igraph.rescale(g.es["weight"], out_range=(0.5, 100)))

	eigenvector_cent = g.eigenvector_centrality(directed=False, scale=True, weights="weight", return_eigenvalue=False)
	between = g.betweenness(vertices=None, directed=False, cutoff=None, weights="weight")
	community = g.community_multilevel()
	member = community.membership

	bet_dict = {}
	eig_dict = {}
	cluster_dict = {}
	for i in range(node_number):
		m = index_to_class[i]
		eigenvect = eigenvector_cent[i]
		betw = between[i]
		eig_dict[m]=eigenvect
		bet_dict[m]=betw
		clust = member[i]
		cluster_dict[m]=clust

	#Here we make the network in networkx in order to be able to save the file as a .json
	DG = nx.Graph()
	DG.add_nodes_from(range(node_number))
	#for i in range(node_number): #This part is to change the colour scheme to a different one
	#	m = index_to_class[i]
	#	DG.node[i]["name"]= m
	DG.add_edges_from(edges)
	counting = 0
	for (i,j) in edges:
		val = edge_weights[counting]
		counting += 1
		val = float(val)
		DG.edge[i][j]['weight'] = val
	for i in range(len(member)):
		memb = member[i]
		DG.node[i]["group"]=memb
	for i in range(len(class_name)):
		name = class_name[i]
		DG.node[i]["name"]= name
	json_data = json_graph.node_link_data(DG)
	
	#This makes the static folder if it does not exist, removes any old version of the file and then saves the new network file.
	static = 'static'
	if not os.path.exists(static):
		os.makedirs(static)

	file_name = input_name + ".json"
	if os.path.exists("/static/file_name"):
		os.remove("/static/file_name")

	with open(os.path.join(static,file_name), "w") as outfile:
		b = json.dump(json_data, outfile)


	return patent_count, patentCounts, name_dict, bet_dict, eig_dict






