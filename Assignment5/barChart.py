import unicodecsv as csv
import matplotlib.pyplot as plt

def getBarChartData():
    ''' function that extracts data needed for bar chart from artists.csv and albums.csv
    and produces x_vals as decades, y_vals as counts of albums released in any decade and artist_names list 
    '''
    f_artists = open('artists.csv') #opens the file artists.csv and renames f_artists in the python environment
    f_albums = open('albums.csv') #open the file albums.csv

    artists_rows = csv.reader(f_artists) #reads the rows in the artists.csv file (f_artists) 
    albums_rows = csv.reader(f_albums)

    artists_header = artists_rows.next() #pulls next item from an iterator ie ignore the first row which is the header
    albums_header = albums_rows.next()

    artist_names = [] #new list artist_names
    
    decades = range(1900,2020, 10) #set range of decades between 1900 to 2020 
    decade_dict = {} #empty dictionary where we set the keys as decades and values all zero initially 
    for decade in decades:
        decade_dict[decade] = 0
    
    for artist_row in artists_rows: #for each row in artits_rows takes 4 variables and gives then variable names
        if not artist_row:          #this row ensures that this only works for artist_row
            continue
        print artist_row
        artist_id, name, followers, popularity = artist_row
        artist_names.append(name) #name is added to artist_name list 

    for album_row  in albums_rows: #similar to above
        if not album_row:
            continue
        artist_id, album_id, album_name, year, popularity = album_row
        for decade in decades: #if year is within a particular decade then add one to the dictionary value for that decade
            if (int(year) >= int(decade)) and (int(year) < (int(decade) + 10)):
                decade_dict[decade] += 1
                break

    x_values = decades
    y_values = [decade_dict[d] for d in decades] #y is the counts of albums in the decades
    return x_values, y_values, artist_names

def plotBarChart():
    ''' function that plots bar chart using x_vals, y_vals and artist_names from getBarChartData() function
    '''
    x_vals, y_vals, artist_names = getBarChartData() #gets variables from getBarChartData function
    
    fig , ax = plt.subplots(1,1) #one plot
    ax.bar(x_vals, y_vals, width=10) #plots bar chart of x_vals, y_vals 
    ax.set_xlabel('decades') #labels x axis as decades
    ax.set_ylabel('number of albums') #labels number of albums as y axis 
    ax.set_title('Totals for ' + ', '.join(artist_names)) #title for plot that takes artists names from artist_names list
    plt.show() #shows plot
    #plt.grid(True)
    #plt.draw()
    #plt.savefig('artists_plot.png')

    
