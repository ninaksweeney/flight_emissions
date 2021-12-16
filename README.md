# Flight Impact : Data for the Conscious Air Traveler
## Abstract
Flying is one of the most carbon-intensive ways that we can spend our time as individuals, and its use is dominated by a small group: in 2018, only 11% of the global population took a flight, and just 1% of the population was responsible for 50% of aviation emissions ([Time](https://time.com/6048871/pandemic-airlines-carbon-emissions/), 2021). Professionals from a variety of disciplines are looking for ways to reduce emissions from air travel and make the industry more sustainable. In addition, individuals who fly often have the power to help solve this problem by both cutting back on air travel and using it more consciously. Flight Impact is a web app that acts as a first step in educating flight consumers. Users can explore the per-passenger emissions of their flight, compare it to similar and less harmful routes, and learn tips to fly more responsibly. 

[Try it yourself here!](https://share.streamlit.io/ninaksweeney/flight_emissions/main/flight_emissions_app.py)

## Design
This app was designed for an invidual who is accustomed to flying, but doesn't typically factor in the carbon output of their trip. The app is not intended to shame someone for buying a flight, but to help them become an informed consumer and understand the impact of their purchase. The user can explore a variety of data filters:   
* If you're trying to pick a vacation destination, search for all global flights from your city to compare the emissions footprints
* If you know your destination, see other flights to nearby destinations in the same country or continent that my decrease emissions
* Filter your options down to an emissions cap to see which destinations are within your limit
* Explore tips to reduce emissions, even once your flight is chosen

## Data  
Emissions data was collected by first creating a dataset of all possible combinations of [large airport codes](https://datahub.io/core/airport-codes#resource-airport-codes), which had about 180,000 routes. I found the 'great circle' distance between each of the airports, which gave me the length of the route in miles. I then automated an API call to [Climatq.io](https://climatiq.io/) for every route, specifying the airport codes, flight distance, number of passengers, and calculation standard source (I used the EPA standards for all data). I was then able to join this emissions data with the latitude & longitude and insert it into a MongoDB database for storage. 

## Algorithms

Initial data cleaning of airport codes and preparation for the API calls was completed in Google Colab. I also made the API calls and inserted the data into MongoDB using pymongo in Google Colab. From MongoDB, I pulled the data into a .py file that housed my Streamlit web app code. From the database, the flight emissions data was converted to a dataframe for manipulation and front-end interactivity. Finally, the .py file lives in this repo and my Streamlit web app is deployed from the file's URL. 

## Tools  
Data Collection: Python Requests, Climatiq.io, pandas  
Data Storage: pyMongo, MongoDB  
Data Cleaning: Pandas  
Data Visualization: Pydeck  
Web App Deployment: Streamlit  



## Communication  
I completed a 5-minute presentation of the data pipeline and interactive app. Slides and visuals for this project are included in this repository. Future work includes
