from haversine import Unit
import haversine as hs
import pandas as pd
from typing import List
from datetime import datetime as dtime
import datetime
from meteostat import Point, Daily
import operator
from functools import reduce
import folium



# from scripts.setting_logs import get_rotating_log

class FeatureExtraction:
    def __init__(self) -> None:
        pass
        
    def distance_from(self,loc1,loc2): 
        dist = hs.haversine(loc1,loc2)
        return round(dist,2)
    
    def distance_from(self,loc1,loc2): 
        dist = hs.haversine(loc1,loc2,unit=Unit.METERS)
        return round(dist,2)

    def cordinate_tupple(self,df,columns):
        for col in columns:
            df[col] = df[col].apply(
                lambda x:(float(x.split(',')[0]),float(x.split(',')[1])))
        return df  

    def convert_to_date(self,df, columns):
        for col in columns:
            df[col] =  df[col].apply(lambda x: pd.to_datetime(x))
        return df
    
    def get_ymwdh(self,df,column):
        # features['year'] = clean_df['trip_Start_time'].dt.year
        df['month'] = df[column].dt.month
        df['day'] = df[column].dt.day
        df['week_day'] = df[column].dt.weekday
        df['hour'] = df[column].dt.hour
        return df
    
    def transform(self, df: pd.DataFrame = None):
        # if not isinstance(df, NoneType):
        self.df = df.copy()
        assert 'Date' in self.df.columns
        df = self.drop_columns(df)
        self.holidays = self._set_holidays(df)
        df = self.generate_columns(df)
        df = self.create_holiday_distance_cols(df, holidays=self.holidays)
        
        # logger.info("Feature enginerring completed")

        return df
    
    def generate_columns(self,df:pd.DataFrame) -> None:
        """Adds date related categorical columns to the dataframe"""

        # df.loc[:, ['Year']] = pd.to_datetime( df['Date'], format='%Y-%m-%d').dt.year
        df.loc[:, ['Month']] = pd.to_datetime(df['trip_Start_time'], format='%Y-%m-%d').dt.month
        df.loc[:, ['WeekOfYear']] = pd.to_datetime(df['Date'], format='%Y-%m-%d').dt.isocalendar().week
        df.loc[:, ['is_month_end']] = pd.to_datetime(df['Date'], format='%Y-%m-%d').dt.is_month_end
        df.loc[:, ['is_month_start']] = pd.to_datetime(df['Date'], format='%Y-%m-%d').dt.is_month_start
        df.loc[:, ['is_quarter_end']] = pd.to_datetime(df['Date'], format='%Y-%m-%d').dt.is_quarter_end
        df.loc[:, ['is_quarter_start']] = pd.to_datetime(df['Date'], format='%Y-%m-%d').dt.is_quarter_start
        df.loc[:, ['is_year_end']] = pd.to_datetime(df['Date'], format='%Y-%m-%d').dt.is_year_end
        df.loc[:, ['is_year_start']] = pd.to_datetime(df['Date'], format='%Y-%m-%d').dt.is_year_start 
      
        # logger.info("9 new columns added to the dataframe")
        
        return df

    def create_holiday_distance_cols(self,df:pd.DataFrame,holidays) -> None:
        df['DistanceToNextHoliday'] = pd.NA
        df['DistanceFromPrevHoliday'] = pd.NA
        
        unique_dates = pd.to_datetime(df.Date, format = '%Y-%m-%d').unique()
        for date in unique_dates:
            after_holiday, to_next_holiday = self._get_holiday_distances(date,holidays=holidays)
            indecies = df[pd.to_datetime(
                df['Date'], format='%Y-%m-%d') == date].index
            df.loc[indecies, 'DistanceToNextHoliday'] = to_next_holiday
            df.loc[indecies, 'DistanceFromPrevHoliday'] = after_holiday
            
        # logger.info( f"generated holidays distance")
        
        df['DistanceToNextHoliday'] = df['DistanceToNextHoliday'].astype('int')
        df['DistanceFromPrevHoliday'] = df['DistanceFromPrevHoliday'].astype('int')
        
        return df
    
    def _set_holidays(self,df:pd.DataFrame) -> None:
        """Filters the holiday dates from a given dateframe"""
        
        holidays = pd.to_datetime(df.query(
            "StateHoliday in ['a', 'b', 'c']")['Date'], format='%Y-%m-%d').dt.date.unique()

        holidays.sort()
        
        # logger.info(f"generatd holidays")
        return holidays

    def _get_holiday_distances(self, date,holidays) -> List[int]:
        """takes in a date, then tells me it's distance on both dxns for the closest holiday"""
        previous, upcoming = self._get_neighbors(date, holidays)

        after_holiday = date - previous

        to_next_holiday = upcoming - date

        return int(after_holiday.days), int(to_next_holiday.days)

    def _get_neighbors(self, date,holidays) -> List[pd.to_datetime]:
        """uses a sorted list of dates to get the neighboring 
        dates for a date. 
        """
        date = pd.to_datetime(date)
        original_year = None
        if date.year >= holidays[-1].year:
            original_year = date.year
            # Assume the date given is in 2014
            date = pd.to_datetime(f"2014-{date.month}-{date.day}")
        previous, upcoming = None, None
        for i, d in enumerate(holidays):
            if d >= date.date():
                previous = pd.to_datetime(holidays[i-1])
                upcoming = pd.to_datetime(holidays[i])
                if original_year:
                    previous = pd.to_datetime(
                        f"{original_year}-{previous.month}-{previous.day}")
                    upcoming = pd.to_datetime(
                        f"{original_year}-{upcoming.month}-{upcoming.day}")
                return previous, upcoming


    def get_weather_data(self, weather_data):

        # Define location for Lagos, Nigeria
        lagos = Point(6.5244, 3.3792)

        # Define time range for the data
        start_date = self.df['Trip Start Time'].min().to_pydatetime()
        # decrease one day from the start date
        start_date = start_date - pd.Timedelta(days=1)
        end_date = self.df['Trip Start Time'].max().to_pydatetime()
        
        # Get daily weather data for Lagos
        weather_data = Daily(lagos, start_date, end_date)
        weather_data = weather_data.fetch()

        return weather_data
    def get_route(self, lat1, lon1, lat2, lon2, trip_id, profile, view):
        lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
        # Initialize the map
        if view == "satellite":
            m = folium.Map(location=[lat1, lon1], tiles="Esri WorldImagery", attr="Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community")
        else:
            m = folium.Map(location=[lat1, lon1], tiles="cartodbpositron")

        # Create the coordinate list for routing
        coords = [[lon1, lat1], [lon2, lat2]]  # Note: Longitude, Latitude order

        # Assuming you have a client object set up for your routing service (e.g., Openrouteservice)
        route = self.client.directions(
            coordinates=coords,
            profile=profile,  # Updated profile for cycling-road directions
            format="geojson",
        )

        # Extract waypoints
        waypoints = list(
            dict.fromkeys(
                reduce(
                    operator.concat,
                    list(
                        map(
                            lambda step: step["way_points"],
                            route["features"][0]["properties"]["segments"][0]["steps"],
                        )
                    ),
                )
            )
        )

        # Draw the route
        folium.PolyLine(
            locations=[list(reversed(coord)) for coord in route["features"][0]["geometry"]["coordinates"]],
            color="blue",
        ).add_to(m)

        # Highlight waypoints
        folium.PolyLine(
            locations=[
                list(reversed(route["features"][0]["geometry"]["coordinates"][index]))
                for index in waypoints
            ],
            color="red",
        ).add_to(m)

        # Add a marker for the start point
        folium.Marker(location=[lat1, lon1], popup=f"Start: {trip_id}").add_to(m)

        # Add a marker for the end point
        folium.Marker(location=[lat2, lon2], popup=f"End: {trip_id}").add_to(m)

        # Calculate the bounds of the route
        min_lat, max_lat = min(lat1, lat2), max(lat1, lat2)
        min_lon, max_lon = min(lon1, lon2), max(lon1, lon2)

        # Set the zoom level dynamically based on the bounds
        m.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])

        # Calculate the distance
        distance_in_meters = route["features"][0]["properties"]["summary"]["distance"]
        distance_in_kilometers = distance_in_meters / 1000

        # Return the map and distance
        return m, distance_in_kilometers


    def combine_get_driver_locations(self, df_trip, df_driver):
        # df_t = df_trip.copy()
        driver_lat_ls = []
        driver_lng_ls = []
        k = 0
        for i, df in df_trip.iterrows():
            try:
                trip_id = df['Trip ID']
                drivers = df_driver[df_driver['order_id']==trip_id]
                driver = drivers[drivers['driver_action']=="accepted"]
                if len(driver)>0:
                    driver_lat_ls.append(float(driver['lat']))
                    driver_lng_ls.append(float(driver['lng']))
                    # df['driver_lat'] = driver['lat']
                    # df['driver_lng'] = driver['lng']
                else:
                    if len(drivers) > 0:
                        driver_lat_ls.append(0.5)
                        driver_lng_ls.append(0.5)
                    else:
                        driver_lat_ls.append(0.0)
                        driver_lng_ls.append(0.0)
            # k+=1
            # if k > 1000:
            #     print(k)
            #     k=0
            except Exception as e:
                driver_lat_ls.append(0.0)
                driver_lng_ls.append(0.0)

        return driver_lat_ls, driver_lng_ls  
            