
import pandas as pd
import numpy as np
import networkx as nx

def readEdgeList(filename):
	data = pd.read_csv(filename)
	if len(data.columns) > 2:
		print Warning('csv has more than two columns')
		data = pd.read_csv(filename, usecols = [0,1])
		dataframe = pd.DataFrame(data)
	else:
		dataframe = pd.DataFrame(data)
	return dataframe

def degree(edgeList, in_or_out):
	if in_or_out == 'out':
		degree = edgeList['artist'].value_counts()
	elif in_or_out == 'in':
		degree = edgeList['related_artist'].value_counts()
	else:
		print 'Error input should be in or out as string'
	return degree

def combineEdgeLists(edgeList1, edgeList2):
	pieces = [edgeList1, edgeList2]
	concatenated = pd.concat(pieces)
	combined = concatenated.drop_duplicates()
	return combined

def pandasToNetworkX(edgeList):
	g = nx.DiGraph()
	for artist,related_artist in edgeList.to_records(index = False):
		g.add_edge(artist,related_artist)
	return g

def randomCentralNode(inputDiGraph):
	centrality_dict = nx.eigenvector_centrality(inputDiGraph)
	normalization = sum(centrality_dict.values())
	for key in centrality_dict:
		try:
			centrality_dict[key] = centrality_dict[key]/float(normalization)
		except ZeroDivisionError:
			centrality_dict[key] = 1.0/len(centrality_dict)
	random_node = np.random.choice(centrality_dict.keys(), p=centrality_dict.values())
	return random_node

#def randomCentralNode(inputDiGraph):
#	centrality_dict = nx.eigenvector_centrality(inputDiGraph)
#	normalization_constant = float(sum(centrality_dict.itervalues()))
#	for key, value in centrality_dict.items():
#		centrality_dict[key]= value #/ normalization_constant
#	random_node = np.random.choice(centrality_dict.keys())#, p=centrality_dict.values())
#	return random_node

#in_or_out = 'out'
#filenamed = 'artist_list.csv'
#filename2 = 'nirvana.csv'
#edgeList = readEdgeList(filenamed)
#edgeList2 = readEdgeList(filename2)
#input_graph = pandasToNetworkX(edgeList)
#print randomCentralNode(input_graph)

#print degree('testEdgeList.csv', 'out')['4EF5vIcCYKMM61oYOG2Tqa']
