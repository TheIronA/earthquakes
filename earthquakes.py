# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json
import matplotlib.pyplot as plot
from datetime import date

def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text

    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.

    ## saving and printing json file
    # creating the json 
    #save_file= open("response_text.json", "w")

    # writing the json
    #json.dump(text, save_file, indent=4)
    #save_file.close()

    # opening the json file
    #with open("response_text.json", "r") as file:
    #    text = json.load(file)

    # printing the json data
    # print(json.dumps(text, indent=4))

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values? - comma separated values (csv)

    ## how many broad sections does this response compromise?
    # type
    # metadata {generated, url, title, status, api, count}
    # features {type: feature, properties: {mag, place, tz, url, detail}}

    dict = json.loads(text)
    return dict

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return data['metadata']['count']


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return earthquake['geometry']['coordinates'][:2]

def get_year(earthquake):
    """Retrieve the year of an earthquake item."""
    time = date.fromtimestamp(earthquake['properties']['time'] / 1000) # convert milliseconds to seconds
    return time.year

def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    max = 0
    max_list = []
    location = []

    # only accounted for one earthquake
    for i in data['features']:
        if get_magnitude(i) > max:
            max = get_magnitude(i)
            max_list.append(get_magnitude(i))
            location.append(get_location(i))
    
    # taking the max from the array 

    return max_list, location


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")



# plot of frequency of earthquakes per year 
years = {}
for i in data['features']:
    year = get_year(i)
    if year in years:
        years[year] += 1
    else:
        years[year] = 1
x = list(years.keys())
y = list(years.values())
plot.bar(x, y)
plot.xlabel("Year")
plot.ylabel("Frequency")
plot.title("Frequency of Earthquakes per Year")
plot.show()


# plot of average magnitude of earthquakes per year 

# use total magnitude / count_earthquakes() within a year

years = {}

for i in data['features']:
    year = get_year(i)
    if year in years:
        years[year]['count'] += 1
        years[year]['total_magnitude'] += get_magnitude(i)
    else:
        years[year] = {'count': 1, 'total_magnitude': get_magnitude(i)}

x = []
y = []
for year in years:
    x.append(year)
    y.append(years[year]['total_magnitude'] / years[year]['count'])

plot.bar(x, y)
plot.xlabel("Year")
plot.ylabel("Average Magnitude")
plot.title("Average magnitude of Earthquakes per Year")
plot.show()

