# COVID-19-Visualizations
Visualizations of the novel coronavirus using data science and machine learning techniques. Please feel free to contribute by sending issues or pull requests. I will do my best effort to update this daily. There is a lot of reading and writing of data involved, so the notebook tends to take around 10 minutes to completely run.

_Stay Strong, Stay Home, and Save Lives_

## Dependencies
This project uses Pandas, NumPy, MatPlotLib, GeoPandas, and Descartes. All the code needed to run is in `COVID19 Visualizations.ipynb`. Please make sure you have installed the all the Python libraries before you run the code. Also make sure to install `ffmpeg` if you want to compile graphics into video.

# Core Functions

## `country(country_name, data)`
Displays the graphs of a country associated with the type of data (confirmed, deaths, or recovered)

## `country_legend(country_name)`
Displays the graphs of all the types of data for a given country

## `customCountries(list_countries)`
Displays the all graph for a list of given countries. All on top of each other for comparison of statistics.

## `country_active_cases(country_name)`
Displays the graph of active cases of COVID-19 for a given country. Calculated by `active = confirmed - deaths - recovered`

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

# Confirmed COVID-19 Cases Worldwide

![COVID-19 Confirmed on Map](geo/geo_confirmed/confirmed_timelapse.gif)

# Deaths from COVID-19 Worldwide

![COVID-19 Deaths on Map](geo/geo_deaths/deaths_timelapse.gif)

# Recovered COVID-19 Cases Worldwide

![COVID-19 Recovered on Map](geo/geo_recovered/recovered_timelapse.gif)
