import requests
from datetime import datetime

def fetchAlbumIds(artist_id):
	'''Using the Spotify API take an artist_id and returns a list of 
	albums_id in a list'''
	url_base = 'https://api.spotify.com/v1/artists/'
	artist_id_str = str(artist_id)
	url = url_base + artist_id_str + '/albums?market=US&album_type=album'
	#print url
	req = requests.get(url)
	if req.ok == False:
		print 'Error'
	req_json = req.json()
	get_items = req_json.get('items')
	album_list = []
	for i in range(len(get_items)):
		get_line = get_items[i]
		get_id = get_line['id']
		album_list.append(get_id)
	return album_list
	

def fetchAlbumInfo(album_id):
	url = 'https://api.spotify.com/v1/albums/' + album_id
	#print url
	req = requests.get(url)
	if req.ok == False:
		print 'Error lalal'
	req_json = req.json()
	get_artists = req_json.get('artists')
	artist_id = get_artists[0]['id']
	get_album_id = album_id
	get_name = req_json.get('name')
	get_year = req_json.get('release_date')
	year = get_year[0:4]
	get_popularity = req_json.get('popularity')
	keys = ['artist_id', 'album_id', 'name', 'year', 'popularity']
	values = [artist_id, album_id, get_name, year, get_popularity]
	album_dict = dict(zip(keys,values))
	return album_dict

#album_id = '6hU9JCoqq4GjYq86dQ1o9b'
#print(fetchAlbumInfo(album_id))


