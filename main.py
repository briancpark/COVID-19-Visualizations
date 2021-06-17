#!/usr/bin/env python
# coding: utf-8

# #  COVID-19: DATA SCIENCE AND MACHINE LEARNING VISUALIZATIONS
# 
# I am currently using the [NYTimes](https://github.com/nytimes/covid-19-data) and [JHU CSSE](https://github.com/CSSEGISandData/COVID-19) database in this notebook. NYTimes is for USA data and JHU CSSE is for international data. Conveniently, they are all written in `.csv` files which Pandas can take great advantage of.
# 
# If you are planning to run the notebook on your own computer, please make sure you have all the dependencies installed! 

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import geopandas
import pycountry
import plotly
import plotly.express as px
import plotly.figure_factory as ff
import time
from datetime import datetime
import json
import os
from urllib.request import urlopen
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

get_ipython().run_line_magic('matplotlib', 'inline')

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

plotly.io.orca.config.executable = '/path/to/orca'
plotly.io.orca.config.save()


# ## Pulling the Databases
# For cloning the repository that contain the databases, I used `.gitignore` to prevent pushing large files to this repository. I do not modify the directories that contain the databases and I leave them as is.

# In[ ]:


#Please run this cell if databases directory is empty!
get_ipython().system('git clone https://github.com/CSSEGISandData/COVID-19 databases/jhucsse')
get_ipython().system('git clone https://github.com/nytimes/covid-19-data databases/nytimes')


# Run the cells below to get the most recent databases!

# In[ ]:


get_ipython().system('git -C databases/jhucsse pull origin master')
get_ipython().system('ls databases/jhucsse')


# In[ ]:


get_ipython().system('git -C databases/nytimes pull origin master')
get_ipython().system('ls databases/nytimes')


# ## Load `.csv` Files into Pandas DataFrames
# All the recent databases are pulled from GitHub

# In[ ]:


COVID19_confirmed = pd.read_csv("databases/jhucsse/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
COVID19_deaths = pd.read_csv("databases/jhucsse/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
COVID19_recovered = pd.read_csv("databases/jhucsse/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")

#Global variables
databases = [COVID19_confirmed, COVID19_deaths, COVID19_recovered]
dataset = [(COVID19_confirmed, "confirmed"), (COVID19_deaths, "deaths"), (COVID19_recovered, "recovered")]

all_countries = list(COVID19_confirmed['Country/Region'])
all_countries = list(dict.fromkeys(all_countries))

dates = list(COVID19_confirmed.columns)
dates.remove('Country/Region')
dates.remove('Province/State')
dates.remove('Lat')
dates.remove('Long')


# In[ ]:


COVID19_US = pd.read_csv("databases/nytimes/us.csv") #Already provided with the JHU CSSE
COVID19_US_states = pd.read_csv("databases/nytimes/us-states.csv")
COVID19_US_counties = pd.read_csv("databases/nytimes/us-counties.csv", dtype={"fips": str})

COVID19_US_states = COVID19_US_states.sort_values(by=['date'])

states = list(set(COVID19_US_states['state'].tolist()))


# ## Data Cleaning
# Cleaning unnecessary data.

# In[ ]:


def data_clean(data):
    data = data.drop(['Province/State', 'Lat', 'Long'], axis=1)
    data = data.groupby(['Country/Region'])[dates].sum()
    data.columns = pd.to_datetime(data.columns)
    return data


# In[ ]:


COVID19_confirmed = data_clean(COVID19_confirmed)
COVID19_deaths = data_clean(COVID19_deaths)
COVID19_recovered = data_clean(COVID19_recovered)
dataset = [(COVID19_confirmed, "confirmed"), (COVID19_deaths, "deaths"), (COVID19_recovered, "recovered")]


# ## Data Charts with Worldwide Data
# Functions to compile graphs

# In[ ]:


def cases_country(country_name, data, label=None):
    country_plot = data.loc[country_name]
    country_plot = country_plot.sort_index().plot(label=label)
    
    if data.equals(COVID19_confirmed):
        data_label = "Confirmed Cases"
    elif data.equals(COVID19_recovered):
        data_label = "Recovered"
    else:
        data_label = "Deaths"
    
    #Labelings
    country_plot.set_ylabel("Number of " + data_label)
    country_plot.set_xlabel("Day")
    country_plot.set_title(data_label + " in " + country_name)
    return country_plot


# In[ ]:


def update_all_cases_country_individual():
    for country in all_countries:
        for data in dataset:
            cases_country(country, data[0])
            plt.savefig("cases_country_individual/" + country + "_" + data[1] + ".png")
            plt.tight_layout()
            plt.clf()


# In[ ]:


def all_cases_country(country_name):
    for data in dataset:
        plt = cases_country(country_name, data[0], label=data[1])
    
    #Labelings
    plt.set_ylabel("Number of Cases")
    plt.set_xlabel("Day")
    plt.set_title("COVID-19 in " + country_name)
    plt.legend()
    return plt


# In[ ]:


def update_all_cases_country():
    for country in all_countries:
        all_cases_country(country)
        plt.savefig("cases_country/" + country + "_all.png")
        plt.tight_layout()
        plt.clf()


# In[ ]:


def worldwide_cases():
    world = COVID19_confirmed.sum().plot(label="confirmed")
    world = COVID19_deaths.sum().plot(label="deaths")
    world = COVID19_recovered.sum().plot(label="recovered")

    #Labelings
    world.set_ylabel("Number of Cases")
    world.set_xlabel("Day")
    world.set_title("COVID-19 Worldwide")
    world.legend()
    plt.savefig("COVID19_worldwide")
    return world


# In[ ]:


def cases_country_active(country_name):
    """
    active = confirmed - deaths - recovered
    """
    confirmed = COVID19_confirmed.loc[country_name]
    deaths = COVID19_deaths.loc[country_name]
    recovered = COVID19_recovered.loc[country_name]
    
    active = confirmed - deaths - recovered

    active = active.plot()
    active.set_ylabel("Number of Active Cases")
    active.set_xlabel("Day")
    active.set_title("Active COVID-19 Cases in " + country_name)


# In[ ]:


def update_all_cases_country_active():    
    for country in all_countries:
        cases_country_active(country)
        plt.savefig("cases_country_active/" + country + "_active_cases.png")
        plt.tight_layout()
        plt.clf()


# In[ ]:


def worldwide_active():
    confirmed = COVID19_confirmed.sum()
    deaths = COVID19_deaths.sum()
    recovered = COVID19_recovered.sum()
    
    active = confirmed - deaths - recovered
    active = active.plot()

    #Labelings
    active.set_ylabel("Number of Active Cases")
    active.set_xlabel("Day")
    active.set_title("COVID-19 Active Cases Worldwide")
    
    plt.savefig("COVID19_worldwide_active.png")
    return active


# In[ ]:


#Still testing and experimenting
def compare_countries(list_countries):    
    for country in list_countries:
        for data in dataset:
            country_data = data[0]
            country_data = country_data.loc[country]
            country_data = country_data.plot(label=data[1] + " in " + str(country))

    country_data.set_ylabel("Number of Cases")
    country_data.set_xlabel("Day")
    country_data.set_title("COVID-19 in " + str(list(list_countries)))
    country_data.legend()
    
    #plt.savefig(str(list_countries) + ".png")
    
compare_countries(['US'])


# In[ ]:


update_all_cases_country_individual()


# In[ ]:


update_all_cases_country()


# In[ ]:


worldwide_cases()


# In[ ]:


update_all_cases_country_active()


# In[ ]:


worldwide_active()


# ## Data with US Data
# Functions that chart US data, from the NYTimes database.

# In[ ]:


def cases_by_state(state):
    df = COVID19_US_states.loc[COVID19_US_states['state'] == state].drop(['fips'], axis=1)
    pd.to_datetime(df['date'])
    
    df = df.set_index(df['date']).drop(['date'], axis=1)
    df = df.sort_values(by=['date'])

    #return df
    return df.plot()


# In[ ]:


def update_states():
    for state in states:
        us_cases = cases_by_state(state)
        
        us_cases.set_ylabel("Cases")
        us_cases.set_xlabel("Day")
        us_cases.set_title("COVID-19 Cases in " + str(state))
        
        plt.savefig("cases_us_states/" + str(state) + ".png")
        plt.clf


# In[ ]:


cases_by_state('Washington')
update_states()


# # Visualizations with Global Data

# In[ ]:


world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))


# In[ ]:


COVID19_geo_confirmed = dataset[0][0]
COVID19_geo_deaths = dataset[1][0]
COVID19_geo_recovered = dataset[2][0]

COVID19_geo_confirmed.reset_index(level=0, inplace=True)
COVID19_geo_deaths.reset_index(level=0, inplace=True)
COVID19_geo_recovered.reset_index(level=0, inplace=True)

COVID19_geo_confirmed = COVID19_geo_confirmed.rename(columns={"Country/Region" : "name"})
COVID19_geo_deaths = COVID19_geo_deaths.rename(columns={"Country/Region" : "name"})
COVID19_geo_recovered = COVID19_geo_recovered.rename(columns={"Country/Region" : "name"})

COVID19_geo_confirmed = COVID19_geo_confirmed.replace({'Taiwan*': 'Taiwan', 'Korea, South': 'South Korea', 'US' : 'United States of America'})
COVID19_geo_deaths = COVID19_geo_deaths.replace({'Taiwan*': 'Taiwan', 'Korea, South': 'South Korea', 'US' : 'United States of America'})
COVID19_geo_recovered = COVID19_geo_recovered.replace({'Taiwan*': 'Taiwan', 'Korea, South': 'South Korea', 'US' : 'United States of America'})

#Delete any islands and Antartica
world_confirmed = world.merge(COVID19_geo_confirmed, how = 'inner', on = 'name')
world_confirmed = world_confirmed[(world_confirmed.pop_est>0) & (world_confirmed.name!="Antarctica")]

world_deaths = world.merge(COVID19_geo_deaths, how = 'inner', on = 'name')
world_deaths = world_deaths[(world_deaths.pop_est>0) & (world_deaths.name!="Antarctica")]

world_recovered = world.merge(COVID19_geo_recovered, how = 'inner', on = 'name')
world_recovered = world_recovered[(world_recovered.pop_est>0) & (world_recovered.name!="Antarctica")]


# In[ ]:


dates = list(COVID19_geo_confirmed)
dates.remove('name')
dates.sort()


# In[ ]:


def geo_confirmed_corona(data):    
    for i in range(len(dates)):
        fig, ax = plt.subplots(1, 1)

        world_confirmed.plot(column=dates[i],
                   cmap='Reds',
                   ax=ax,
                   legend=True,
                   legend_kwds={'label': "Population by Country",
                                'orientation': "horizontal"})

        #Save the figure
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(20, 10)
        fig.savefig('geo/geo_confirmed_normalized/' + str(i).zfill(3) + '.png', dpi=100)
        plt.close(fig)


# In[ ]:


def geo_deaths_corona(data):
    for i in range(len(dates)):
        fig, ax = plt.subplots(1, 1)

        world_deaths.plot(column=dates[i],
                   cmap='Greys',
                   ax=ax,
                   legend=True,
                   legend_kwds={'label': "Population by Country",'orientation': "horizontal"})

        #Save the figure
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(20, 10)
        fig.savefig('geo/geo_deaths_normalized/' + str(i).zfill(3) + '.png', dpi=100)
        plt.close(fig)


# In[ ]:


def geo_recovered_corona(data):
    for i in range(len(dates)):
        fig, ax = plt.subplots(1, 1)

        world_recovered.plot(column=dates[i],
                   cmap='Greens',
                   ax=ax,
                   legend=True,
                   legend_kwds={'label': "Population by Country",'orientation': "horizontal"})

        #Save the figure
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(20, 10)
        fig.savefig('geo/geo_recovered_normalized/' + str(i).zfill(3) + '.png', dpi=100)
        plt.close(fig)


# In[ ]:


geo_confirmed_corona(COVID19_geo_confirmed)
geo_deaths_corona(COVID19_geo_deaths)
geo_recovered_corona(COVID19_geo_recovered)


# In[ ]:


#New color theme to display color gradients
Solarcorona = ['rgb(252, 222, 156)', 'rgb(250, 164, 118)', 'rgb(240, 116, 110)', 'rgb(227, 79, 111)', 'rgb(220, 57, 119)', 'rgb(185, 37, 122)', 'rgb(124, 29, 111)', '#1b0c41', '#000004']


# In[ ]:


#SCRAP PREVIOUS
#New dataframes
mapping = {country.name: country.alpha_3 for country in pycountry.countries}
geo_confirmed = COVID19_confirmed.rename(index={'Korea, South': 'Korea, Republic of', 'US' :'United States', 'Taiwan*' :'Taiwan, Province of China', 'Vietnam':'Viet Nam', 'Russia': 'Russian Federation', 'Iran': 'Iran, Islamic Republic of', 'Tanzania': 'Tanzania, United Republic of', 'Laos': "Lao People's Democratic Republic", 'Syria': 'Syrian Arab Republic', 'Brunei': 'Brunei Darussalam', 'Venezuela': 'Venezuela, Bolivarian Republic of', 'Bolivia':  'Bolivia, Plurinational State of', 'Moldova': 'Moldova, Republic of'}).rename(index = lambda name: mapping.get(name))
geo_deaths = COVID19_deaths.rename(index={'Korea, South': 'Korea, Republic of', 'US' :'United States', 'Taiwan*' :'Taiwan, Province of China', 'Vietnam':'Viet Nam', 'Russia': 'Russian Federation', 'Iran': 'Iran, Islamic Republic of', 'Tanzania': 'Tanzania, United Republic of', 'Laos': "Lao People's Democratic Republic", 'Syria': 'Syrian Arab Republic', 'Brunei': 'Brunei Darussalam', 'Venezuela': 'Venezuela, Bolivarian Republic of', 'Bolivia':  'Bolivia, Plurinational State of', 'Moldova': 'Moldova, Republic of'}).rename(index = lambda name: mapping.get(name))
geo_recovered = COVID19_recovered.rename(index={'Korea, South': 'Korea, Republic of', 'US' :'United States', 'Taiwan*' :'Taiwan, Province of China', 'Vietnam':'Viet Nam', 'Russia': 'Russian Federation', 'Iran': 'Iran, Islamic Republic of', 'Tanzania': 'Tanzania, United Republic of', 'Laos': "Lao People's Democratic Republic", 'Syria': 'Syrian Arab Republic', 'Brunei': 'Brunei Darussalam', 'Venezuela': 'Venezuela, Bolivarian Republic of', 'Bolivia':  'Bolivia, Plurinational State of', 'Moldova': 'Moldova, Republic of'}).rename(index = lambda name: mapping.get(name))


# In[ ]:


#confirmed 500000
#deaths 10000
#recovered 100000

def geo_frames(df, file, case_range):
    for i in range(len(geo_confirmed.columns)):
        fig = px.choropleth(df, locations=df.index,
                            color=geo_confirmed.columns[i],
                            range_color=(0, case_range),
                            color_continuous_scale=Solarcorona,
                           )

        fig.update_layout(
            title_text = 'COVID-19 Cases Confirmed                        GitHub: briancpark',
        )

        #fig.show()
        fig.write_html("geo/" + file + "_html/" + str(i).zfill(3) + ".html")
        
#geo_frames(geo_confirmed, "geo_confirmed", 200000)


# In[ ]:


"""
for i in range(len(geo_confirmed.columns)):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("file:///Users/brianpark/Desktop/PUBLISHED%20Projects/COVID19/geo/geo_confirmed_html/" + str(i).zfill(3) + ".html")
    time.sleep(3)
    driver.save_screenshot("geo/geo_confirmed/" + str(i).zfill(3) + ".png")
    driver.close()
"""


# In[ ]:


#len(geo_confirmed.columns)


# # Visualizations with US Data
# For some reason, plotly doesn't want to work when `write_image()` is called, so I used selenium instead to screenshot. Not a very convenient way, but in the end it gives high quality graphs.

# In[ ]:


dates = list(set(list(COVID19_US_states['date'])))
dates.sort(key = lambda date: datetime.strptime(date, '%Y-%m-%d')) 
states = list(set(list(COVID19_US_states['state'])))


# In[ ]:


def create_html(i, data_type, data_label, color_gradient, max_cases, date):
    df = COVID19_US_counties#pd.read_csv("databases/nytimes/us-counties.csv", dtype={"fips": str})
    df = df[df['date']==date]

    fig = px.choropleth(df, geojson=counties, locations='fips', color=data_type,
                               color_continuous_scale=color_gradient,
                               range_color=(0, max_cases),
                               scope="usa",
                               labels={data_type:data_type}
                              )
    fig.update_layout(title_text = 'USA COVID-19 ' + data_label + ' by County on ' + str(date) + "              GitHub:briancpark")
    fig.write_html("geo/geo_us_" + data_type + "_html/" + str(i).zfill(3) + ".html")


# In[ ]:


def update_us_cases_by_counties(max_cases, limit):
        
    i = 0

    for date in dates:
        create_html(i, 'cases', 'Cases', "Sunsetdark", max_cases, date)       
        i = i + 1


# In[ ]:


def update_us_deaths_by_counties(max_cases, limit):
    i = 0
    
    for date in dates:
        create_html(i, 'deaths', 'Deaths', "Greys", max_cases, date)
        i = i + 1


# In[ ]:


def convert_to_png(file, limit):
    if file == "confirmed":
        directory = "geo_us_cases"
    else:
        directory = "geo_us_deaths"
    
    for i in range(len(dates) - limit, len(dates)):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1280x720');
        
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get("file:///Users/brianpark/Projects/COVID-19-Visualizations/geo/" + directory + "_html/" + str(i).zfill(3) + ".html")
        time.sleep(3)
        driver.save_screenshot("geo/" + directory + "/" + str(i).zfill(3) + ".png")
        driver.close()


# ## Compile Timelapses
# Create beautiful, and yet alarming dynamic graphs that implement time with COVID-19. `ffmpeg` is used to compile the `.gif` and `.mp4` files. Please make sure you have that installed. Can be simply done in your terminal via `pip install ffmpeg`

# In[ ]:


def compile_timelapse():
    get_ipython().system('rm timelapses/global_confirmed_timelapse.mp4')
    get_ipython().system('rm timelapses/global_deaths_timelapse.mp4')
    get_ipython().system('rm timelapses/global_recovered_timelapse.mp4')
    
    get_ipython().system('rm timelapses/global_confirmed_timelapse.gif')
    get_ipython().system('rm timelapses/global_deaths_timelapse.gif')
    get_ipython().system('rm timelapses/global_recovered_timelapse.gif')
    
    get_ipython().system('ffmpeg -r 15 -i geo/geo_confirmed/%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p timelapses/global_confirmed_timelapse.mp4')
    get_ipython().system('ffmpeg -r 15 -i geo/geo_deaths/%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p timelapses/global_deaths_timelapse.mp4')
    get_ipython().system('ffmpeg -r 15 -i geo/geo_recovered/%03d.png -c:v libx26|4 -r 30 -pix_fmt yuv420p timelapses/global_recovered_timelapse.mp4')
        
    get_ipython().system('ffmpeg -i timelapses/global_confirmed_timelapse.mp4 timelapses/global_confirmed_timelapse.gif')
    get_ipython().system('ffmpeg -i timelapses/global_deaths_timelapse.mp4 timelapses/global_deaths_timelapse.gif')
    get_ipython().system('ffmpeg -i timelapses/global_recovered_timelapse.mp4 timelapses/global_recovered_timelapse.gif')
    
    get_ipython().system('rm timelapses/global_confirmed_normalized_timelapse.mp4')
    get_ipython().system('rm timelapses/global_deaths_normalized_timelapse.mp4')
    get_ipython().system('rm timelapses/global_recovered_normalized_timelapse.mp4')
    
    get_ipython().system('rm timelapses/global_confirmed_normalized_timelapse.gif')
    get_ipython().system('rm timelapses/global_deaths_normalized_timelapse.gif')
    get_ipython().system('rm timelapses/global_recovered_normalized_timelapse.gif')
    
    get_ipython().system('ffmpeg -r 15 -i geo/geo_confirmed_normalized/%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p timelapses/global_confirmed_normalized_timelapse.mp4')
    get_ipython().system('ffmpeg -r 15 -i geo/geo_deaths_normalized/%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p timelapses/global_deaths_normalized_timelapse.mp4')
    get_ipython().system('ffmpeg -r 15 -i geo/geo_recovered_normalized/%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p timelapses/global_recovered_normalized_timelapse.mp4')
        
    get_ipython().system('ffmpeg -i timelapses/global_confirmed_normalized_timelapse.mp4 timelapses/global_confirmed_normalized_timelapse.gif')
    get_ipython().system('ffmpeg -i timelapses/global_deaths_normalized_timelapse.mp4 timelapses/global_deaths_normalized_timelapse.gif')
    get_ipython().system('ffmpeg -i timelapses/global_recovered_normalized_timelapse.mp4 timelapses/global_recovered_normalized_timelapse.gif')
    
    get_ipython().system('rm timelapses/us_confirmed_timelapse.mp4')
    get_ipython().system('rm timelapses/us_confirmed_timelapse.gif')
    
    get_ipython().system('rm timelapses/us_deaths_timelapse.mp4')
    get_ipython().system('rm timelapses/us_deaths_timelapse.gif')
    
    get_ipython().system('ffmpeg -r 15 -i geo/geo_us_cases/%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p timelapses/us_confirmed_timelapse.mp4    ')
    get_ipython().system('ffmpeg -i timelapses/us_confirmed_timelapse.mp4 timelapses/us_confirmed_timelapse.gif')
    
    get_ipython().system('ffmpeg -r 15 -i geo/geo_us_deaths/%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p timelapses/us_deaths_timelapse.mp4')
    get_ipython().system('ffmpeg -i timelapses/us_deaths_timelapse.mp4 timelapses/us_deaths_timelapse.gif')


# In[ ]:


update_us_cases_by_counties(10000, 5)#len(dates)


# In[ ]:


update_us_deaths_by_counties(1000, 5)


# In[ ]:


convert_to_png("confirmed", 5) #len(dates)) #10


# In[ ]:


convert_to_png("deaths", 5)


# In[ ]:


compile_timelapse()


# In[ ]:


## print(px.colors.sequential.Inferno)


# In[ ]:


"""#Debugging cell
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

plotly.io.orca.config.executable = '/path/to/orca'
plotly.io.orca.config.save()

df = pd.read_csv("databases/nytimes/us-counties.csv", dtype={"fips": str})
df = df[df['date']=="2020-05-08"]
df['cases'] = 1 / np.log10(df["cases"])

Solarcorona = ['rgb(252, 222, 156)', 'rgb(250, 164, 118)', 'rgb(240, 116, 110)', 'rgb(227, 79, 111)', 'rgb(220, 57, 119)', 'rgb(185, 37, 122)', 'rgb(124, 29, 111)', '#1b0c41', '#000004']

#Solarcorona = ['rgb(252, 222, 156)', 'rgb(250, 164, 118)', 'rgb(220, 57, 119)', 'rgb(185, 37, 122)', 'rgb(124, 29, 111)', '#1b0c41', '#000004', '#000004', '#000004', '#000004', '#000004', '#000004', '#000004', '#000004', '#000004']

fig = px.choropleth(df, geojson=counties, locations='fips', color='cases',
                           color_continuous_scale=Solarcorona,
                           range_color=(0, 100000),
                           scope="usa",
                           labels={'cases':'cases'}
                          )
fig.update_layout(#margin={"r":0,"t":0,"l":0,"b":0}),
                  title_text = 'USA COVID-19 Cases by County on ' + "05-08" + "              GitHub:briancpark",
coloraxis_colorbar=dict(
    title="Population",
    ticktext=["1M", "10M", "100M", "1B"],
))


                    
fig.show()
"""


# In[ ]:


"""
#Debugging cell
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

plotly.io.orca.config.executable = '/path/to/orca'
plotly.io.orca.config.save()

df = pd.read_csv("databases/nytimes/us-counties.csv", dtype={"fips": str})
df = df[df['date']=="2020-05-08"]

Solarcorona = ['rgb(252, 222, 156)', 'rgb(250, 164, 118)', 'rgb(240, 116, 110)', 'rgb(227, 79, 111)', 'rgb(220, 57, 119)', 'rgb(185, 37, 122)', 'rgb(124, 29, 111)', '#1b0c41', '#000004']

#Solarcorona = ['rgb(252, 222, 156)', 'rgb(250, 164, 118)', 'rgb(220, 57, 119)', 'rgb(185, 37, 122)', 'rgb(124, 29, 111)', '#1b0c41', '#000004', '#000004', '#000004', '#000004', '#000004', '#000004', '#000004', '#000004', '#000004']

fig = px.choropleth(df, geojson=counties, locations='fips', color='deaths',
                           color_continuous_scale="Greys",
                           range_color=(0, 100),
                           scope="usa",
                           labels={'deaths':'deaths'},
                          )
fig.update_layout(#margin={"r":0,"t":0,"l":0,"b":0}),
                  title_text = 'USA COVID-19 Deaths by County on ' + "05-08" + "              GitHub:briancpark")
fig.show()
"""


# In[ ]:


"""
#Debugging this cell

df = pd.read_csv("databases/nytimes/us-counties.csv", dtype={"fips": str})
df['fips'] = pd.to_numeric(df['fips'], errors='coerce')
df = df.dropna(subset=['fips'])
df['fips'] = df['fips'].astype(int)
df = df[df['date']=="2020-05-05"]


colorscale = ["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
    "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
    "#08519c", "#0b4083", "#08306b"]
    
endpts = list(np.linspace(1, 1000, len(colorscale) - 1))
fips = df['fips'].tolist()
values = df['cases'].tolist()


fig = ff.create_choropleth(
    fips=fips, values=values, scope=['usa'],
    binning_endpoints=endpts, colorscale=colorscale,
    show_state_data=False,
    show_hover=True,
    asp = 2.9,
    title_text = 'COVID-19 in USA',
    legend_title = 'Cases'
)
fig.layout.template = None
fig.show()


#plotly.io.write_image(fig, "image.png", format=None, scale=None, width=None, height=None)
"""


# # Machine Learning Methods
# A start. Goal is to predict coronavirus cases before a lockdown has initiated, and then compare it to real data. I will learn how machine learning works someday

# In[ ]:


df = COVID19_US_states.loc[COVID19_US_states['state'] == 'New York'].drop(['fips'], axis=1)
pd.to_datetime(df['date'])

df = df.set_index(df['date']).drop(['date'], axis=1)
df = df.sort_values(by=['date'])

#df.plot()

#ates_test = 
nydates = df.index.to_list()[:22]
lockdown_dates = df.index.to_list()[22:]

df.head(22)


# In[ ]:


from scipy.optimize import curve_fit
x = np.array(range(len(nydates)))
y = np.array(df['cases'].tolist()[:22])

def func(x, a, b, c):
    return a * np.exp(-b * x) + c

popt, pcov = curve_fit(func, x, y, p0=(1, 1e-6, 1))
popt


# In[ ]:


xx = np.array(range(len(nydates) + len(lockdown_dates)))
yy = func(xx, *popt)


# In[ ]:


#plt.plot(x, y, 'ko')
#plt.plot(xx, yy)
plt.plot(df.index.to_list(), df['cases'].to_list())


# # Drafts and Debugging For More Visualizations!

# In[ ]:


import plotly.express as px

df = px.data.election()
geojson = px.data.election_geojson()

#print(df["district"][2])
#print(geojson["features"][0]["properties"])
df = COVID19_US_counties[COVID19_US_counties['state'] == 'Alabama']
df = df[df['date'] == '2020-04-01']
df


# In[ ]:


from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
df = df

import plotly.express as px

fig = px.choropleth(df, geojson=counties, locations='fips', color='cases',
                           color_continuous_scale="Viridis",
                           range_color=(0, 10000),
                           scope="usa",
                           labels={'cases':'cases'}
                          )
#fig.show()


# In[ ]:


counties


# In[ ]:


def retrieve_state_json(state):
    custom = counties.copy()

    for county in custom["features"]:
        if county['properties']["STATE"] != "01":
            custom["features"].remove(county)


# In[ ]:


custom = counties.copy()

for county in custom["features"]:
    if county['properties']["STATE"] != "01":
        custom["features"].remove(county)


# In[ ]:


custom


# In[ ]:


from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
df = df

import plotly.express as px

fig = px.choropleth(df, geojson=custom, locations='fips', color='cases',
                           color_continuous_scale="Viridis",
                           range_color=(0, 10000),
                           scope="usa",
                           labels={'cases':'cases'}
                          )
fig.update_geos(fitbounds="locations")
#fig.show()


# In[ ]:


import plotly.express as px

df = df
geojson = custom

fig = px.choropleth(df, geojson=custom, color="cases",
                    locations="county", featureidkey="01001",
                    projection="mercator"
                   )
fig.update_geos(fitbounds="locations", visible=True)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#fig.show()


# In[ ]:


custom


# In[ ]:


custom['features'][0]


# # BREAK

# In[ ]:


#New dataframes
mapping = {country.name: country.alpha_3 for country in pycountry.countries}
geo_confirmed = COVID19_confirmed.rename(index={'Korea, South': 'Korea, Republic of', 'US' :'United States', 'Taiwan*' :'Taiwan, Province of China', 'Vietnam':'Viet Nam', 'Russia': 'Russian Federation', 'Iran': 'Iran, Islamic Republic of', 'Tanzania': 'Tanzania, United Republic of', 'Laos': "Lao People's Democratic Republic", 'Syria': 'Syrian Arab Republic', 'Brunei': 'Brunei Darussalam', 'Venezuela': 'Venezuela, Bolivarian Republic of', 'Bolivia':  'Bolivia, Plurinational State of', 'Moldova': 'Moldova, Republic of'}).rename(index = lambda name: mapping.get(name))
geo_deaths = COVID19_deaths.rename(index={'Korea, South': 'Korea, Republic of', 'US' :'United States', 'Taiwan*' :'Taiwan, Province of China', 'Vietnam':'Viet Nam', 'Russia': 'Russian Federation', 'Iran': 'Iran, Islamic Republic of', 'Tanzania': 'Tanzania, United Republic of', 'Laos': "Lao People's Democratic Republic", 'Syria': 'Syrian Arab Republic', 'Brunei': 'Brunei Darussalam', 'Venezuela': 'Venezuela, Bolivarian Republic of', 'Bolivia':  'Bolivia, Plurinational State of', 'Moldova': 'Moldova, Republic of'}).rename(index = lambda name: mapping.get(name))
geo_recovered = COVID19_recovered.rename(index={'Korea, South': 'Korea, Republic of', 'US' :'United States', 'Taiwan*' :'Taiwan, Province of China', 'Vietnam':'Viet Nam', 'Russia': 'Russian Federation', 'Iran': 'Iran, Islamic Republic of', 'Tanzania': 'Tanzania, United Republic of', 'Laos': "Lao People's Democratic Republic", 'Syria': 'Syrian Arab Republic', 'Brunei': 'Brunei Darussalam', 'Venezuela': 'Venezuela, Bolivarian Republic of', 'Bolivia':  'Bolivia, Plurinational State of', 'Moldova': 'Moldova, Republic of'}).rename(index = lambda name: mapping.get(name))


# In[ ]:


"""
df = geo_deaths
fig = px.choropleth(df, locations=df.index,
                    color="2020-02-10", # lifeExp is a column of gapminder
                    range_color=(0, 10000),
                    color_continuous_scale=Solarcorona,
                   )

fig.update_layout(
    title_text = 'COVID-19 Cases Confirmed                        GitHub: briancpark',
)

fig.show()
"""


# # Mask Usage
# Data was provided by the New York Times. Playing around with more data here.

# In[ ]:


#Load mask usage database
US_masks = pd.read_csv("databases/nytimes/mask-use/mask-use-by-county.csv")


# In[ ]:


US_masks


# In[ ]:


US_masks['COUNTYFP'] = US_masks['COUNTYFP'].apply(lambda x: '{0:0>5}'.format(x))


# In[ ]:


fig = px.choropleth(US_masks, geojson=counties, locations='COUNTYFP', color='ALWAYS',
                           color_continuous_scale="reds",
                           range_color=(0, 1),
                           scope="usa",
                           labels={'masks':'always'}
                          )

fig.update_layout(title_text = 'US Citizens Who Always Wears Masks in Social Distancing             GitHub:briancpark')
fig.write_html("geo/us_mask_usage_html/always.html")
#fig.show()


# In[ ]:


fig = px.choropleth(US_masks, geojson=counties, locations='COUNTYFP', color='FREQUENTLY',
                           color_continuous_scale="reds",
                           range_color=(0, 1),
                           scope="usa",
                           labels={'masks':'always'}
                          )

fig.update_layout(title_text = 'US Citizens Who Frequently Wears Masks in Social Distancing             GitHub:briancpark')
fig.write_html("geo/us_mask_usage_html/frequently.html")
#fig.show()


# In[ ]:


fig = px.choropleth(US_masks, geojson=counties, locations='COUNTYFP', color='SOMETIMES',
                           color_continuous_scale="reds",
                           range_color=(0, 1),
                           scope="usa",
                           labels={'masks':'always'}
                          )

fig.update_layout(title_text = 'US Citizens Who Sometimes Wears Masks in Social Distancing             GitHub:briancpark')
fig.write_html("geo/us_mask_usage_html/sometimes.html")
#fig.show()


# In[ ]:


fig = px.choropleth(US_masks, geojson=counties, locations='COUNTYFP', color='RARELY',
                           color_continuous_scale="reds",
                           range_color=(0, 1),
                           scope="usa",
                           labels={'masks':'always'}
                          )

fig.update_layout(title_text = 'US Citizens Who Rarely Wears Masks in Social Distancing             GitHub:briancpark')
fig.write_html("geo/us_mask_usage_html/rarely.html")
#fig.show()


# In[ ]:


fig = px.choropleth(US_masks, geojson=counties, locations='COUNTYFP', color='NEVER',
                           color_continuous_scale="reds",
                           range_color=(0, 1),
                           scope="usa",
                           labels={'masks':'always'}
                          )

fig.update_layout(title_text = 'US Citizens Who Never Wears Masks in Social Distancing             GitHub:briancpark')
fig.write_html("geo/us_mask_usage_html/never.html")
#fig.show()


# In[ ]:


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080');

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get("file:///Users/brianpark/Projects/COVID-19-Visualizations/geo/us_mask_usage_html/always.html")
time.sleep(3)
driver.save_screenshot("geo/us_mask_usage/always.png")
driver.close()


# In[ ]:


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080');

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get("file:///Users/brianpark/Projects/COVID-19-Visualizations/geo/us_mask_usage_html/sometimes.html")
time.sleep(3)
driver.save_screenshot("geo/us_mask_usage/sometimes.png")
driver.close()


# In[ ]:


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080');

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get("file:///Users/brianpark/Projects/COVID-19-Visualizations/geo/us_mask_usage_html/frequently.html")
time.sleep(3)
driver.save_screenshot("geo/us_mask_usage/frequently.png")
driver.close()


# In[ ]:


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080');

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get("file:///Users/brianpark/Projects/COVID-19-Visualizations/geo/us_mask_usage_html/rarely.html")
time.sleep(3)
driver.save_screenshot("geo/us_mask_usage/rarely.png")
driver.close()


# In[ ]:


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080');

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get("file:///Users/brianpark/Projects/COVID-19-Visualizations/geo/us_mask_usage_html/never.html")
time.sleep(3)
driver.save_screenshot("geo/us_mask_usage/never.png")
driver.close()


# In[ ]:


import subprocess as cmd


from datetime import date

cmd.run("git add .", check=True, shell=True)


# In[ ]:


cmd.run('git commit -m ' + '''"''' + str(date.today()) + ''' update"''', check=True, shell=True)


# In[ ]:


#os.system('git push')


# In[ ]:


get_ipython().system('git push')


# In[ ]:




