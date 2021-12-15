# Emissions Itinerary: Travel Planning with Carbon Emissions in Mind
For many in the United States, air travel is built in to normal life; going home for the holidays, taking a family vacation, or visiting a National Park all require boarding a plane. Most of us prepare for takeoff without ever considering the impact of our flight - BBC writes that air travel is responsible for [5% of global warming](https://www.bbc.com/future/article/20200218-climate-change-how-to-cut-your-carbon-emissions-when-flying), and demand for flights continues to grow. There are many convincing arguments for the misleading nature of an individual's 'carbon footprint' compared to large corporations, however when [one percent of the world's population accounts for more than half of air travel emissions](https://www.lunduniversity.lu.se/article/one-percent-worlds-population-accounts-more-half-flying-emissions), vacationers actually have an opportunity to make impactful change. Whether it's cutting back on flying in a given year, or taking actions like avoiding empty flights and old planes, there are ways that we as individuals can contribute. 

Using carbon emissions data collected from the [Carbon Interface API](https://www.carboninterface.com/) for flight routes around the world, I plan to build an interactive app that helps individuals see the impact of their air travel and opt for less detrimental options. 


## Question/Need 
- Air travel is largely used by a small percentage of people, and is contributing to climate change.   
- Help people understand the impact of their flight and make travel decisions consciously

## Data
- I plan to collect emissions data points from at least 500,000 airport combinations on the [Carbon Interface API](https://www.carboninterface.com/)  
- IATA international airport codes and coordinates from [Datahub.io](https://datahub.io/core/airport-codes#resource-airport-codes)


## Tools
- Data Collection: Carbon Interface API and python requests
- Data Storage: MongoDB
- Data Analysis & Preparation: Google Colab
- Web App Creation: Streamlit

## MVP Goal
- End to End MVP finished: Data collected, stored, and basic analysis done. Basic Streamlit app set up 
- If possible, I'd like to have some user interaction built in, such as choosing start/end points for a flight
