''' Script containing readCSV() function (to read a csv file input)
    get_avg_latlng() to pull the latitude and longitude data from our file
    zip_code_barchart() to get the zip codes for the contractos in the dataset 
    if run latlong from command line then can run get_avg_latlng and if run hist then get zip_code_barchart'''

import csv
import sys

def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)

#print "hello this works" # little test line to make sure the script was running

def get_avg_latlng(filename):
    lines = readCSV(filename)
    sum_lat = 0
    sum_lng = 0
    num_lines = 0
    for i in lines:
        if (i[-3] == ""):
            continue    # continue brings the iteration back to the top of the loop
        if (i[27] == "NJ"):
            continue
        lat = float(i[-3])
        lng = float(i[-2])
        #print (lat, lng)
        num_lines  = num_lines + 1    
        sum_lat = float(sum_lat) + lat
        sum_lng = float(sum_lng) + lng
     
    avg_lat = sum_lat / float(num_lines)
    avg_lng = sum_lng / float(num_lines)       
    
    print("average latitude:", avg_lat, "average longitude:", avg_lng)

#if __name__== '__main__': 
#    get_avg_latlng("permits_hydepark.csv")



from matplotlib import pyplot as plt
import Image

def zip_code_barchart(filename):
    lines = readCSV(filename)
    zipcodes = []
    for i in lines:
        if (i[28] == ""):
            continue
        if (i[27] == "NJ"): # Filtering out the NJ contractors
            continue
        else:
            zi = i[28][0:5]
        zipcode = int(zi)
        zipcodes.append(zipcode)
    
    # Plot a histogram with the zipcodes 
    plt.hist(zipcodes, bins=100) # Check whether the frequency makes sense - it seems to make sense
    plt.xlabel('Contractor Zipcodes')
    plt.ylabel('Frequency')
    plt.title('Zipcode Histogram for Hyde Park')
    #plt.xlim(59000, 61000)
    #plt.ylim(0, 15)
    plt.grid(True)
    plt.draw()
    plt.savefig('histogram.png')
    Image.open('histogram.png').save('histogram.jpg', 'JPEG')
    #print(len(zipcodes))

#if __name__== '__main__':      # comment out otherwise forces an output from function
#    zip_code_barchart("permits_hydepark.csv")


# Setting so that latlong calls get_avg_latlng function and when use hist then use zip_code_barchart
if sys.argv[1] == "latlong":
    get_avg_latlng("permits_hydepark.csv")
elif sys.argv[1] == "hist":
    zip_code_barchart("permits_hydepark.csv")
else:
    print "nothing is working"  # just for a bit of fun! 

