
''' Artist Network script with XXX functions
'''

import requests
import pandas as pd
import numpy as np

def getRelatedArtists(artistID):
	url_base = 'https://api.spotify.com/v1/artists/'
	artist_ID = str(artistID)
	end_url = '/related-artists'
	url = url_base + artist_ID + end_url
	req = requests.get(url)
	if req.ok == False:
		print 'Error'
	req_json = req.json()
	get_artists = req_json.get('artists')
	related_artist_list = []
	for i in range(len(get_artists)):
		get_line = get_artists[i]
		get_id = get_line['id']
		related_artist_list.append(get_id)
	return related_artist_list
	

def getDepthEdges(artistID, depth):
	tupl_artist_list_primary = []
	tupl_artist_list = []
	related_ids = []
	related_ids.append(artistID)
	for i in range(depth):
		for ids in related_ids: 
			depth_artist_list = getRelatedArtists(ids)
			for artist in depth_artist_list:
				tupl = (ids, artist)
				tupl_artist_list_primary.append(tupl)
		related_ids = depth_artist_list
	for tupl in tupl_artist_list_primary:
		if tupl not in tupl_artist_list:
			tupl_artist_list.append(tupl)
	return tupl_artist_list 	# Check that tuples not duplicated

def getEdgeList(artistID, depth):
	tuple_list = getDepthEdges(artistID, depth)
	edgelist = pd.DataFrame(tuple_list)
	return edgelist

def writeEdgeList(artistID, depth, filename):
	save_edgelist = getEdgeList(artistID, depth)
	saved_csv_file = save_edgelist.to_csv(filename, index = False, header = ['artist', 'related_artist'])

# need to comment this out! 
#artist = '2mAFHYBasVVtMekMUkRO9g'
#depth = 2
#filename = 'artist_list.csv'
#writeEdgeList(artist,depth,filename)
