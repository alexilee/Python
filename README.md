# Python

Here are a few examples of projects/code that I've done.
1. DistillingWeb
* Scrapes a list of cities from a site ranking traffic. Uses nominatum API to return json geometry for each city scraped. Uses pandas and geopandas to plot the points on a map.
2. RealEstatebyNeighborhood
* Group project analyzing Real Estate price changes by neighborhoods in the greater Seattle area in the year intervals of 2005, 2010, and 2015 where I played the role of the developer. The code starts by reading in and formatting a CSV file containing King County parcel IDs. It uses these IDs to scrape appraisal values (for all three years) from the King County Assessor's site. Using Nominatum's API, polygons are created for each neighborhood and the values are stored inside each geojson. The geojson's are outputted and used in an interactive visualization via Mapbox.
3. SeattlePublicLands
* Analysis of all property publicly owned by the city of Seattle. The code reads in a large file from the City of Seattle government containing data on all publicly owned properties. The first part of the code performs basic aggregations and analysis and creates a couple histogram to display the results. The second part of the code uses Google's API to geocode each address and stores them into a CSV file.
