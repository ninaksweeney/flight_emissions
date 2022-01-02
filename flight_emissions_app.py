''' This document is hosted on github and is the source for a Streamlit App. 
The following code is broken into sections based on the user experience of the app. The sections
are as follows:
- Data Setup
- Section 1: Intro & Welcome Text
- Section 2: Dropdown pick lists and data filtering
- Section 3: Map Setup
- Section 4: Building the User Options Table
- Section 5: Alternative actions
'''




# Data Setup
import pandas as pd
import streamlit as st
import pymongo
from pymongo import MongoClient
import pydeck as pdk
import config

#this will make the map stretch out wide when people are on bigger screens,
#better user experience
st.set_page_config(layout="wide")

#connect to cloud Mongodb server
uri = 'mongodb://urhejh70922nhwipt6kt:hNfQXzFxrsDQGGbyH8KX@bs8ntk4apfl7fga-mongodb.services.clever-cloud.com:27017/bs8ntk4apfl7fga'
client = MongoClient( uri )

# MongoDB connection info
hostname = 'bs8ntk4apfl7fga-mongodb.services.clever-cloud.com'
port = 27017
username = 'urhejh70922nhwipt6kt'
password = st.secrets["db_password"]
databaseName = 'bs8ntk4apfl7fga'

# authenticate the database
client = MongoClient(hostname, username=username, password=password, authSource = databaseName, 
                    authMechanism = 'SCRAM-SHA-256')
db = client[databaseName]

#read data from the database into dataframe
@st.cache(allow_output_mutation=True, suppress_st_warning=True, hash_funcs={"MyUnhashableClass": lambda _: None})
def fetching_flight_data():
    return pd.DataFrame(list(db.final_flight_app.find({})))

#this is the dataframe that will show up in map form on our app
flights = fetching_flight_data()

#end data setup, begin building web app interactions





# Section 1: Intro and Welcome Text
st.title('Welcome to Flight Impact!')
st.markdown(
    '''
    Flying is one of the most carbon-intensive ways that we can spend our time as individuals, and its use is dominated by a small group: in 2018, only **11% of the global population** took a flight, and just 
    **1% of the population was responsible for 50% of aviation emissions** ([Time](https://time.com/6048871/pandemic-airlines-carbon-emissions/), 2021). If flying is a part of your life, there are ways to reduce your air travel emissions, and you can start here! Explore route options, understand your flight's carbon impact, and inform your decisions with EPA data.   
      
    **How to get started:**  
    * Compare the carbon emissions of multiple routes by choosing locations from the left-side dropdowns or filtering your search to an emissions limit   
    (*For reference, the EPA estimates that a [typical passenger vehicle](https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle) emits about 4.6 metric tons (4600 kg) of CO2 per year*)
    * Hover over the routes on the map, zoom in, and drag left and right to explore the route map
    * Check out the table at the bottom of the page for alternative routes, emissions comparisons, and additional ways to travel consciously

    
    
    
    ''')



# Section 2: Dropdown pick lists and data filtering

default_value = 'Select or type location'
#create lists of multiselect options to filter the map - unique countries and cities
country_list= [default_value] + sorted(flights.dest_country_full.unique().astype(str))
city_list = [default_value] + sorted(flights.origin_city.unique())

#create origin country multiselect
country_choice_1 = st.sidebar.selectbox('Origin Country', country_list, index=0)

#if country choice is chosen already, filter city options to that country - 
#else just show full list
if country_choice_1 !=default_value:
    city_list1 = [default_value] + sorted(flights.origin_city[flights.origin_country_full==country_choice_1].unique())
    city_choice_1 = st.sidebar.selectbox('Origin City', city_list1, index=0)
else:
    city_choice_1 = st.sidebar.selectbox('Origin City', city_list, index=0)

#create destination country multiselect
country_choice_2 = st.sidebar.selectbox('Destination Country', country_list, index=0)

#if country choice is already chosen, filter city options to that country - 
#else just show full list
if country_choice_2 !=default_value:   
    city_list2 = [default_value] + sorted(flights.origin_city[flights.origin_country_full==country_choice_2].unique())
    city_choice_2 = st.sidebar.selectbox('Destination City', city_list2, index=0)
else:
    city_choice_2 = st.sidebar.selectbox('Destination City', city_list, index=0)


user_emissions_limit = st.sidebar.slider('Per Passenger Emissions Limit (kg)', int(flights.formatted_co2e.min()), int(flights.formatted_co2e.max()), value=int(flights.formatted_co2e.max()))

emissions_limit_filter = flights.formatted_co2e <= user_emissions_limit


#if city is full, filter down to just that city (same with country), 
#otherwise no filter
if city_choice_1 != default_value:
    origin_filter = (flights.origin_city==city_choice_1) | (flights.dest_city == city_choice_1)
elif country_choice_1 != default_value:
    origin_filter = (flights.origin_country_full==country_choice_1) | (flights.dest_country_full==country_choice_1)
else:
    origin_filter = ~flights.origin_country_full.isnull()

#same thing for the destination filter
if city_choice_2 != default_value:
    dest_filter = (flights.origin_city==city_choice_2) | (flights.dest_city == city_choice_2)
elif country_choice_2 != default_value:
    dest_filter = (flights.origin_country_full==country_choice_2) | (flights.dest_country_full==country_choice_2)
else:
    dest_filter = ~flights.origin_country_full.isnull()

#filter the data in the map based on both user's origin & dest choices - if none, just 
#show the airport dots (base layer) and not any routes until locations are chosen
if (city_choice_1 == default_value) & (country_choice_1==default_value) & (city_choice_2==default_value) & (country_choice_2==default_value):
    user_filtered_data = flights[flights.origin_country_full == 'dont show anything']
else:
    user_filtered_data = flights[origin_filter][dest_filter][emissions_limit_filter]





# Section 3: Map Setup

#color of map routes
rgb = [246, 174, 45, 120]

#layer of just the coordinate of each airport. Will always show. 
base_layer = pdk.Layer(
    "ScatterplotLayer",
    flights[['origin_long', 'origin_lat']],
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_min_pixels=2,
    radius_max_pixels=100,
    line_width_min_pixels=1,
    get_position=['origin_long','origin_lat'],
    get_fill_color=[229, 89, 52],
    get_line_color=[229, 89, 52],
    wrapLongitude= True
)
#Layer of the air routes, will be filtered by user inputs
arc_layer = pdk.Layer(
    "ArcLayer",
    data=user_filtered_data[['origin_lat', 'origin_long', 'dest_lat', 'dest_long', 'origin_city', 'origin_country_full',
                                'dest_city','dest_country_full', 'formatted_co2e', 'formatted_tons']],
    get_width = 8,
    get_source_position=['origin_long', 'origin_lat'],
    get_target_position=['dest_long', 'dest_lat'],
    get_source_color=rgb,
    get_target_color=rgb,
    pickable=True, 
    auto_highlight=True, 
    tooltip=True,
    wrapLongitude= True)

#text that shows up when somebody rolls over a route on the map
tooltip_text = {
    "html": "{origin_city}, {origin_country_full} and <br />{dest_city}, {dest_country_full} <br /> <b>Emissions: {formatted_co2e} kg ({formatted_tons} tons) per passenger</b>",
    "style": {"backgroundColor":"white",
              "color":"darkcyan"}}

#initial view of the map. slightly tilted using pitch, and centered on Chad
view_state = pdk.ViewState(pitch=45, zoom = 1.1, latitude = 12.4, longitude = 15.05)

#create the entire map with both layers
deckchart = st.pydeck_chart(pdk.Deck(layers=[base_layer, arc_layer],
                                    map_style = 'light',
                                    initial_view_state= view_state,
                                    tooltip=tooltip_text))






# Section 4: Building the User Options Table

#the data is structured in a way that a single combination of cities will only show  up
#once - that is, CHI-DEN and DEN-CHI do not both exist. However, for the user
#experience, we need to simulate the actual 'origin' and 'destination' options they choose. 
#this takes some data manipulation in the formula below. 

@st.cache(ttl=5*60)
def format_display_df_origin(row):
    #origin city in the data
    origin= f'{row[1]}, {row[2]}'
    #destination city in the data
    destination = f'{row[3]}, {row[4]}'
    #if city choice 1 is chosen, and that city exists as an origin in the data, return
    #the origin data. If it exists as a destination, return the destination data.
    #Do the same for city choice 2 and country choices
    if city_choice_1 != default_value:
        if city_choice_1 in origin:
            return f'{origin}'
        elif city_choice_1 in destination:
            return f'{destination}'
    elif country_choice_1 != default_value:
        if country_choice_1 in origin:
            return f'{origin}'
        elif country_choice_1 in destination:
            return f'{destination}'
    elif city_choice_2!= default_value:
        if city_choice_2 in origin:
            return f'{destination}'
        elif city_choice_2 in destination:
            return f'{origin}'
    elif country_choice_2 != default_value:
        if country_choice_2 in origin:
            return f'{destination}'
        elif country_choice_2 in destination:
            return f'{origin}'

#this is a very similar function but is all opposite because it's formatting our destination
#choice, not the origin choice
@st.cache(ttl=5*60)
def format_display_df_dest(row):
    origin= f'{row[1]}, {row[2]}'
    destination = f'{row[3]}, {row[4]}'
    if city_choice_1 != default_value:
        if city_choice_1 in origin:
            return f'{destination}'
        elif city_choice_1 in destination:
            return f'{origin}'
    elif country_choice_1 != default_value:
        if country_choice_1 in origin:
            return f'{destination}'
        elif country_choice_1 in destination:
            return f'{origin}'
    elif city_choice_2!= default_value:
        if city_choice_2 in origin:
            return f'{origin}'
        elif city_choice_2 in destination:
            return f'{destination}'
    elif country_choice_2 != default_value:
        if country_choice_2 in origin:
            return f'{origin}'
        elif country_choice_2 in destination:
            return f'{destination}'



#break this section of the page into two columns
col1, col2 = st.columns(2)
with col1:
    st.subheader('If your route is flexible...')
    #if nothing's been chosen, prompt them to choose
    if (city_choice_1 == default_value) & (country_choice_1==default_value) & (city_choice_2==default_value) & (country_choice_2==default_value):
        st.write('Choose a location on the left to explore your options!')
    else:
        if len(user_filtered_data)<5:
            # get all the cities in the country of the city that the user chose and show those as alternative options
            if city_choice_2!=default_value:
                dest_city_country = flights[(flights.dest_city == city_choice_2)].dest_country_full.unique()[0]
            # if the destination country only has one city, get the city's continent show those cities as options
                if len(flights[flights.dest_country_full == dest_city_country].dest_city.unique()) == 1:
                    st.write('Look for lower-emission flights to your chosen continent:')
                    dest_city_continent = flights[(flights.dest_city == city_choice_2)].dest_continent.unique()[0]
                    lower_flights_filter = (flights.dest_continent==dest_city_continent) | (flights.origin_continent==dest_city_continent)
                else:
                    st.write('Look for lower-emission flights to your chosen country:')
                    lower_flights_filter = (flights.origin_country_full==dest_city_country) | (flights.dest_country_full==dest_city_country)
                # filter the dataframe by origin filter, and this new destination filter
                lower_flights = flights[origin_filter][lower_flights_filter][['formatted_co2e','origin_city','origin_country_full', 'dest_city', 'dest_country_full']]
                
            elif country_choice_2 != default_value:
            # if the destination country only has one city, get the city's continent and show those cities as options
                if len(flights[flights.dest_country_full == country_choice_2].dest_city.unique()) == 1:
                    st.write('Look for lower-emission flights to your chosen continent:')
                    dest_city_continent = flights[(flights.dest_country_full == country_choice_2)].dest_continent.unique()[0]
                    lower_flights_filter = (flights.dest_continent==dest_city_continent) | (flights.origin_continent==dest_city_continent)
                else:
                    st.write('Look for lower-emission flights to your chosen country:')
                    lower_flights_filter = (flights.origin_country_full==country_choice_2) | (flights.dest_country_full==country_choice_2)
                # filter the dataframe by origin filter, and this new destination filter
                lower_flights = flights[origin_filter][lower_flights_filter][['formatted_co2e','origin_city', 'origin_country_full', 'dest_city', 'dest_country_full']]
            
            lower_flights.rename({'formatted_co2e':'CO2/Passenger', 'origin_city':'Origin', 'origin_country_full':'Origin Country','dest_city':'Dest. City',
                            'dest_country_full':'Dest. Country'}, axis=1, inplace=True)
            #format the data so it's all ordered as the user chose - by origin and destination
            lower_flights['Route Origin'] = lower_flights.apply(format_display_df_origin, axis=1)
            lower_flights['Route Destination'] = lower_flights.apply(format_display_df_dest, axis=1)
            st.dataframe(lower_flights[['CO2/Passenger', 'Route Origin', 'Route Destination']].sort_values('CO2/Passenger', ascending=True)[:30])

        elif len(user_filtered_data)>=5: 
            #if the list of flights is longer than 5, just show all of the routes that match their chosen criteria
            st.write('See the lowest-emission flights with your criteria:')
            user_filtered_data_df = user_filtered_data[['formatted_co2e','origin_city','origin_country_full', 'dest_city', 'dest_country_full']]
            user_filtered_data_df.rename({'formatted_co2e':'CO2/Passenger', 'origin_city':'Origin', 'origin_country_full':'Origin Country','dest_city':'Dest. City',
                            'dest_country_full':'Dest. Country'}, axis=1, inplace=True)
            user_filtered_data_df['Route Origin'] = user_filtered_data_df.apply(format_display_df_origin, axis=1)
            user_filtered_data_df['Route Destination'] = user_filtered_data_df.apply(format_display_df_dest, axis=1)
            st.write(user_filtered_data_df[['CO2/Passenger', 'Route Origin', 'Route Destination']].sort_values('CO2/Passenger', ascending=True))






# Section 5: Alternative actions
with col2:
    st.subheader('If your destination is decided...')
    st.markdown('''
    There are still [ways to minimize your carbon impact](https://grist.org/guides/2021-holiday-makeover/6-habits-of-highly-effective-climate-conscious-travelers/) as an air traveler!  
    * Do you need to fly? Check out options for trains and bus routes before buying a plane ticket
    * Make sure the plane is at full capacity, maximizing efficiency
    * Opt for a newer, regular-sized aircraft (avoid jumbo-jets)
    * Sit in an economy seat 
    * Opt for direct flights instead of layovers
    ''')

for i in range(6):  
    st.text("")

st.markdown('''     
             
   All emissions data you see above was collected from the Climatiq.io API using US EPA standards for calculating flight emissions.
   Airports included are designated 'large airports' by OurAirports.com, defined as a "land airport with scheduled major airline service with millions of passengers/year, or major military base."

''')