# Alex Lee
# Code that reads the csv converted format of the file 'Council Report-Update-03-20-2015-formatted.xlsx'.
# This first part of the code allows ease of simple analysis of the data.
# The second part of the code geocodes the first 300 land parcels using Google's API.

import csv
import numpy as np
import matplotlib.pyplot as plt
import urllib2
import json

def main():
    output = read_csv("CouncilReport2015.csv")
    depart_dict = {}
    classification_dict = {}
    current_use_dict = {}
    ownership_dict = {}
    land_sqft = []
    create_dicts(output, depart_dict, classification_dict, current_use_dict, ownership_dict, land_sqft)
    classification_histogram(depart_dict, classification_dict, current_use_dict, ownership_dict, land_sqft)
    actual_intervals = ['0-10,000 Ft.', '10,000-30,000 Ft.', '30,000-50,000 Ft.', \
                        '50,000-100,000 Ft.', '100,000+ Ft.']
    sqft_count = property_histogram(land_sqft, actual_intervals)
    print_analysis(depart_dict, classification_dict, current_use_dict, ownership_dict, land_sqft, actual_intervals, sqft_count)
    geocode(output)
    #test_function()


# PART 1
def read_csv(file):
    """This function reads a csv file and returns the output as a list"""
    csv_file = open(file)
    csv_file.next()
    reader = csv.reader(csv_file)
    output = list(reader)
    return output
    csv_file.close()


def create_dicts(output, depart_dict, classification_dict, current_use_dict, ownership_dict, land_sqft):
    """ This function creates dictionaries to store various counts for future
    analysis.
    """

    for row in output:
        # Various counts for analysis of the data
        if row[1] not in depart_dict.keys():
            depart_dict[row[1]] = 1
        else:
            depart_dict[row[1]] += 1
        if row[5] not in classification_dict.keys():
            classification_dict[row[5]] = 1
        else:
            classification_dict[row[5]] += 1
        if row[6] not in current_use_dict.keys():
            current_use_dict[row[6]] = 1
        else:
            current_use_dict[row[6]] += 1
        if row[8] not in ownership_dict.keys():
            ownership_dict[row[8]] = 1
        else:
            ownership_dict[row[8]] += 1
        sqft_format1 = row[9].replace(' ', '')
        sqft_format2 = sqft_format1.replace(',', '')
        sqft_format3 = sqft_format2.replace('-', '')
        if sqft_format3 != '':
            land_sqft.append(int(sqft_format3))


def classification_histogram(depart_dict, classification_dict, current_use_dict, ownership_dict, land_sqft):
    """ This function creates and saves a histogram for the classification
    of land parcels. """
    class_intervals = len(classification_dict)
    index = np.arange(class_intervals)
    bar_width = 0.8
    opacity = 0.4
    bar = plt.bar(index, classification_dict.values(), bar_width, alpha=0.6, \
                    color='b')
    plt.xlabel('Classification')
    plt.ylabel('Frequency')
    plt.title('Classification of Properties')
    plt.xticks(index + bar_width / 2, classification_dict.keys())
    plt.tight_layout()
    plt.savefig("classification.png")
    #plt.show()
    plt.clf()


def property_histogram(land_sqft, actual_intervals):
    """ This function creates counts of property sizes and creates and saves
    a histogram. """
    sqft_intervals = 5
    sqft_count = [0] * sqft_intervals
    for sqft in land_sqft:
        if sqft > 100000:
            sqft_count[4] += 1
        elif sqft > 50000:
            sqft_count[3] += 1
        elif sqft > 30000:
            sqft_count[2] += 1
        elif sqft > 10000:
            sqft_count[1] += 1
        else:
            sqft_count[0] += 1
    return sqft_count

    # Use the counts of property sizes to display and save a histogram
    index = np.arange(sqft_intervals)
    bar_width = 0.8
    opacity = 0.4
    bar = plt.bar(index, sqft_count, bar_width, alpha=0.6, color='b')
    plt.xlabel('Square Footage (in thousands)')
    plt.ylabel('Frequency')
    plt.title('Square Footage of Properties')
    plt.xticks(index + bar_width / 2, ('0-10', '10-30', '30-50', '50-100', '100+'))
    plt.tight_layout()
    plt.savefig("square-footage.png")
    #plt.show()
    plt.clf()


def print_analysis(depart_dict, classification_dict, current_use_dict, ownership_dict, land_sqft, actual_intervals, sqft_count):
    """ This function prints the results from earlier analysis. """
    print "Land Parcel Counts for Each Department"
    for key, value in depart_dict.items():
        print "    " + key + ": " + str(value)
    print
    print "Land Parcel Counts for Each Classification"
    for key, value in classification_dict.items():
        print "    " + key + ": " + str(value)
    print
    print "Land Parcel Counts for Type of Ownership"
    for key, value in ownership_dict.items():
        print "    " + key + ": " + str(value)
    print
    print "Land Parcel Counts of Square Footage"
    i = 0
    for interval in actual_intervals:
        print interval + ": " + str(sqft_count[i])
        i += 1

#PART 2

# Extract addresses from file
def geocode(output):
    """ This function takes the addresses out of the csv file and uses Google's
    API to get lattitude and longtitude coordinates. It skips Index Errors and
    stores the results into a csv file. """
    addresses = []
    coordinates = []
    print len(output)
    for row in output:
        addresses.append(row[4].replace(' ', '+'))
    #addresses = addresses[:10]
    #addresses = addresses[:100]
    #addresses = addresses[:300]
    #addresses = addresses[:3]
    
    # Geocode addresses from file using Google's API
    for address in addresses:
        # Get the lattitude and longitude of each address
        json_text = urllib2.urlopen\
        ("https://maps.googleapis.com/maps/api/geocode/json?address="\
        + address + ",+Seattle,+WA&key=AIzaSyAJUuIWJKWIpBfx83k1LpraLzUuu0WXLPE").\
        read()
        json_text = json.loads(json_text)
        try:
            lattitude = json_text["results"][0]["geometry"]["location"]["lat"]
            longitude = json_text["results"][0]["geometry"]["location"]["lng"]
        except IndexError:
            continue
        coordinates.append([lattitude, longitude])
        
    # Write the resulting coordinates in a new csv file
    coordinates_file = open("coordinates.csv", "w")
    writer = csv.writer(coordinates_file)
    writer.writerow([["Lattitude"], ["Longitude"]])
    for coordinate in coordinates:
        writer.writerows([coordinate])
    

def test_function():
    assert depart_dict['SEATTLE CITY LIGHT'] == 172
    assert depart_dict['NEIGHBORHOODS'] == 56
    assert classification_dict['Surplus'] == 8
    assert classification_dict['Interim Use'] == 19
    assert coordinates == [[47.556224, -122.302346], [47.5717083, -122.2977302], [47.5682057, -122.292443]]
    

if __name__ == "__main__":
    main()