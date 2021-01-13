import pandas as pd
import streamlit as st
import pydeck as pdk


lat = 43.57329
lon = -116.60422
search_radius = .15
Locations = ['Nampa', 'Eagle', 'Raleigh', 'DC','Other']
dot_size=120
cities = pd.read_csv('uscities.csv')
cities['city'] = cities.city.map(str) + ', ' + cities.state_name

sorted_df = cities.sort_values('city', ascending=True)

#data['Latitude'] = pd.to_numeric(data['Latitude'], downcast='float')
def filter(lat=lat,lon=lon, search_radius=search_radius):
    df = pd.read_csv('parler-vidoes-geocoded.csv')
    df = df[(df['Latitude'] < lat + search_radius)]
    df = df[(df['Latitude'] > lat - search_radius)]
    df = df[(df['Longitude'] < lon + search_radius)]
    df = df[(df['Longitude'] > lon - search_radius)]
    return(df)
#st.dataframe(df)


def lat_lon(df,dot_size=dot_size):
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state=pdk.ViewState(
            latitude=lat,
            longitude=lon,
            zoom=9,
            pitch=0,
            bearing=0
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[Longitude, Latitude]',
                get_color= [255,0,0],
                get_radius=dot_size,
            ),
        ],
    ))
#where = st.selectbox('Location', options=list(Locations))
#city = st.selectbox('City', options=list(cities['city'].tolist()))
city = st.selectbox('City', options=list(sorted_df['city'].tolist()))
city_row = sorted_df[sorted_df['city'].str.match(city)]
lat = float(city_row['lat'])
lon = float(city_row['lng'])

cities.sort_values('city', ascending=True)
search_radius = float(st.text_input('Search Radius', search_radius))
dot_size = st.slider('Dot Radius', 120, 2000, 200)
    
    
lat_lon(filter(lat,lon,search_radius),dot_size)