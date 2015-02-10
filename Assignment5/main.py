import sys
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo
from csvUtils import writeArtistsTable, writeAlbumsTable
from barChart import plotBarChart

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    print "input artists are ", artist_names
    artist_list = []
    albums_list= []
    
    for name in artist_names:
    	get_artist_id = fetchArtistId(name)
    	#print get_artist_id
    	get_artist_info = fetchArtistInfo(get_artist_id)
    	get_album_ids = fetchAlbumIds(get_artist_id)
    	artist_list.append(get_artist_info)
    	for album in get_album_ids:
    		get_album_info = fetchAlbumInfo(album)
    		albums_list.append(get_album_info)
	writeArtistsTable(artist_list)
    writeAlbumsTable(albums_list)
    plotBarChart()
#print artist_list
