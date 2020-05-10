# COVID-19-Visualizations
Visualizations of the novel coronavirus using data science and machine learning techniques. Please feel free to contribute by sending issues or pull requests. I will do my best effort to update this daily. There is a lot of reading and writing of data involved, so the notebook tends to take around 30 minutes to completely run a fresh copy of the notebook. Apoligies in advanced if this causes your browser to crash because of high RAM usage (Runs okay on my machine with 8GB of RAM and in Chrome). At the time of making this project, I have never formally studied data science or machine learning yet, so feedback is much appreciated. I was able to build this project through extensive documentation reading of the data science and machine learning packages, and I may be missing more efficient ways to run my code.

**If your intentions are to use this for a school project or personal project, please fork this repository and email [briancpark@berkeley.edu](mailto:briancpark@berkeley.edu). I am interested in what you are willing to create or have created with my code**

_Stay Strong, Stay Home, and Save Lives_

![COVID-19 Confirmed](timelapses/us_confirmed_timelapse.gif)

## Dependencies
This project uses Pandas, NumPy, MatPlotLib, GeoPandas, and Descartes, plotly, and Selenium. All the code needed to run is in [`COVID19 Visualizations.ipynb`](https://github.com/briancpark/COVID-19-Visualizations/blob/master/COVID19%20Visualizations.ipynb). Please make sure you have installed the all the Python libraries before you run the code. Also make sure to install `ffmpeg` if you want to compile graphics into video.

## Databases
[NYTimes](https://github.com/nytimes/covid-19-data) database was used for United States of America data and [JHU CSSE](https://github.com/CSSEGISandData/COVID-19) database was used for international data. Repository is updated bidaily as both databases update around 12 hours apart. Notebook is conveniently coded with UNIX commands so that all it takes to update the visualizations is a simple restart and rerun of the kernel.

# Core Functions

## `country(country_name, data)`
Displays the graphs of a country associated with the type of data (confirmed, deaths, or recovered)

## `country_legend(country_name)`
Displays the graphs of all the types of data for a given country

## `country_active_cases(country_name)`
Displays the graph of active cases of COVID-19 for a given country. Calculated by `active = confirmed - deaths - recovered`

## `compare_countries(list_countries)`
Displays the all graph for a list of given countries. All on top of each other for comparison of statistics.

# Update Functions

## `update_all_cases_country_individual()`
Updates/overwrites all the graphs by country and data type (confirmed, deaths, recovered) in the `cases_country_individual/` directory.

## `update_all_cases_country()`
Updates/overwrites all the graphs by country and all data types in the `cases_country/` directory

## `update_all_cases_country_active()`
Updates/overwrites all the graphs of active cases by country in the `cases_country_active/` directory


# Global Statistics

## `worldwide_cases()`
Updates/overwrites the worldwide COVID-19 cases. Saved in the main directory as `COVID19_worldwide.png`

![Global Statistics](COVID19_worldwide.png)

## `worldwide_active()`
Updates/overwrites the worldwide COVID-19 active cases. Saved in the main directory as `COVID19_worldwide_active.png`

![Global Active Statistics](COVID19_worldwide_active.png)

# Geo Functions
These functions utilize the GeoPandas library to visualize COVID-19 cases on the map.

## `compile_timelapse()`
Uses `ffmpeg` to compile into video and gif format.

# Visualizations

## Timelapses

### Confirmed COVID-19 Cases Worldwide
![COVID-19 Confirmed on Map](timelapses/global_confirmed_timelapse.gif)

### Deaths from COVID-19 Worldwide
![COVID-19 Deaths on Map](timelapses/global_deaths_timelapse.gif)

### Recovered COVID-19 Cases Worldwide
![COVID-19 Recovered on Map](timelapses/global_recovered_timelapse.gif)

### Confirmed COVID-19 Cases by County in United States
![COVID-19 Confirmed](timelapses/us_confirmed_timelapse.gif)

### COVID-19 Deaths by County in United States
![COVID-19 Deaths](timelapses/us_deaths_timelapse.gif)

## Graphs

### COVID-19 Worldwide Cases
Cases are still rising alarmingly high

![Global Statistics](COVID19_worldwide.png)

### COVID-19 Active Cases Worldwide
The amount of active cases are slightly starting to flatten.

![Global Active Statistics](COVID19_worldwide_active.png)

### Where It All Began (China)
China's effective lockdown measures have resulted in a good recovery. China has slowly started going back to normal life, while still taking precautions of a second wave.

![china](cases_country/China_all.png)
![china](cases_country_active/China_active_cases.png)

### South Korea's Quick Response with Contact Tracing and Extensive Testing
South Korea responded quickly and was able contain the virus under 10,000 active cases.

![korea](cases_country/Korea,&#32;South_all.png)
![korea](cases_country_active/Korea,&#32;South_active_cases.png)

### The Last of US
Level of disorganized and opposing views of public health has caused economies to shut down and not take the virus to serious measures.

![us](cases_country/US_all.png)
![us](cases_country_active/US_active_cases.png)

### The Coronavirus Wave
The novel coronavirus has spread westward and the US will probably be the latest to recover fully based on the data and statistics. Eastern Asia also have to take serious precautions for a second wave, which could lead to another "coronavirus wave" westwards.

![COVID-19 Confirmed on Map](timelapses/global_confirmed_timelapse.gif)

### How Bad is it Over Here?
Showcasing the top 5 highest COVID-19 cases by states.

#### New York
New York city has it the worst, but curve is being slowly flattened.

![us](cases_us_states/New&#32;York.png)

#### New Jersey

![us](cases_us_states/New&#32;Jersey.png)

#### Massachusetts

![us](cases_us_states/Massachusetts.png)

#### Illinois

![us](cases_us_states/Illinois.png)

#### California
LA area is spreading more and more rapidly, as well as the Bay Area. Internships and jobs are being cancelled or remote for many of the big tech companies. Following the "coronavirus wave" concept, California may very well be the last state to recover fully from this epidemic.

![us](cases_us_states/California.png)

# COVID-19 Cases in the United States of America
I used the dataset provided by the [NYTimes](https://github.com/nytimes/covid-19-data). Although the dataset provided by JHU CSSE provides international data, the NYTimes has more specific metadata that is useful in analyzing the United States data like coronavirus cases by states and cities. COVID-19 cases are rising dangerously high in United States at the time of writing this. The NYTimes has already displayed useful [statistics](https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html) with their own database, but I decided to take it one step further and implement time factor.
